# GRAINVIEW SWD link test: reads the Multigrain's debug IDs through J3 -> JTRACE.
# Proves the main board's SWD path (GP14/15 + R1/R2, VTREF sense on GP26, the ribbon).
# Read-only: never halts the CPU or writes target memory, only debug-port registers.
#
# Run from the Mac (stop grainview_server.py first, it holds the USB port):
#   tools/venv/bin/python tools/gv_pico.py quit
#   ~/Library/Python/3.9/bin/mpremote run pico/swdtest.py
#
# Bit-banged in plain MicroPython (tens of kHz): slow, but SWD has no minimum clock.
# Clocking follows CMSIS-DAP: SWCLK idles high, the host changes SWDIO with SWCLK low,
# both sides sample on the rising edge.
import time
from machine import ADC, Pin

SWCLK, SWDIO, VTREF = 14, 15, 26

OK, WAIT, FAULT = 1, 2, 4
DP_ABORT, DP_CTRL, DP_SELECT, DP_RDBUFF = 0x0, 0x4, 0x8, 0xC   # DPIDR is 0x0 on read

# DPv2 dormant -> SWD: selection alert (LSB first, byte by byte)
ALERT = (0x92, 0xF3, 0x09, 0x62, 0x95, 0x2D, 0x85, 0x86,
         0xE9, 0xAF, 0xDD, 0xE3, 0xA2, 0x0E, 0xBC, 0x19)

H7_DEV = {0x450: "STM32H74x/75x", 0x480: "STM32H7A3/B3", 0x483: "STM32H72x/73x"}


class SWDError(Exception):
    pass


clk = Pin(SWCLK, Pin.OUT, value=1)
dio = Pin(SWDIO, Pin.OUT, value=1)
clk_hi, clk_lo = clk.on, clk.off


def drive():
    dio.init(Pin.OUT)


def release():
    dio.init(Pin.IN, Pin.PULL_UP)        # pull-ups only (RP2350 erratum E9)


def write_bits(v, n):
    for _ in range(n):
        dio.value(v & 1)
        clk_lo()
        clk_hi()
        v >>= 1


def read_bits(n):
    v = 0
    for i in range(n):
        clk_lo()
        v |= dio.value() << i
        clk_hi()
    return v


def cycle(n=1):
    for _ in range(n):
        clk_lo()
        clk_hi()


def parity(v):
    return bin(v).count("1") & 1


def xfer(ap, rnw, addr, data=0):
    """One SWD transaction. Returns the read value (None for writes)."""
    a2, a3 = (addr >> 2) & 1, (addr >> 3) & 1
    req = 1 | ap << 1 | rnw << 2 | a2 << 3 | a3 << 4 | ((ap + rnw + a2 + a3) & 1) << 5 | 1 << 7
    for _ in range(100):
        drive()
        write_bits(req, 8)
        release()
        cycle()                          # turnaround
        ack = read_bits(3)
        if ack == OK:
            if rnw:
                v = read_bits(32)
                p = read_bits(1)
                cycle()                  # turnaround
                drive()
                write_bits(0, 8)         # idle
                if p != parity(v):
                    raise SWDError("parity error (noise / bad SWDIO connection?)")
                return v
            cycle()
            drive()
            write_bits(data, 32)
            write_bits(parity(data), 1)
            write_bits(0, 8)
            return None
        if ack == WAIT:
            cycle()
            drive()
            write_bits(0, 8)
            continue
        if ack == FAULT:
            cycle()
            drive()
            raise SWDError("FAULT")
        cycle(33)                        # protocol error: let a confused target finish
        drive()
        hint = {7: "SWDIO stays high: nothing answering (ribbon? Multigrain powered?)",
                0: "SWDIO stuck low"}.get(ack, "garbled")
        raise SWDError("no ACK (%s) on %s %s 0x%X: %s" % (
            bin(ack), "AP" if ap else "DP", "read" if rnw else "write", addr, hint))
    raise SWDError("WAIT never cleared")


def line_reset():
    drive()
    write_bits(0xFFFFFF, 24)
    write_bits(0xFFFFFFFF, 32)           # 56 ones (>= 50)
    write_bits(0, 8)                     # idle


def jtag_to_swd():
    drive()
    write_bits(0xFFFFFFFF, 32)
    write_bits(0xFFFFFF, 24)
    write_bits(0xE79E, 16)
    line_reset()


def dormant_to_swd():
    drive()
    write_bits(0xFF, 8)
    for b in ALERT:
        write_bits(b, 8)
    write_bits(0, 4)
    write_bits(0x1A, 8)                  # SW-DP activation code
    line_reset()


def ap_read(apsel, reg):
    xfer(0, 0, DP_SELECT, apsel << 24 | (reg & 0xF0))
    xfer(1, 1, reg & 0xC)                # posted: the value arrives in RDBUFF
    return xfer(0, 1, DP_RDBUFF)


def ap_write(apsel, reg, v):
    xfer(0, 0, DP_SELECT, apsel << 24 | (reg & 0xF0))
    xfer(1, 0, reg & 0xC, v)


def mem_read(addr, apsel=0):
    ap_write(apsel, 0x00, 0x23000002)    # CSW: 32-bit, no auto-increment, debug master
    ap_write(apsel, 0x04, addr)          # TAR
    return ap_read(apsel, 0x0C)          # DRW


def main():
    v = ADC(VTREF).read_u16() * 3.3 / 65535
    print("VTREF (GP26): %.2f V" % v)
    if v < 2.5:
        print("  -> no 3.3 V from JTRACE: is the Multigrain powered and the ribbon in"
              " (red stripe = pin 1 at both ends)?")
        return

    dpidr = None
    for name, seq in (("JTAG->SWD", jtag_to_swd), ("dormant->SWD", dormant_to_swd)):
        seq()
        try:
            dpidr = xfer(0, 1, 0)
            print("connected (%s)" % name)
            break
        except SWDError as e:
            print("  %s: %s" % (name, e))
    if dpidr is None:
        print("FAILED: no SWD response")
        return

    designer = (dpidr >> 1) & 0x7FF
    print("DPIDR  0x%08X  (DP v%d, part 0x%02X, designer 0x%03X%s)" % (
        dpidr, (dpidr >> 12) & 0xF, (dpidr >> 20) & 0xFF, designer,
        " = ARM" if designer == 0x23B else ""))

    xfer(0, 0, DP_ABORT, 0x1E)                           # clear sticky errors
    xfer(0, 0, DP_CTRL, 0x50000000)                      # debug + system power-up request
    for _ in range(100):
        if xfer(0, 1, DP_CTRL) & 0xA0000000 == 0xA0000000:
            break
        time.sleep_ms(1)
    else:
        print("debug power-up not acknowledged; stopping")
        return

    print("AP0 IDR 0x%08X" % ap_read(0, 0xFC))
    cpuid = mem_read(0xE000ED00)
    print("CPUID  0x%08X%s" % (cpuid, "  = Cortex-M7" if (cpuid >> 4) & 0xFFF == 0xC27 else ""))
    idc = mem_read(0x5C001000)
    dev = idc & 0xFFF
    print("DBGMCU_IDCODE 0x%08X  (dev 0x%03X = %s, rev 0x%04X)" % (
        idc, dev, H7_DEV.get(dev, "?"), idc >> 16))

    xfer(0, 0, DP_CTRL, 0)                               # drop the power-up request
    print("SWD link OK")


try:
    main()
except SWDError as e:
    print("FAILED:", e)
finally:
    clk.init(Pin.IN)                     # let go of the JTRACE lines
    dio.init(Pin.IN)
