#!/usr/bin/env python3
"""mg_preset.py - load PresetNN.mgp of the current project over SWD.

RE (1.4.8.0): FUN_08012b24(n) -> FUN_08026754 opens Preset%02d.mgp with n+1 in
the current project folder, deserializes it, then (re)loads every sound's WAV.
Current project index u32 @ 0x20008cc4 (folder Project%02d = n+1).

!! The preset FILE MUST EXIST. Loading a missing one clears the project's sounds
!! and the module autosaves that blank state (2026-10-11 incident; recover by
!! loading a real preset from the panel). Check the card first.

Same one-halt call as mg_load.py: halt in main's idle loop, PC -> function,
LR -> idle loop, resume; no second halt. Completion is polled without halting.

Usage:
    tools/venv/bin/python tools/mg_preset.py            # show current project
    tools/venv/bin/python tools/mg_preset.py 2          # load Preset02.mgp
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from mg_call import connect  # noqa: E402
from mg_load import wait_idle_and_halt, call_returning_to_idle, SD_STATE  # noqa: E402

LOAD_PRESET_FN = 0x08012B24
PROJECT = 0x20008CC4
PROJECT_PATH = 0x240332FC


def main():
    ap = argparse.ArgumentParser(description="Load PresetNN.mgp (must exist!).")
    ap.add_argument("preset", type=int, nargs="?", help="preset number as on the card (1 = Preset01)")
    ap.add_argument("--timeout", type=float, default=30.0)
    ap.add_argument("--freq", type=int, default=4_000_000)
    a = ap.parse_args()

    session = connect(a.freq)
    try:
        t = session.target
        proj = t.read_memory(PROJECT)
        path = bytes(t.read_memory_block8(PROJECT_PATH, 64)).split(b"\0", 1)[0].decode()
        print(f"Current project: Project{proj + 1:02d}   ({path})")
        if a.preset is None:
            return
        if not 1 <= a.preset <= 99:
            sys.exit("preset must be 1..99")
        if t.read_memory(SD_STATE) in (1, 3):
            sys.exit("SD busy/error - try again.")
        print(f"Loading {path}/Preset{a.preset:02d}.mgp ...")
        t0 = time.time()
        xpsr = wait_idle_and_halt(t)
        if xpsr is None:
            sys.exit("Couldn't catch the CPU in the idle loop - nothing called.")
        call_returning_to_idle(t, xpsr, LOAD_PRESET_FN, [a.preset - 1])
        halted_ms = (time.time() - t0) * 1000
        # done when SD has been idle for a little while (preset + WAV reads)
        idle_since = None
        while time.time() - t0 < a.timeout:
            busy = t.read_memory(SD_STATE) != 0
            if busy:
                idle_since = None
            elif idle_since is None:
                idle_since = time.time()
            elif time.time() - idle_since > 0.5 and time.time() - t0 > 1.0:
                print(f"Done (one halt ~{halted_ms:.0f} ms; SD idle after "
                      f"{(idle_since - t0) * 1000:.0f} ms). Check the module.")
                return
            time.sleep(0.02)
        print("SD never settled - check the module.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
