#!/usr/bin/env python3
"""SPIKE: read a raw WAV off the module's SD into scratch SDRAM over SWD, no
granular processing, without touching any sound slot.

  FUN_0801fb94(folder, name, buf, max_samples, &n)  -- raw reader:
     seeks past the WAV header, f_read's the PCM into `buf`, *n = words read.

We call it with buf = top of SDRAM (clear of sample buffers), catch the return
on a breakpoint, fully restore the idle-loop context, then pull the bytes out.

Usage: spike_preview.py [wav_index] [max_samples]
"""
import sys, time, struct
sys.path.insert(0, "tools")
from mg_call import connect
from mg_load import IDLE_LO, IDLE_HI, SD_STATE, COUNTS, MAX_FILES, u32, u8
from pyocd.core.target import Target

WAVS_LIST = 0x30008800          # folder 1 (/Wavs) filename cache, 0x100 each
READER    = 0x0801FB94          # FUN_0801fb94(folder,name,buf,max,&n)
SCRATCH   = 0xC3F00000          # top-of-SDRAM scratch (64MB ends 0xC3FFFFFF)
NOUT      = 0xC3FE0000          # output word for *n, clear of the data
CATCH     = 0x08000000          # breakpoint catch (never executed, only a BP target)
CORE_REGS = ["r0","r1","r2","r3","r4","r5","r6","r7","r8","r9","r10","r11",
             "r12","sp","lr","pc","xpsr"]
SENTINEL  = 0xDEADBEEF


def wait_idle(t, tries=300):
    for _ in range(tries):
        t.halt()
        pc, xpsr = t.read_core_registers_raw(["pc", "xpsr"])
        if IDLE_LO <= pc <= IDLE_HI and (xpsr & 0x1FF) == 0:
            return xpsr | (1 << 24)
        t.resume(); time.sleep(0.003)
    return None


def call5(t, func, a0, a1, a2, a3, a4_stack, timeout=5.0):
    xpsr = wait_idle(t)
    if xpsr is None:
        raise RuntimeError("couldn't catch the idle loop")
    saved = t.read_core_registers_raw(CORE_REGS)          # list, in order
    sp = saved[CORE_REGS.index("sp")]
    sp2 = (sp - 16) & ~7
    t.write_memory(NOUT, SENTINEL)                        # sentinel for *n
    t.write_memory(sp2, a4_stack & 0xFFFFFFFF)            # 5th arg at [sp']
    t.set_breakpoint(CATCH)
    try:
        names = ["r0","r1","r2","r3","sp","lr","pc","xpsr"]
        vals  = [a0, a1, a2, a3, sp2, CATCH | 1, func | 1, xpsr]
        t.write_core_registers_raw(names, [v & 0xFFFFFFFF for v in vals])
        t.resume()
        t0 = time.time()
        while time.time() - t0 < timeout:
            if t.get_state() == Target.State.HALTED:
                pc = t.read_core_register("pc")
                if pc == CATCH:
                    r0 = t.read_core_register("r0")
                    n  = t.read_memory(NOUT)
                    return r0, n, (time.time() - t0)
                # halted somewhere unexpected
                raise RuntimeError("halted at unexpected pc=0x%08x" % pc)
            time.sleep(0.01)
        raise RuntimeError("timeout: reader did not return in %.1fs" % timeout)
    finally:
        if t.get_state() != Target.State.HALTED:
            t.halt()
        t.write_core_registers_raw(CORE_REGS, [v & 0xFFFFFFFF for v in saved])
        t.remove_breakpoint(CATCH)
        t.resume()


def main():
    idx    = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    nsamp  = int(sys.argv[2]) if len(sys.argv) > 2 else 32768   # 128 KB
    s = connect(4_000_000)
    t = s.target
    try:
        sd = u32(t, SD_STATE)
        count = min(u32(t, COUNTS + 1 * 4), MAX_FILES[1])
        print("SD state=%d   /Wavs count=%d" % (sd, count))
        if sd == 3:
            sys.exit("SD in error state; aborting.")
        if not (0 <= idx < count):
            sys.exit("index %d out of range (0..%d)" % (idx, count - 1))
        name_ptr = WAVS_LIST + idx * 0x100
        name = bytes(t.read_memory_block8(name_ptr, 0x100)).split(b"\0", 1)[0].decode("latin-1")
        print("reading /Wavs[%d] = %r  (max %d samples = %d KB) -> 0x%08x"
              % (idx, name, nsamp, nsamp * 4 // 1024, SCRATCH))

        pre = tuple(t.read_memory_block32(SCRATCH, 8))
        print("scratch before: " + " ".join("%08x" % w for w in pre))

        r0, n, dt = call5(t, READER, 1, name_ptr, SCRATCH, nsamp, NOUT)
        print("reader returned r0=%d (0=OK)  *n=%d words (%d bytes)  in %.2fs"
              % (r0, n, n * 4, dt))
        if r0 != 0:
            print("  (non-zero = error/EOF code; see decompile)")
        got = n if (0 < n <= nsamp) else nsamp
        raw = bytes(t.read_memory_block8(SCRATCH, got * 4))

        out = "/private/tmp/claude-501/-Users-leo--projects-multigrain/4b828ace-3ef5-4a1d-98e0-8d2ec5aaa2a1/scratchpad/preview.raw"
        with open(out, "wb") as f:
            f.write(raw)
        print("wrote %d bytes -> %s" % (len(raw), out))

        # quick stats: float32 vs int32 interpretation
        fl = struct.unpack("<%df" % got, raw)
        inr = sum(1 for v in fl if -1.5 <= v <= 1.5)
        fmax = max((abs(v) for v in fl if v == v), default=0.0)
        print("float32 view: %d/%d samples in [-1.5,1.5]  peak|f|=%.4g" % (inr, got, fmax))
    finally:
        s.close()


if __name__ == "__main__":
    main()
