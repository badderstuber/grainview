#!/usr/bin/env python3
"""mg_load.py - load a WAV into the Multigrain's SELECTED sound over SWD.

Drives the firmware's own front-panel file-browse routine (what turning the
encoder in file mode does), so the sample loads AND the sound's filename param
is updated via its setter (project saves it). RE notes, all from 1.4.8.0:

    FUN_0803e710(ui, delta)  browse+load: cursor += delta (clamped), load that
                             file into the current sound; filename set only
                             on success. Returns 1 ok / 0 fail.
    current sound            u8  @ 0x24025b30; set via FUN_08011980(n) (reactive
                             setter: store + notify handler @ +0xfa4/+0xfa8)
                             = edit focus only. Playback: post engine event 3
                             (FUN_0802a25c(3), or write bit 3 of 0x240441b8 -
                             we do that, no halt); FUN_0801a49c then copies the
                             selected sound into playing (0x20008c5c +0x14/+0x1c)
    sound struct N           0x24020b84 + N*0x9f0; source u8 @ +0x59c
                             (0=project folder, 1=/Wavs, 2=/Recs)
    file counts              u32 @ 0x240272d4 + folder*4
    file lists               folder0 names @ 0x30000800, folder1 @ 0x30008800
                             (0x100 each); folder2 = int list @ 0x30010800 -> Rec%05d.wav
    browse cursor            i32 @ 0x24033344 + (folder*8 + sound)*4
    SD state                 u32 @ 0x20008ccc (1=busy, 3=error/no card)

The call is only injected while the CPU sits in main()'s idle loop (thread
mode, PC in 0x0800ba9a..0x0800baa0) - the same context the UI task runs in.

Usage:
    tools/venv/bin/python tools/mg_load.py              # status (read-only)
    tools/venv/bin/python tools/mg_load.py 10 --dry-run # plan, no call
    tools/venv/bin/python tools/mg_load.py 10           # load file 10
    tools/venv/bin/python tools/mg_load.py --sound 2         # focus Sound 2, keep playing
    tools/venv/bin/python tools/mg_load.py --sound 2 --play  # focus + switch playback
    tools/venv/bin/python tools/mg_load.py --sound 2 5  # load file 5 into Sound 2, no interruption
    tools/venv/bin/python tools/mg_load.py --folder wavs     # list /Wavs (any folder)
    tools/venv/bin/python tools/mg_load.py --folder recs 3   # load Rec [3] (changes the
                                                             # sound's folder, like ALT+folder)
"""
import argparse
import os
import struct
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from mg_call import connect, swd_call  # noqa: E402

BROWSE_LOAD_FN = 0x0803E710
SET_FOLDER_FN = 0x0803E91C    # panel's folder buttons: set sound's folder (setter +
                              # notify), then BROWSE_LOAD(ui, 0) = load at that folder's
                              # cursor. An EMPTY sound is reset first (params from the
                              # template, cursors -> 0 / newest Rec) - see load_plan()
BROWSER_UI = 0x240452C8      # r0 the UI passes (file-browser screen object)
SELECT_SOUND_FN = 0x08011980  # set current sound (0-7) + fire change notify
EV_PLAY_SELECTED = 3          # engine tick: playing sound (0x20008c70) = selected
CUR_SOUND = 0x24025B30
STATE = 0x20008C5C            # engine/UI state block
PLAYING = STATE + 0x14        # u32 playing sound
EVENTS = 0x240441B8           # engine event bits (posted |=, consumed per tick)
SOUND_BASE = 0x24020B84
SOUND_STRIDE = 0x9F0
SRC_OFF = 0x59C
COUNTS = 0x240272D4
LISTS = {0: 0x30000800, 1: 0x30008800}
REC_LIST = 0x30010800
CURSORS = 0x24033344
SD_STATE = 0x20008CCC
IDLE_LO, IDLE_HI = 0x0800BA9A, 0x0800BAA0
FNAME_OFF = {0: 0x7DC, 1: 0x6C8, 2: 0x5B4}   # sound struct filename per folder
FOLDERS = {0: "project folder", 1: "/Multigrain/Wavs", 2: "/Multigrain/Recs"}
MAX_FILES = {0: 0x80, 1: 0x80, 2: 0x400}     # list sizes in RAM
EMPTY_MASK = STATE + 0x40     # u32 bit n = sound n is a Live Sound (mg_rec.LIVE_MASK);
                              # FUN_080128a4's "has audio" = this bit or AUDIO_LEN != 0
AUDIO_LEN = 0x20000160 + 0x378  # + n*0x10: u32 sample length  (FUN_080128a4)
LOST_OFF = 0x4F4              # u8 per sound; non-zero = 0x0803e91c skips the reset
# The firmware every address here was mapped on (Multigrain.1.4.8.0.bin, not in git: it's
# Intellijel's). No version string in the image, so the build is known by the SHA-256 of
# its flash image; anything else = hands off (grainview_server, the Pico's pico/mgfw.py).
FW_VERSION = "1.4.8.0"
FW_BASE, FW_SIZE = 0x08000000, 634672
FW_SHA256 = "2c1ce5ea2216aaed6a2bca0d2cab655e4293ca352a886ca405eed66fca51a71c"


def fw_ok(t):
    """True if the module runs FW_VERSION: its flash image hashed (~2 s, read-only)."""
    import hashlib
    h = hashlib.sha256()
    for a in range(FW_BASE, FW_BASE + FW_SIZE, 0x8000):
        h.update(bytes(t.read_memory_block8(a, min(0x8000, FW_BASE + FW_SIZE - a))))
    return h.hexdigest() == FW_SHA256


def u8(t, a):
    return t.read_memory(a, 8)


def u32(t, a):
    return t.read_memory(a)


def i32(t, a):
    return struct.unpack("<i", struct.pack("<I", u32(t, a)))[0]


def file_names(t, folder, count):
    if folder in LISTS:
        out = []
        for i in range(count):
            raw = bytes(t.read_memory_block8(LISTS[folder] + i * 0x100, 0x100))
            out.append(raw.split(b"\0", 1)[0].decode("latin-1"))
        return out
    nums = [struct.unpack("<i", struct.pack("<I", v))[0]
            for v in t.read_memory_block32(REC_LIST, count)] if count else []
    return ["Rec%05d.wav" % abs(n) for n in nums]


def status(t, snd=None):
    if snd is None:
        snd = u8(t, CUR_SOUND)
    folder = u8(t, SOUND_BASE + snd * SOUND_STRIDE + SRC_OFF)
    count = folder_count(t, folder) if folder in FOLDERS else 0
    cursor = i32(t, CURSORS + (folder * 8 + snd) * 4) if folder in FOLDERS else 0
    sd = u32(t, SD_STATE)
    return snd, folder, count, cursor, sd


def folder_count(t, folder):
    return min(u32(t, COUNTS + folder * 4), MAX_FILES[folder])


def sound_is_empty(t, snd):
    """FUN_0803e91c's test for resetting the sound before a folder change:
    no audio (FUN_080128a4() == 0) and +0x4f4 == 0."""
    has_audio = (u32(t, EMPTY_MASK) >> snd) & 1 or u32(t, AUDIO_LEN + snd * 0x10)
    return not has_audio and not u8(t, SOUND_BASE + snd * SOUND_STRIDE + LOST_OFF)


def load_plan(t, folder, index):
    """Checks + prep (no halt) for loading file `index` of `folder` (0 project,
    1 /Wavs, 2 /Recs) into the CURRENT sound. Returns (func, args, name, fixup):
    inject func(*args) at the idle loop; if fixup, the sound was empty and the
    folder change reset its cursor, so call fix_cursor() once that's done.
    Same folder: browse by delta (the tested path). Other folder: cursor[F] =
    index, then the panel's folder-button call loads it."""
    snd, cur_folder, _, cursor, sd = status(t)
    if folder not in FOLDERS:
        raise ValueError(f"unknown folder {folder}")
    count = folder_count(t, folder)
    if not 0 <= index < count:
        raise ValueError(f"index {index} out of range (folder has {count} file(s))")
    if sd in (1, 3):
        raise ValueError("SD busy" if sd == 1 else "SD error / no card")
    name = file_names(t, folder, count)[index]
    if folder == cur_folder:
        return BROWSE_LOAD_FN, [BROWSER_UI, index - cursor], name, False
    t.write_memory(CURSORS + (folder * 8 + snd) * 4, index)
    return SET_FOLDER_FN, [BROWSER_UI, folder], name, sound_is_empty(t, snd)


def fix_cursor(t, snd, folder, index, timeout=10.0):
    """After a folder change on an empty sound (it loaded file 0 / the newest
    Rec): wait for that load to finish, then load `index`. The cursor write and
    call happen in ONE halt at the idle loop, so the first call is surely done.
    Returns True if a second load was injected."""
    t0 = time.time()
    time.sleep(0.05)
    while time.time() - t0 < timeout:
        if u8(t, SOUND_BASE + snd * SOUND_STRIDE + SRC_OFF) == folder and u32(t, SD_STATE) != 1:
            break
        time.sleep(0.02)
    xpsr = wait_idle_and_halt(t)
    if xpsr is None:
        raise RuntimeError("couldn't catch the CPU in the idle loop for the cursor fix")
    if i32(t, CURSORS + (folder * 8 + snd) * 4) == index or u8(t, CUR_SOUND) != snd:
        t.resume()
        return False
    t.write_memory(CURSORS + (folder * 8 + snd) * 4, index)
    call_returning_to_idle(t, xpsr, BROWSE_LOAD_FN, [BROWSER_UI, 0])
    return True


def write8(t, addr, v, volatile=False, tries=3):
    """1-byte write while the CPU runs. The ST-Link reads each byte back to verify;
    if the firmware changes that byte in between, it reports 'Write verification
    error' though our write went out. volatile=True: the firmware also writes this
    byte (flags), so that's fine. Otherwise confirm by reading back, retry."""
    from pyocd.core.exceptions import ProbeError
    for i in range(tries):
        try:
            t.write_memory(addr, v, 8)
            return
        except ProbeError as e:
            if "verification" not in str(e):
                raise
            if volatile or u8(t, addr) == v:
                return
    raise RuntimeError(f"write 0x{addr:08x} = {v} didn't stick after {tries} tries")


def select_nohalt(t, n):
    """Select sound n without halting (no audio glitch).

    Mirrors FUN_08011980 minus the UI page's 'sound changed' vtable call
    (+0x40), which tested unnecessary: LEDs + knobs follow anyway (2026-10-11).
    Also does the notify's other step: engine state +0x11 = +0x08.
    """
    write8(t, CUR_SOUND, n)
    write8(t, STATE + 0x11, u8(t, STATE + 0x08), volatile=True)


def post_event_nohalt(t, n, timeout=0.5):
    """Post engine event n by writing the events word while the CPU RUNS.

    The firmware posts with an atomic |= and the engine fetch-and-clears it each
    tick, so it is almost always 0. We only write when it reads 0 (so we can't
    clobber another pending event), then confirm the engine consumed it.
    """
    bit = 1 << n
    t0 = time.time()
    while time.time() - t0 < timeout:
        if u32(t, EVENTS) == 0:
            t.write_memory(EVENTS, bit)
            while time.time() - t0 < timeout:
                if not u32(t, EVENTS) & bit:
                    return True
                time.sleep(0.001)
            return False
        time.sleep(0.001)
    return False


def wait_idle_and_halt(t, tries=200):
    """Halt only when the core is in main()'s idle loop, in thread mode.
    Returns the saved xPSR (truthy) or None."""
    if hasattr(t, "halt_in"):                # gv_pico.PicoTarget: the loop runs on the Pico
        r = t.halt_in(IDLE_LO, IDLE_HI, tries)
        return r[1] | (1 << 24) if r else None
    for _ in range(tries):
        t.halt()
        pc, xpsr = t.read_core_registers_raw(["pc", "xpsr"])
        if IDLE_LO <= pc <= IDLE_HI and (xpsr & 0x1FF) == 0:
            return xpsr | (1 << 24)
        t.resume()
        time.sleep(0.003)
    return None


def call_returning_to_idle(t, xpsr, func, args):
    """One-halt call: with the core halted in main()'s idle loop, point PC at
    func and LR back at the top of the idle loop, then resume. The idle loop
    keeps nothing in r0-r3/r12 and recomputes flags, and func preserves
    r4-r11/sp (AAPCS), so when func returns the loop just carries on - no
    second halt, nothing to restore."""
    names = ["r%d" % i for i in range(len(args))] + ["lr", "pc", "xpsr"]
    vals = [v & 0xFFFFFFFF for v in args] + [IDLE_LO | 1, func | 1, xpsr]
    t.write_core_registers_raw(names, vals)
    t.resume()


def fname_field(t, snd, folder):
    a = SOUND_BASE + snd * SOUND_STRIDE + FNAME_OFF[folder]
    return bytes(t.read_memory_block8(a, 0x100)).split(b"\0", 1)[0].decode("latin-1")


def main():
    ap = argparse.ArgumentParser(description="Load a WAV into the selected sound.")
    ap.add_argument("index", type=int, nargs="?",
                    help="file index in the selected sound's folder (omit = status)")
    ap.add_argument("--sound", type=int, choices=range(1, 9), metavar="1-8",
                    help="select this sound first = edit focus, playback untouched "
                         "(front-panel numbering)")
    ap.add_argument("--halt-select", action="store_true",
                    help="select via the firmware setter call (halts = audio glitch)")
    ap.add_argument("--halt-load", action="store_true",
                    help="old load path: halt + wait for return (longer glitch)")
    ap.add_argument("--play", action="store_true",
                    help="also switch playback to the selected sound (engine event 3)")
    ap.add_argument("--folder", choices=["project", "wavs", "recs"],
                    help="list/load from this folder (default: the sound's current one)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--timeout", type=float, default=30.0)
    ap.add_argument("--freq", type=int, default=4_000_000)
    a = ap.parse_args()

    session = connect(a.freq)
    try:
        t = session.target
        current = u8(t, CUR_SOUND)
        target_snd = current if a.sound is None else a.sound - 1
        if a.sound is not None and target_snd != current:
            if a.dry_run:
                print(f"DRY RUN - would select Sound {target_snd + 1} (currently {current + 1})")
            elif a.halt_select:
                if not wait_idle_and_halt(t):
                    sys.exit("Couldn't catch the CPU in the idle loop - nothing called.")
                swd_call(t, SELECT_SOUND_FN, [target_snd], 0x08000000, 5.0, lean=True)
                time.sleep(0.1)
            else:
                select_nohalt(t, target_snd)
                time.sleep(0.02)
            if not a.dry_run:
                now = u8(t, CUR_SOUND)
                if now != target_snd:
                    sys.exit(f"Select failed: current sound is {now + 1}, wanted {target_snd + 1}.")
                print(f"Selected Sound {target_snd + 1}.")

        if a.play:
            playing = u32(t, PLAYING)
            if a.dry_run:
                print(f"DRY RUN - would post event {EV_PLAY_SELECTED} "
                      f"(playing now Sound {playing + 1})")
            elif post_event_nohalt(t, EV_PLAY_SELECTED):
                time.sleep(0.05)
                now = u32(t, PLAYING)
                print(f"Playing: Sound {playing + 1} -> Sound {now + 1}  (no halt)"
                      + ("" if now == target_snd else "   (did NOT follow selection)"))
            else:
                print("  event not consumed in time - playback not switched.")

        snd, folder, count, cursor, sd = status(t, target_snd)
        if folder not in FOLDERS:
            sys.exit(f"Sound {snd + 1}: unknown source byte {folder} - not touching it.")
        if a.folder and ["project", "wavs", "recs"].index(a.folder) != folder:
            return load_other_folder(t, a, snd, ["project", "wavs", "recs"].index(a.folder))
        names = file_names(t, folder, count)
        print(f"Sound {snd + 1}   source: {FOLDERS[folder]}   "
              f"{count} file(s)   SD state: {sd}")
        for i, n in enumerate(names):
            print(f"  {'>' if i == cursor else ' '}[{i:3d}] {n}")

        if a.index is None:
            return
        if not 0 <= a.index < count:
            sys.exit(f"index {a.index} out of range 0..{count - 1}")
        if sd in (1, 3):
            sys.exit(f"SD state is {sd} ({'busy' if sd == 1 else 'error/no card'}) - try again.")
        delta = a.index - cursor
        print(f"\nPlan: Sound {snd + 1} <- [{a.index}] {names[a.index]}  "
              f"via 0x{BROWSE_LOAD_FN:08x}(0x{BROWSER_UI:08x}, {delta:+d})")
        if a.dry_run:
            print("DRY RUN - nothing called.")
            return

        if a.halt_load:
            if not wait_idle_and_halt(t):
                sys.exit("Couldn't catch the CPU in the idle loop - nothing called.")
            ret = swd_call(t, BROWSE_LOAD_FN, [BROWSER_UI, delta & 0xFFFFFFFF],
                           0x08000000, a.timeout, lean=True)
            time.sleep(0.2)
            snd2, folder2, _, cursor2, sd2 = status(t)
            print(f"\n{'LOADED' if ret == 1 else 'FAILED'} (r0={ret})  "
                  f"cursor now {cursor2}, SD state {sd2}")
            return

        t0 = time.time()
        xpsr = wait_idle_and_halt(t)
        if xpsr is None:
            sys.exit("Couldn't catch the CPU in the idle loop - nothing called.")
        call_returning_to_idle(t, xpsr, BROWSE_LOAD_FN, [BROWSER_UI, delta])
        halted_ms = (time.time() - t0) * 1000
        # wait for it to finish, without halting: cursor moved, SD idle, and
        # the sound's filename now matches
        want = names[a.index]
        while time.time() - t0 < a.timeout:
            _, _, _, cursor2, sd2 = status(t, snd)
            if cursor2 == a.index and sd2 == 0 and fname_field(t, snd, folder) == want:
                print(f"\nLOADED {want} into Sound {snd + 1}  "
                      f"(one halt, ~{halted_ms:.0f} ms incl. idle catch; "
                      f"done after {(time.time() - t0) * 1000:.0f} ms)")
                return
            time.sleep(0.01)
        print(f"\nNOT CONFIRMED after {a.timeout:.0f}s: cursor {cursor2}, SD state {sd2}, "
              f"filename '{fname_field(t, snd, folder)}' (file may be invalid/unsupported)")
    finally:
        session.close()


def load_other_folder(t, a, snd, folder):
    """--folder that isn't the sound's current one: list it, and load via the
    panel's folder-button call (load_plan / fix_cursor)."""
    count = folder_count(t, folder)
    cursor = i32(t, CURSORS + (folder * 8 + snd) * 4)
    print(f"Sound {snd + 1}   folder: {FOLDERS[folder]} (sound is on "
          f"{FOLDERS[u8(t, SOUND_BASE + snd * SOUND_STRIDE + SRC_OFF)]})   {count} file(s)")
    for i, n in enumerate(file_names(t, folder, count)):
        print(f"  {'>' if i == cursor else ' '}[{i:3d}] {n}")
    if a.index is None:
        return
    if a.dry_run:
        print(f"\nDRY RUN - would set cursor and call 0x{SET_FOLDER_FN:08x}"
              f"(0x{BROWSER_UI:08x}, {folder})"
              + ("  (sound is EMPTY: it gets reset, then a 2nd load)" if sound_is_empty(t, snd) else ""))
        return
    if u8(t, CUR_SOUND) != snd:
        sys.exit("Selected sound changed - not loading.")
    try:
        func, args, name, fixup = load_plan(t, folder, a.index)
    except ValueError as e:
        sys.exit(str(e))
    t0 = time.time()
    xpsr = wait_idle_and_halt(t)
    if xpsr is None:
        sys.exit("Couldn't catch the CPU in the idle loop - nothing called.")
    call_returning_to_idle(t, xpsr, func, args)
    if fixup and fix_cursor(t, snd, folder, a.index):
        print("  (sound was empty: loaded twice to land on the right file)")
    while time.time() - t0 < a.timeout:
        _, f2, _, c2, sd2 = status(t, snd)
        if f2 == folder and c2 == a.index and sd2 == 0 and fname_field(t, snd, folder) == name:
            print(f"\nLOADED {name} from {FOLDERS[folder]} into Sound {snd + 1}  "
                  f"(done after {(time.time() - t0) * 1000:.0f} ms)")
            return
        time.sleep(0.01)
    _, f2, _, c2, sd2 = status(t, snd)
    print(f"\nNOT CONFIRMED: folder {f2}, cursor {c2}, SD state {sd2}, "
          f"filename '{fname_field(t, snd, f2) if f2 in FOLDERS else '?'}'")


if __name__ == "__main__":
    main()
