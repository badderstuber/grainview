#!/usr/bin/env python3
"""mg_preset.py - presets + projects of the Multigrain over SWD.

RE (1.4.8.0, offline 2026-10-12; preset load hardware-tested 2026-10-11):
    FUN_08012b24(n)          load Preset(n+1).mgp of the current project. A MISSING
                             file blanks all 8 sounds (the panel's "new preset") and
                             the module autosaves that - so: exists-bit check first.
    FUN_08011450(n)          panel's preset save: autosave, then FUN_08021858(n,
                             sounds, collect = settings+0x1d1 == 1, force = 0) ->
                             Preset(n+1).mgp. Refuses (10) if locked.
    FUN_0801e924(n)          toggle the lock: create/delete Preset(n+1).lck
    FUN_08012c54(n, save)    switch to Project(n+1); save=1 (as the panel) writes the
                             outgoing project's Autosave.mgp first. A missing folder
                             gets CREATED as a new empty project -> exists-bit check.
    autosave now             no call: project-changed flag state+0x11 = 1 and tick
                             counter state+0x0c = 10000 -> the UI task saves on its
                             next pass and clears the flag (only on success).
All slots are 0..47 (48 presets = panel's 6 banks x 8 pads; 48 projects).
Bitmaps (u32[2], bit n = slot n): preset exists 0x240312e0, preset locked
0x240312e8 (rebuilt by the project folder scan), project exists 0x240312f4.
Current preset u8 0x24025b18 (> 47 = none), current project u8 0x24025c74 (UI)
and u32 0x20008cc4 (SD folder; path string 0x240332fc) - these two match unless
a firmware "collect" of another project left the SD side elsewhere.

All calls are synchronous in the UI task (they block it while the SD works,
same as from the panel); injected with the same one-halt call as mg_load.py.
Completion is polled without halting.

Usage:
    tools/venv/bin/python tools/mg_preset.py                 # status
    tools/venv/bin/python tools/mg_preset.py 2               # load Preset02
    tools/venv/bin/python tools/mg_preset.py --save 5        # save to Preset05
    tools/venv/bin/python tools/mg_preset.py --lock 5        # toggle Preset05 lock
    tools/venv/bin/python tools/mg_preset.py --project 3     # switch to Project03
    tools/venv/bin/python tools/mg_preset.py --autosave      # save Autosave.mgp now
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from mg_call import connect  # noqa: E402
from mg_load import (wait_idle_and_halt, call_returning_to_idle, write8,  # noqa: E402
                     u8, u32, SD_STATE, STATE)

LOAD_PRESET_FN = 0x08012B24
SAVE_PRESET_FN = 0x08011450
LOCK_PRESET_FN = 0x0801E924
LOAD_PROJECT_FN = 0x08012C54
PRESET_EXISTS = 0x240312E0
PRESET_LOCKED = 0x240312E8
PROJECT_EXISTS = 0x240312F4
CUR_PRESET = 0x24025B18
CUR_PROJECT = 0x24025C74          # UI side
PROJECT = 0x20008CC4              # SD side (folder in use)
PROJECT_PATH = 0x240332FC
AUTOSAVE_TICK = STATE + 0x0C
PROJECT_DIRTY = STATE + 0x11
SLOTS = 48


def bitmap(t, addr):
    lo, hi = t.read_memory_block32(addr, 2)
    v = lo | hi << 32
    return [n for n in range(SLOTS) if v >> n & 1]


def status(t):
    cp = u8(t, CUR_PRESET)
    return {
        "project": u8(t, CUR_PROJECT), "sd_project": u32(t, PROJECT),
        "path": bytes(t.read_memory_block8(PROJECT_PATH, 64)).split(b"\0", 1)[0].decode(),
        "projects": bitmap(t, PROJECT_EXISTS),
        "presets": bitmap(t, PRESET_EXISTS), "locked": bitmap(t, PRESET_LOCKED),
        "preset": cp if cp < SLOTS else None,
        "sd": u32(t, SD_STATE), "dirty": u8(t, PROJECT_DIRTY),
    }


def _check(t, n, need_preset=None):
    """Common guards. Raises ValueError with a user-facing reason."""
    if not 0 <= n < SLOTS:
        raise ValueError(f"slot must be 1..{SLOTS}")
    s = status(t)
    if s["sd"] != 0:
        raise ValueError("SD busy" if s["sd"] == 1 else "SD error / no card")
    if s["project"] != s["sd_project"]:
        raise ValueError(f"project mismatch (UI {s['project'] + 1}, SD {s['sd_project'] + 1})"
                         " - switch project on the module first")
    if need_preset and n not in s["presets"]:
        raise ValueError(f"Preset{n + 1:02d} doesn't exist")
    return s


def _inject(t, func, args):
    xpsr = wait_idle_and_halt(t)
    if xpsr is None:
        raise RuntimeError("couldn't catch the CPU in the idle loop - nothing called")
    call_returning_to_idle(t, xpsr, func, args)


def load_preset(t, n):
    _check(t, n, need_preset=True)
    _inject(t, LOAD_PRESET_FN, [n])


def save_preset(t, n):
    s = _check(t, n)
    if n in s["locked"]:
        raise ValueError(f"Preset{n + 1:02d} is locked")
    _inject(t, SAVE_PRESET_FN, [n])


def toggle_lock(t, n):
    _check(t, n, need_preset=True)
    _inject(t, LOCK_PRESET_FN, [n])


def load_project(t, n):
    s = _check(t, n)
    if n not in s["projects"]:
        raise ValueError(f"Project{n + 1:02d} doesn't exist")
    _inject(t, LOAD_PROJECT_FN, [n, 1])


def autosave_now(t):
    """No halt: the UI task's own autosave, due at once."""
    write8(t, PROJECT_DIRTY, 1, volatile=True)
    t.write_memory(AUTOSAVE_TICK, 10000)


def wait_done(t, ok, timeout=30.0, settle=0.3):
    """Poll (no halt) until ok(status) holds and SD has been idle for `settle` s.
    The injected call runs inside the UI task, so RAM reads see it finish."""
    t0, idle = time.time(), None
    while time.time() - t0 < timeout:
        s = status(t)
        if s["sd"] == 0 and ok(s):
            idle = idle or time.time()
            if time.time() - idle >= settle:
                return s, time.time() - t0
        else:
            idle = None
        time.sleep(0.02)
    return None, timeout


def show(s):
    def row(name, have, extra=lambda n: ""):
        cells = "".join(("#" if n in have else ".") + extra(n) for n in range(SLOTS))
        print(f"  {name:9s}" + " ".join(cells[i:i + 16] for i in range(0, len(cells), 16)))
    print(f"Project{s['project'] + 1:02d}   ({s['path']})   SD state {s['sd']}"
          + ("   [unsaved changes]" if s["dirty"] else ""))
    cur = "-" if s["preset"] is None else "Preset%02d" % (s["preset"] + 1)
    print(f"  current preset: {cur}")
    print(f"  presets:   {' '.join(f'{n + 1:02d}' + ('L' if n in s['locked'] else '') for n in s['presets']) or '-'}")
    print(f"  projects:  {' '.join(f'{n + 1:02d}' for n in s['projects']) or '-'}")


def main():
    ap = argparse.ArgumentParser(description="Presets + projects (slots 1..48).")
    ap.add_argument("preset", type=int, nargs="?", help="load PresetNN (1 = Preset01)")
    ap.add_argument("--save", type=int, metavar="N", help="save to PresetNN (not if locked)")
    ap.add_argument("--lock", type=int, metavar="N", help="toggle PresetNN's lock")
    ap.add_argument("--project", type=int, metavar="N", help="switch to ProjectNN (saves first)")
    ap.add_argument("--autosave", action="store_true", help="write Autosave.mgp now")
    ap.add_argument("--timeout", type=float, default=30.0)
    ap.add_argument("--freq", type=int, default=4_000_000)
    a = ap.parse_args()

    session = connect(a.freq)
    try:
        t = session.target
        s = status(t)
        show(s)
        try:
            if a.preset is not None:
                n = a.preset - 1
                load_preset(t, n)
                done, dt = wait_done(t, lambda s: s["preset"] == n, a.timeout)
            elif a.save is not None:
                n = a.save - 1
                save_preset(t, n)
                done, dt = wait_done(t, lambda s: s["preset"] == n and n in s["presets"], a.timeout)
            elif a.lock is not None:
                n, was = a.lock - 1, a.lock - 1 in s["locked"]
                toggle_lock(t, n)
                done, dt = wait_done(t, lambda s: (n in s["locked"]) != was, a.timeout)
            elif a.project is not None:
                n = a.project - 1
                load_project(t, n)
                done, dt = wait_done(t, lambda s: s["project"] == n == s["sd_project"], a.timeout)
            elif a.autosave:
                autosave_now(t)
                done, dt = wait_done(t, lambda s: not s["dirty"], a.timeout)
            else:
                return
        except ValueError as e:
            sys.exit(str(e))
        print(f"\nDone after {dt * 1000:.0f} ms:" if done else "\nNOT CONFIRMED - check the module:")
        show(done or status(t))
    finally:
        session.close()


if __name__ == "__main__":
    main()
