#!/usr/bin/env python3
"""mg_watch.py - catch WHO writes a RAM address (hardware watchpoint over SWD).

Arms a DWT write-watchpoint on ADDR, waits for you to do something on the
module (press a button...), and when the firmware writes ADDR the core halts:
we print PC/LR + disassembly of the writing code, then remove the watchpoint
and resume. The halt lasts milliseconds (tiny audio blip at most).

Usage:
    tools/venv/bin/python tools/mg_watch.py 0x20008c70            # first hit
    tools/venv/bin/python tools/mg_watch.py 0x20008c70 --hits 3   # several
    tools/venv/bin/python tools/mg_watch.py 0x20008c70 --size 1   # byte watch
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from mg_call import connect  # noqa: E402
from mg_pcsample import disasm  # noqa: E402
from mg_xref import func_start  # noqa: E402


def stack_callers(t, sp, depth=0x400):
    """Heuristic unwind: words on the stack that are Thumb return addresses
    (odd, in flash, preceded by a BL/BLX) -> likely call chain, innermost first."""
    import struct
    from mg_xref import DATA, BASE, bl_target
    raw = bytes(t.read_memory_block8(sp, depth))
    out = []
    for o in range(0, depth, 4):
        w = struct.unpack_from("<I", raw, o)[0]
        if not (w & 1) or not BASE <= w < BASE + len(DATA):
            continue
        ret = w & ~1
        p = ret - BASE
        hw1, hw2 = struct.unpack_from("<HH", DATA, p - 4)
        blx_reg = struct.unpack_from("<H", DATA, p - 2)[0]
        if bl_target(ret - 4, hw1, hw2) is not None:
            callee = bl_target(ret - 4, hw1, hw2)
            out.append((sp + o, ret, f"BL 0x{callee:08x}"))
        elif (blx_reg & 0xFF87) == 0x4780:
            out.append((sp + o, ret, f"BLX r{(blx_reg >> 3) & 0xF}"))
    return out


def main():
    ap = argparse.ArgumentParser(description="Hardware write-watchpoint on an address.")
    ap.add_argument("addr", type=lambda s: int(s, 0))
    ap.add_argument("--size", type=int, default=4, choices=(1, 2, 4))
    ap.add_argument("--hits", type=int, default=1, help="stop after this many writes")
    ap.add_argument("--timeout", type=float, default=120.0, help="seconds to wait per hit")
    ap.add_argument("--stack", action="store_true",
                    help="also print a heuristic call chain from the stack")
    ap.add_argument("--freq", type=int, default=4_000_000)
    a = ap.parse_args()

    from pyocd.core.target import Target
    session = connect(a.freq)
    t = session.target
    wtype = Target.WatchpointType.WRITE
    armed = False
    try:
        for hit in range(a.hits):
            before = t.read_memory(a.addr, a.size * 8)
            if not t.set_watchpoint(a.addr, a.size, wtype):
                sys.exit("Could not set watchpoint (no free DWT comparator?)")
            armed = True
            print(f"[{hit + 1}/{a.hits}] watching writes to 0x{a.addr:08x} "
                  f"(now {before:#x}) - do the thing on the module...")
            t0 = time.time()
            while t.get_state() != Target.State.HALTED:
                if time.time() - t0 > a.timeout:
                    print("  timeout - no write seen.")
                    return
                time.sleep(0.005)
            pc = t.read_core_register("pc")
            lr = t.read_core_register("lr")
            after = t.read_memory(a.addr, a.size * 8)
            chain = stack_callers(t, t.read_core_register("sp")) if a.stack else []
            t.remove_watchpoint(a.addr, a.size, wtype)
            armed = False
            t.resume()
            fs = func_start(pc)
            print(f"  WRITE {before:#x} -> {after:#x}   pc=0x{pc:08x} "
                  f"(in FUN_{fs:08x})  lr=0x{lr:08x}" if fs else
                  f"  WRITE {before:#x} -> {after:#x}   pc=0x{pc:08x}  lr=0x{lr:08x}")
            print("  (DWT halts just AFTER the store - it's the instruction before =>)")
            print(disasm(pc, before=0x18, after=0x6))
            if chain:
                print("  call chain (innermost first, heuristic):")
                for at, ret, how in chain:
                    fs = func_start(ret)
                    print(f"    @0x{at:08x}  ret 0x{ret:08x} "
                          f"in FUN_{fs:08x}  ({how})" if fs else
                          f"    ret 0x{ret:08x}  ({how})")
    finally:
        if armed:
            try:
                t.remove_watchpoint(a.addr, a.size, wtype)
            except Exception:
                pass
        try:
            if t.get_state() == Target.State.HALTED:
                t.resume()
        except Exception:
            pass
        session.close()


if __name__ == "__main__":
    main()
