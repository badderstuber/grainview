# Checks + times pico/swd.py against the Multigrain (through J3 -> JTRACE).
# Read-only on the Multigrain, except DCRDR (a debug scratch register, restored after).
#   tools/venv/bin/python tools/gv_pico.py quit
#   mpremote cp pico/swd.py :  &&  mpremote run pico/swdbench.py
import hashlib
import time

from swd import SWD, SWDError

FLASH_SHA = "b71e729cfe1cf1808a2fa1e862d1127fb689cba70d18b09f60713df486387beb"  # bin[:4096]
FLASH_1_8 = bytes.fromhex("000220d5ab0408")                                       # bin[1:8]
SOUND_BASE, SOUND_STRIDE, LO, HI = 0x24020B84, 0x9F0, 0x48, 0x424   # the server's poll block
DCRDR = 0xE000EDF8


def check(s):
    print("  DPIDR 0x%08X" % s.connect())
    print("  CPUID 0x%08X  IDCODE 0x%08X" % (s.read32(0xE000ED00), s.read32(0x5C001000)))

    t = time.ticks_us()
    fl = s.read_block8(0x08000000, 4096)
    dt = time.ticks_diff(time.ticks_us(), t)
    ok = hashlib.sha256(fl).digest().hex() == FLASH_SHA
    print("  flash 4 KB vs Multigrain.1.4.8.0.bin: %s  (%d ms, %.0f KB/s)" % (
        "MATCH" if ok else "MISMATCH", dt // 1000, 4096 / dt * 1e6 / 1024))
    print("  unaligned read8: %s" % ("MATCH" if s.read_block8(0x08000001, 7) == FLASH_1_8
                                     else "MISMATCH"))

    t = time.ticks_us()
    for n in range(8):
        s.read_block8(SOUND_BASE + n * SOUND_STRIDE + LO, HI - LO)
    print("  server poll (8 sound blocks, %d B): %d ms" % (
        8 * (HI - LO), time.ticks_diff(time.ticks_us(), t) // 1000))

    old = s.read32(DCRDR)
    s.write32(DCRDR, 0xA5C35A3C)
    back = s.read32(DCRDR)
    s.write32(DCRDR, old)
    print("  write32 (DCRDR): %s" % ("OK" if back == 0xA5C35A3C else "read back 0x%08X" % back))


for khz in (1000, 4000, 8000, 12000):
    print("SWCLK %d kHz" % khz)
    s = SWD(khz=khz)
    try:
        check(s)
    except SWDError as e:
        print("  FAILED:", e)
    finally:
        s.close()
