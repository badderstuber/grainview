#!/usr/bin/env python3
"""mg_sd.py - read the Multigrain's /Wavs file list over SWD (card stays in the
module). The firmware scans /Multigrain/Wavs into RAM; we read that list:

    count     : u32 at 0x240272d8
    filenames : 0x100-byte entries at 0x30008800 (up to 128), NUL-terminated

Optionally re-run the firmware's directory scan first (FUN_0801f0d4, no args -
proven safe) to pick up card changes.

Usage:
    tools/venv/bin/python tools/mg_sd.py            # read current list
    tools/venv/bin/python tools/mg_sd.py --rescan   # call dir-scan, then read
"""
import argparse
import sys

COUNT_ADDR = 0x240272D8
NAMES_BASE = 0x30008800
ENTRY = 0x100
MAX_FILES = 128
DIRSCAN_FN = 0x0801F0D4


def connect(freq):
    from pyocd.core.helpers import ConnectHelper
    s = ConnectHelper.session_with_chosen_probe(
        blocking=False,
        options={"target_override": "cortex_m", "connect_mode": "attach",
                 "frequency": freq, "resume_on_disconnect": True})
    if s is None:
        sys.exit("No ST-Link found. Plug it in and power the module.")
    s.open()
    return s


def read_list(target):
    count = target.read_memory(COUNT_ADDR)
    if count > MAX_FILES:
        print(f"  (count={count} looks wrong; clamping to {MAX_FILES})")
        count = MAX_FILES
    files = []
    for i in range(count):
        raw = bytes(target.read_memory_block8(NAMES_BASE + i * ENTRY, ENTRY))
        name = raw.split(b"\x00", 1)[0].decode("latin-1", "replace")
        files.append(name)
    return count, files


def main():
    ap = argparse.ArgumentParser(description="Read Multigrain /Wavs list over SWD.")
    ap.add_argument("--rescan", action="store_true",
                    help="call the firmware dir-scan first (FUN_0801f0d4)")
    ap.add_argument("--freq", type=int, default=4_000_000)
    a = ap.parse_args()

    session = connect(a.freq)
    try:
        target = session.target
        if a.rescan:
            from mg_call import swd_call   # reuse the function-call helper
            print("rescanning card (FUN_0801f0d4)...")
            swd_call(target, DIRSCAN_FN, [], 0x08000000, 8.0)
        count, files = read_list(target)
        print(f"\n/Multigrain/Wavs - {count} file(s):")
        for i, name in enumerate(files):
            print(f"  [{i:3}] {name}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
