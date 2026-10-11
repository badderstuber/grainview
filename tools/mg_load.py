#!/usr/bin/env python3
"""mg_load.py - load a WAV into the Multigrain's SELECTED sound over SWD.

Drives the firmware's own front-panel file-browse routine (what turning the
encoder in file mode does), so the sample loads AND the sound's filename param
is updated via its setter (project saves it). RE notes, all from 1.4.8.0:

    FUN_0803e710(ui, delta)  browse+load: cursor += delta (clamped), load that
                             file into the current sound; filename set only
                             on success. Returns 1 ok / 0 fail.
    current sound            u8  @ 0x24025b30
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
"""
import argparse
import os
import struct
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from mg_call import connect, swd_call  # noqa: E402

BROWSE_LOAD_FN = 0x0803E710
BROWSER_UI = 0x240452C8      # r0 the UI passes (file-browser screen object)
CUR_SOUND = 0x24025B30
SOUND_BASE = 0x24020B84
SOUND_STRIDE = 0x9F0
SRC_OFF = 0x59C
COUNTS = 0x240272D4
LISTS = {0: 0x30000800, 1: 0x30008800}
REC_LIST = 0x30010800
CURSORS = 0x24033344
SD_STATE = 0x20008CCC
IDLE_LO, IDLE_HI = 0x0800BA9A, 0x0800BAA0
FOLDERS = {0: "project folder", 1: "/Multigrain/Wavs", 2: "/Multigrain/Recs"}
MAX_FILES = 128


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
    nums = [i32(t, REC_LIST + i * 4) for i in range(count)]
    return ["Rec%05d.wav" % abs(n) for n in nums]


def status(t):
    snd = u8(t, CUR_SOUND)
    folder = u8(t, SOUND_BASE + snd * SOUND_STRIDE + SRC_OFF)
    count = u32(t, COUNTS + folder * 4) if folder in FOLDERS else 0
    cursor = i32(t, CURSORS + (folder * 8 + snd) * 4) if folder in FOLDERS else 0
    sd = u32(t, SD_STATE)
    return snd, folder, min(count, MAX_FILES), cursor, sd


def wait_idle_and_halt(t, tries=200):
    """Halt only when the core is in main()'s idle loop, in thread mode."""
    for _ in range(tries):
        t.halt()
        pc = t.read_core_register("pc")
        ipsr = t.read_core_register("xpsr") & 0x1FF
        if IDLE_LO <= pc <= IDLE_HI and ipsr == 0:
            return True
        t.resume()
        time.sleep(0.003)
    return False


def main():
    ap = argparse.ArgumentParser(description="Load a WAV into the selected sound.")
    ap.add_argument("index", type=int, nargs="?",
                    help="file index in the selected sound's folder (omit = status)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--timeout", type=float, default=30.0)
    ap.add_argument("--freq", type=int, default=4_000_000)
    a = ap.parse_args()

    session = connect(a.freq)
    try:
        t = session.target
        snd, folder, count, cursor, sd = status(t)
        if folder not in FOLDERS:
            sys.exit(f"Sound {snd + 1}: unknown source byte {folder} - not touching it.")
        names = file_names(t, folder, count)
        print(f"Selected: Sound {snd + 1}   source: {FOLDERS[folder]}   "
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

        if not wait_idle_and_halt(t):
            sys.exit("Couldn't catch the CPU in the idle loop - module left running, nothing called.")
        ret = swd_call(t, BROWSE_LOAD_FN, [BROWSER_UI, delta & 0xFFFFFFFF], 0x08000000, a.timeout)
        time.sleep(0.2)
        snd2, folder2, _, cursor2, sd2 = status(t)
        ok = ret == 1
        print(f"\n{'LOADED' if ok else 'FAILED'} (r0={ret})  "
              f"cursor now {cursor2}, SD state {sd2}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
