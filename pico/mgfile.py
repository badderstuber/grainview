# FILE on the Pico: the card's file lists, WAV loads, presets + projects, over SWD (swd.py).
# Ports of the hardware-tested Mac helpers, same checks + messages as grainview_server.py:
#   tools/mg_load.py   load_plan / fix_cursor / wait_idle_and_halt / call_returning_to_idle
#   tools/mg_preset.py load / save / lock a preset, open a project, autosave now
# Every call is injected the same way: halt only in main()'s idle loop, point PC at the
# function and LR back at the loop, resume - one short halt, nothing to restore.
#
#   counts(s)                      {"project": n, "Wavs": n, "Recs": n}
#   files(s, folder=None)          (folder, cursor, names); None = the selected sound's
#   load(s, folder, index)         -> the fix-up job (fix()) or None; raises with the reason
#   fix(s, job)                    True once done (call it every poll until then)
#   preset(s, "load"|"save"|"lock", n) / project(s, "load"|"save", n)
import struct
import time

import mg_map as M
from mgpoll import NAME_PEEK, base, name

IDX = {v: k for k, v in M.FOLDER_NAMES.items()}
FIX_WAIT_MS, FIX_TIMEOUT_MS = 50, 10000


def u8(s, a):
    return s.read_block8(a, 1)[0]


def i32(s, a):
    return struct.unpack("<i", s.read_block8(a, 4))[0]


def bits(s, a):                               # u32[2] bitmap -> slots set
    b = s.read_block8(a, 8)
    return [n for n in range(M.SLOTS) if b[n >> 3] >> (n & 7) & 1]


def count(s, f):
    return min(s.read32(M.COUNTS + f * 4), M.MAX_FILES[f])


def cursor_at(f, snd):
    return M.CURSORS + (f * 8 + snd) * 4


def names(s, f, n):
    """The folder's first n names."""
    if f == 2:                                # /Recs: an int list -> Rec%05d.wav
        return ["Rec%05d.wav" % abs(v)
                for v in struct.unpack("<%di" % n, s.read_block8(M.REC_LIST, n * 4))] if n else []
    out = []
    for i in range(n):
        a = M.LISTS[f] + i * 0x100
        b = s.read_block8(a, NAME_PEEK)
        if b"\0" not in b:
            b = s.read_block8(a, 0x100)
        out.append(name(b))
    return out


def status(s):
    snd = u8(s, M.CUR_SOUND)
    return snd, u8(s, base(snd) + M.SRC_OFF), s.read32(M.SD_STATE)


def counts(s):
    return {M.FOLDER_NAMES[f]: count(s, f) for f in M.FOLDER_NAMES}


def files(s, folder=None):
    snd, cur, _ = status(s)
    f = cur if folder is None else IDX[folder]
    if f not in M.FOLDER_NAMES:
        raise ValueError("unknown source byte %d" % f)
    return M.FOLDER_NAMES[f], i32(s, cursor_at(f, snd)), names(s, f, count(s, f))


# ---- one-halt calls ----

def call(s, xpsr, func, args):
    """Core halted in the idle loop: run func(*args), returning into the loop."""
    try:
        for i, v in enumerate(args):
            s.write_reg(i, v & 0xFFFFFFFF)
        s.write_reg(14, M.IDLE_LO | 1)        # lr
        s.write_reg(15, func | 1)             # pc (Thumb)
        s.write_reg(16, xpsr | 1 << 24)
    finally:
        s.resume()                            # never leave the module halted


def halt_idle(s):
    r = s.halt_in(M.IDLE_LO, M.IDLE_HI, 200)
    if r is None:
        raise RuntimeError("couldn't catch the CPU in the idle loop - nothing called")
    return r[1]


def inject(s, func, args):
    call(s, halt_idle(s), func, args)


def sound_is_empty(s, snd):
    """FUN_0803e91c resets an empty sound before a folder change (mg_load.sound_is_empty)."""
    audio = s.read32(M.EMPTY_MASK) >> snd & 1 or s.read32(M.AUDIO_LEN + snd * 0x10)
    return not audio and not u8(s, base(snd) + M.LOST_OFF)


def load(s, folder, index):
    """File index of folder (None = the sound's own) -> the selected sound. Same folder:
    browse by delta; another: cursor = index, then the panel's folder-button call (the sound
    switches folder). An empty sound gets reset by that and loads file 0: then the returned
    job loads index once that's done (fix())."""
    snd, cur, sd = status(s)
    if cur not in M.FOLDER_NAMES:
        raise ValueError("unknown source byte %d" % cur)
    f = cur if folder is None else IDX[folder]
    n = count(s, f)
    if not 0 <= index < n:
        raise ValueError("index %d out of range (folder has %d file(s))" % (index, n))
    if sd in (1, 3):
        raise ValueError("SD busy" if sd == 1 else "SD error / no card")
    if f == cur:
        inject(s, M.BROWSE_LOAD_FN, (M.BROWSER_UI, index - i32(s, cursor_at(f, snd))))
        return None
    s.write32(cursor_at(f, snd), index)
    job = (snd, f, index, time.ticks_ms()) if sound_is_empty(s, snd) else None
    inject(s, M.SET_FOLDER_FN, (M.BROWSER_UI, f))
    return job


def fix(s, job):
    """mg_load.fix_cursor without the blocking wait: False until the first load is done
    (the sound on its new folder, SD not busy) or FIX_TIMEOUT_MS passed, then the cursor
    write + browse load in one halt (skipped if it landed right, or the sound changed)."""
    snd, f, index, t0 = job
    dt = time.ticks_diff(time.ticks_ms(), t0)
    if dt < FIX_WAIT_MS or dt < FIX_TIMEOUT_MS and not (
            u8(s, base(snd) + M.SRC_OFF) == f and s.read32(M.SD_STATE) != 1):
        return False
    xpsr = halt_idle(s)
    try:
        if i32(s, cursor_at(f, snd)) != index and u8(s, M.CUR_SOUND) == snd:
            s.write32(cursor_at(f, snd), index)
            call(s, xpsr, M.BROWSE_LOAD_FN, (M.BROWSER_UI, 0))
    finally:
        s.resume()                            # (a no-op once call() resumed)
    return True


# ---- presets + projects (mg_preset.py) ----

def check(s, n, need_preset=False):
    if not 0 <= n < M.SLOTS:
        raise ValueError("slot must be 1..%d" % M.SLOTS)
    sd = s.read32(M.SD_STATE)
    if sd != 0:
        raise ValueError("SD busy" if sd == 1 else "SD error / no card")
    ui, card = u8(s, M.CUR_PROJECT), s.read32(M.SD_PROJECT)
    if ui != card:
        raise ValueError("project mismatch (UI %d, SD %d) - switch project on the module first"
                         % (ui + 1, card + 1))
    if need_preset and n not in bits(s, M.PRESET_EXISTS):
        raise ValueError("Preset%02d doesn't exist" % (n + 1))


def preset(s, action, n):
    if action == "load":                      # a missing file would blank all 8 sounds
        check(s, n, True)
        inject(s, M.LOAD_PRESET_FN, (n,))
    elif action == "save":
        check(s, n)
        if n in bits(s, M.PRESET_LOCKED):
            raise ValueError("Preset%02d is locked" % (n + 1))
        inject(s, M.SAVE_PRESET_FN, (n,))
    elif action == "lock":
        check(s, n, True)
        inject(s, M.LOCK_PRESET_FN, (n,))
    else:
        raise ValueError("action must be load, save or lock")


def project(s, action, n):
    if action == "save":                      # no halt: the UI task's autosave, due now
        s.write8(M.PROJECT_DIRTY, 1)
        s.write32(M.AUTOSAVE_TICK, 10000)
    elif action == "load":                    # a missing one would be created empty
        check(s, n)
        if n not in bits(s, M.PROJECT_EXISTS):
            raise ValueError("Project%02d doesn't exist" % (n + 1))
        inject(s, M.LOAD_PROJECT_FN, (n, 1))  # 1 = save the outgoing project first
    else:
        raise ValueError("action must be load or save")
