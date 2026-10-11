#!/usr/bin/env python3
"""mg_pcsample.py - where is the Multigrain's CPU spending its time? (no halt)

Samples the DWT program-counter sample register (DWT_PCSR, 0xE000101C) over SWD
while the firmware runs, then prints a histogram of PCs with a disassembly of
the hottest spot from Multigrain.1.4.8.0.bin. Use it to see what a hung/stuck
module is spinning on.

Usage:
    tools/venv/bin/python tools/mg_pcsample.py            # 500 samples
    tools/venv/bin/python tools/mg_pcsample.py -n 2000 --top 20
"""
import argparse
import collections
import os
import sys

DWT_PCSR = 0xE000101C
FLASH_BASE = 0x08000000
BIN = os.path.join(os.path.dirname(__file__), "..", "Multigrain.1.4.8.0.bin")

sys.path.insert(0, os.path.dirname(__file__))
from mg_peek import connect  # noqa: E402


def disasm(addr, before=0x20, after=0x20):
    try:
        import capstone
    except ImportError:
        return "  (capstone not installed - no disassembly)"
    data = open(BIN, "rb").read()
    start = (addr - before) & ~1
    off = start - FLASH_BASE
    if not 0 <= off < len(data):
        return f"  (0x{addr:08x} is outside flash - RAM code or bad sample)"
    md = capstone.Cs(capstone.CS_ARCH_ARM,
                     capstone.CS_MODE_THUMB | capstone.CS_MODE_MCLASS)
    lines = []
    for i in md.disasm(data[off:off + before + after], start):
        mark = "=>" if i.address <= addr < i.address + i.size else "  "
        lines.append(f"  {mark} {i.address:08x}  {i.mnemonic:8} {i.op_str}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Sample the running PC (no halt).")
    ap.add_argument("-n", type=int, default=500, help="number of samples")
    ap.add_argument("--top", type=int, default=10, help="how many PCs to list")
    ap.add_argument("--freq", type=int, default=4_000_000)
    args = ap.parse_args()

    session = connect(args.freq)
    try:
        target = session.board.target
        counts = collections.Counter(
            target.read_memory(DWT_PCSR) for _ in range(args.n))
    finally:
        session.close()

    print(f"{args.n} samples, {len(counts)} distinct PCs:")
    for pc, c in counts.most_common(args.top):
        print(f"  0x{pc:08x}  {c:5d}  {100 * c / args.n:5.1f}%")
    hot = counts.most_common(1)[0][0]
    if hot in (0, 0xFFFFFFFF):
        print("\nPCSR unreadable (core halted/sleeping or DWT off).")
        return
    print(f"\nhottest 0x{hot:08x}:")
    print(disasm(hot))


if __name__ == "__main__":
    main()
