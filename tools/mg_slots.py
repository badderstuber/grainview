#!/usr/bin/env python3
"""mg_slots.py - which file is loaded in each of the Multigrain's 8 sounds.

Read-only, plain RAM reads while the module runs (no halt, no glitch).

RE (1.4.8.0, offsets shared with mg_load.py): sound struct N at
0x24020b84 + N*0x9f0 holds a source u8 @ +0x59c (0=project folder, 1=/Wavs,
2=/Recs) and one filename field per source (+0x7dc / +0x6c8 / +0x5b4, 0x100
bytes, NUL-terminated). Only the field for the current source is meaningful.
u8 @ +0x4f4 is shown raw: believed to be a "file missing" flag (unverified).

Usage:
    tools/venv/bin/python tools/mg_slots.py          # table
    tools/venv/bin/python tools/mg_slots.py --json   # for the app/API
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from mg_peek import connect  # noqa: E402
from mg_load import (CUR_SOUND, CURSORS, FOLDERS, PLAYING, SOUND_BASE,  # noqa: E402
                     SOUND_STRIDE, SRC_OFF, fname_field, i32, u8, u32)

MISSING_OFF = 0x4F4
SHORT = {0: "project", 1: "Wavs", 2: "Recs"}


def slots(t):
    sel, play = u8(t, CUR_SOUND), u32(t, PLAYING)
    out = []
    for snd in range(8):
        base = SOUND_BASE + snd * SOUND_STRIDE
        folder = u8(t, base + SRC_OFF)
        known = folder in FOLDERS
        out.append({
            "sound": snd + 1,
            "selected": snd == sel,
            "playing": snd == play,
            "source": folder,
            "folder": SHORT.get(folder),
            "file": fname_field(t, snd, folder) if known else None,
            "cursor": i32(t, CURSORS + (folder * 8 + snd) * 4) if known else None,
            "flag_4f4": u8(t, base + MISSING_OFF),
        })
    return out


def main():
    ap = argparse.ArgumentParser(description="Show the file loaded in each sound.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--freq", type=int, default=4_000_000)
    a = ap.parse_args()

    session = connect(a.freq)
    try:
        rows = slots(session.target)
    finally:
        session.close()
    if a.json:
        print(json.dumps(rows, indent=1))
        return
    print("     S P  folder   cur  4f4  file")
    for r in rows:
        print(f"  {r['sound']}  {'*' if r['selected'] else ' '} {'>' if r['playing'] else ' '}  "
              f"{r['folder'] or '?%d' % r['source']:7} {r['cursor'] if r['cursor'] is not None else '-':>4}"
              f"  {r['flag_4f4']:3}  {r['file'] or '(empty)'}")
    print("  S = selected (edit focus), P = playing")


if __name__ == "__main__":
    main()
