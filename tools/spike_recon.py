#!/usr/bin/env python3
"""Read-only recon for the WAV-preview spike:
  1. find SDRAM (0xCxxxxxxx) pointers inside the 8 sound structs (= sample buffers)
  2. probe how far SDRAM is mapped from 0xC0000000
  3. stability-check a candidate scratch region (read twice, ~0.4s apart)
No writes, no halts."""
import sys, time
sys.path.insert(0, "tools")
from mg_call import connect

SOUND_BASE = 0x24020B84
STRIDE = 0x9F0
SDRAM = 0xC0000000


def main():
    s = connect(4_000_000)
    t = s.target
    try:
        print("=== SDRAM pointers found in sound structs ===")
        for n in range(8):
            base = SOUND_BASE + n * STRIDE
            words = t.read_memory_block32(base, STRIDE // 4)
            hits = [(i * 4, w) for i, w in enumerate(words)
                    if 0xC0000000 <= w <= 0xCFFFFFFF]
            if hits:
                hs = ", ".join("+0x%x=0x%08x" % (o, w) for o, w in hits)
                print("  sound %d @0x%08x: %s" % (n, base, hs))
            else:
                print("  sound %d @0x%08x: (no SDRAM ptr)" % (n, base))

        print("\n=== SDRAM extent (4MB steps from 0xC0000000) ===")
        last_ok = None
        for k in range(0, 65):  # up to 256MB
            a = SDRAM + k * 0x400000
            try:
                v = t.read_memory_block32(a, 1)[0]
                last_ok = a
            except Exception as e:
                print("  fault at 0x%08x (%d MB) -> SDRAM spans 0x%08x..0x%08x"
                      % (a, k * 4, SDRAM, (last_ok or SDRAM) + 0x3FFFFF))
                break
        else:
            print("  mapped through 0x%08x (>=256MB?!)" % last_ok)

        print("\n=== stability of candidate scratch regions ===")
        # read 64 words at a few offsets, twice ~0.4s apart; stable+same = idle
        cands = [SDRAM + 0x00000000, SDRAM + 0x00100000, SDRAM + 0x00400000,
                 SDRAM + 0x01000000, SDRAM + 0x02000000]
        snap1 = {}
        for a in cands:
            try:
                snap1[a] = tuple(t.read_memory_block32(a, 64))
            except Exception:
                snap1[a] = None
        time.sleep(0.4)
        for a in cands:
            if snap1[a] is None:
                print("  0x%08x: UNMAPPED" % a); continue
            try:
                s2 = tuple(t.read_memory_block32(a, 64))
            except Exception:
                print("  0x%08x: became unreadable" % a); continue
            same = s2 == snap1[a]
            allz = all(w == 0 for w in s2)
            allff = all(w == 0xFFFFFFFF for w in s2)
            unini = all((w & 0xFFFF) in (0xFFFE, 0xFFFF, 0x0000) for w in s2)
            print("  0x%08x: %-14s first=0x%08x %s%s%s"
                  % (a, "STABLE" if same else "CHANGING", s2[0],
                     "all-zero " if allz else "",
                     "all-ff " if allff else "",
                     "uninit-ish " if unini and not allz and not allff else ""))
    finally:
        s.close()


if __name__ == "__main__":
    main()
