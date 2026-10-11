#!/usr/bin/env python3
"""mg_call.py - call a firmware function on the running Multigrain over SWD.

This is how we DRIVE the module (load a WAV, scan the SD, select a sound) without
modifying firmware: briefly halt the core, set up a function call in the CPU
registers, point the PC at the firmware's own function, let it run, catch the
return, then restore the original context and resume. Interrupts stay enabled so
the function's SD/DMA/timer dependencies still work (and audio ISRs keep firing).

    r0..r3 = up to 4 integer arguments (ARM AAPCS)
    LR     = a "catch" address with a breakpoint, so the return halts us
    PC     = function entry | 1 (Thumb)

Usage:
    # safest first test - directory scan, NO args (just proves the mechanism):
    tools/venv/bin/python tools/mg_call.py 0x0801f0d4

    # with integer args (hex or dec), e.g. load WAV index 0 into target ptr:
    tools/venv/bin/python tools/mg_call.py 0x08026754 0 0x20000abc

    --catch ADDR   return-catch breakpoint (default 0x08000000, the SP word -
                   never executed normally, so no false hits)
    --timeout SEC  how long to wait for the call to return (default 8)
    --dry-run      show what it WOULD do, don't touch the target

WARNING: halts the core briefly and runs firmware code with the args you give.
Wrong args can hang the firmware - recover with a Boot-button reset / power
cycle (no brick risk). Start with the no-arg dir scan (0x0801f0d4).
"""
import argparse
import sys
import time


def parse_int(s):
    return int(s, 0)


def connect(freq_hz):
    from pyocd.core.helpers import ConnectHelper
    session = ConnectHelper.session_with_chosen_probe(
        blocking=False,
        options={
            "target_override": "cortex_m",
            "connect_mode": "attach",      # don't reset; we halt explicitly
            "frequency": freq_hz,
            "resume_on_disconnect": True,  # leave the module running on exit
        },
    )
    if session is None:
        sys.exit("No ST-Link found. Plug it in and power the module.")
    session.open()
    return session


CORE_REGS = ["r0", "r1", "r2", "r3", "r4", "r5", "r6", "r7", "r8", "r9",
             "r10", "r11", "r12", "sp", "lr", "pc", "xpsr"]


def swd_call(target, func, args, catch, timeout):
    from pyocd.core.target import Target
    target.halt()                        # must halt before reading core regs
    # save full context so we can put the module back exactly as it was
    saved = {r: target.read_core_register(r) for r in CORE_REGS}
    print("  saved context: pc=0x%08x sp=0x%08x lr=0x%08x"
          % (saved["pc"], saved["sp"], saved["lr"]))
    bp_set = False
    try:
        for i, a in enumerate(args[:4]):
            target.write_core_register("r%d" % i, a & 0xFFFFFFFF)
        bp_set = target.set_breakpoint(catch)
        if not bp_set:
            print("  WARN: could not set breakpoint at catch addr")
        target.write_core_register("lr", catch | 1)     # Thumb return
        target.write_core_register("pc", func | 1)       # Thumb entry
        target.write_core_register("xpsr", saved["xpsr"] | (1 << 24))  # T bit
        print("  calling 0x%08x(%s) ..."
              % (func, ", ".join("0x%x" % a for a in args)))
        target.resume()
        t0 = time.time()
        while time.time() - t0 < timeout:
            if target.get_state() == Target.State.HALTED:
                pc = target.read_core_register("pc")
                if (pc & ~1) == (catch & ~1):
                    ret = target.read_core_register("r0")
                    print("  returned after %.2fs  r0 = 0x%08x (%d)"
                          % (time.time() - t0, ret, ret))
                    return ret
                # halted somewhere else - a fault or stray breakpoint
                print("  halted at 0x%08x (not the catch addr) after %.2fs"
                      % (pc, time.time() - t0))
                return None
            time.sleep(0.01)
        print("  TIMEOUT after %.1fs - function did not return." % timeout)
        target.halt()
        print("  halted at pc=0x%08x" % target.read_core_register("pc"))
        return None
    finally:
        if bp_set:
            try:
                target.remove_breakpoint(catch)
            except Exception:
                pass
        for r, v in saved.items():
            try:
                target.write_core_register(r, v)
            except Exception:
                pass
        try:
            target.resume()
        except Exception:
            pass
        print("  context restored, module resumed.")


def main():
    ap = argparse.ArgumentParser(description="Call a firmware function over SWD.")
    ap.add_argument("func", type=parse_int, help="function entry address (hex/dec)")
    ap.add_argument("args", nargs="*", type=parse_int, help="up to 4 integer args")
    ap.add_argument("--catch", type=parse_int, default=0x08000000,
                    help="return-catch breakpoint addr (default 0x08000000)")
    ap.add_argument("--timeout", type=float, default=8.0)
    ap.add_argument("--freq", type=int, default=4_000_000)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.dry_run:
        print("DRY RUN - would call 0x%08x with args %s, catch 0x%08x"
              % (a.func, [hex(x) for x in a.args], a.catch))
        return

    session = connect(a.freq)
    try:
        swd_call(session.target, a.func, a.args, a.catch, a.timeout)
    finally:
        session.close()


if __name__ == "__main__":
    main()
