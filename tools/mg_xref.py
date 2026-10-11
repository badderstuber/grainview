#!/usr/bin/env python3
"""mg_xref.py - offline cross-references in Multigrain.1.4.8.0.bin (no Ghidra).

Finds Thumb-2 BL / B.W branches to an address, and literal-pool words that hold
it (string / data / function-pointer refs). For each hit, prints the enclosing
function start (nearest preceding PUSH {..., lr}).

Usage:
    tools/venv/bin/python tools/mg_xref.py 0x0801fb94          # who calls it?
    tools/venv/bin/python tools/mg_xref.py 0x0805c840 --lit    # who uses this string?
    tools/venv/bin/python tools/mg_xref.py 0x0801fb94 --dis 40 # + disasm around each call
"""
import argparse
import os
import struct

BASE = 0x08000000
BIN = os.path.join(os.path.dirname(__file__), "..", "Multigrain.1.4.8.0.bin")
DATA = open(BIN, "rb").read()


def bl_target(pc, hw1, hw2):
    """Decode a 32-bit Thumb BL (or B.W) at pc; return target or None."""
    if (hw1 & 0xF800) != 0xF000 or (hw2 & 0xD000) not in (0xD000, 0x9000):
        return None
    s = (hw1 >> 10) & 1
    imm10 = hw1 & 0x3FF
    j1 = (hw2 >> 13) & 1
    j2 = (hw2 >> 11) & 1
    imm11 = hw2 & 0x7FF
    i1 = 1 - (j1 ^ s)
    i2 = 1 - (j2 ^ s)
    off = (s << 24) | (i1 << 23) | (i2 << 22) | (imm10 << 12) | (imm11 << 1)
    if s:
        off -= 1 << 25
    return pc + 4 + off


def branch_refs(target):
    hits = []
    for o in range(0, len(DATA) - 4, 2):
        hw1, hw2 = struct.unpack_from("<HH", DATA, o)
        t = bl_target(BASE + o, hw1, hw2)
        if t == target:
            kind = "BL" if hw2 & 0x4000 else "B.W"
            hits.append((BASE + o, kind))
    return hits


def literal_refs(value):
    hits = []
    for v in (value, value | 1):
        p = struct.pack("<I", v)
        i = DATA.find(p)
        while i != -1:
            if i % 4 == 0:
                hits.append((BASE + i, "LIT"))
            i = DATA.find(p, i + 1)
    return sorted(set(hits))


def func_start(addr, limit=0x2000):
    """Nearest preceding 'push {..., lr}' (16-bit B5xx or 32-bit E92D 4xxx)."""
    o = addr - BASE
    for back in range(0, limit, 2):
        p = o - back
        if p < 0:
            break
        hw = struct.unpack_from("<H", DATA, p)[0]
        if (hw & 0xFF00) == 0xB500:
            return BASE + p
        if hw == 0xE92D and p + 4 <= len(DATA):
            if struct.unpack_from("<H", DATA, p + 2)[0] & 0x4000:
                return BASE + p
    return None


def disasm(addr, before, after=8):
    import capstone
    md = capstone.Cs(capstone.CS_ARCH_ARM,
                     capstone.CS_MODE_THUMB | capstone.CS_MODE_MCLASS)
    start = addr - before
    out = []
    for i in md.disasm(DATA[start - BASE:addr - BASE + after], start):
        mark = "=>" if i.address == addr else "  "
        out.append(f"    {mark} {i.address:08x}  {i.mnemonic:8} {i.op_str}")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Offline xrefs in the Multigrain .bin")
    ap.add_argument("addr", type=lambda s: int(s, 0))
    ap.add_argument("--lit", action="store_true", help="literal-pool refs only")
    ap.add_argument("--dis", type=int, metavar="BYTES",
                    help="disassemble BYTES before each branch hit")
    args = ap.parse_args()

    hits = [] if args.lit else branch_refs(args.addr & ~1)
    hits += literal_refs(args.addr & ~1)
    print(f"{len(hits)} ref(s) to 0x{args.addr:08x}:")
    for a, kind in hits:
        fs = func_start(a)
        fs_s = f"in FUN_{fs:08x}" if fs else "in ?"
        print(f"  {kind:4} @ 0x{a:08x}  {fs_s}")
        if args.dis and kind != "LIT":
            print(disasm(a, args.dis))


if __name__ == "__main__":
    main()
