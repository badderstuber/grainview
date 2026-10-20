# GRAINVIEW SWD master on PIO: the Pico's replacement for the ST-Link.
# Pins: SWCLK GP14, SWDIO GP15 (through R1/R2 on the main board to J3 -> JTRACE).
#
# The PIO program only shifts bits; the SWD protocol (requests, ACKs, parity, retries) is
# here in Python, except the block-read loop (viper, straight on the PIO FIFO registers:
# plain Python costs ~280 us per word). Clocking follows CMSIS-DAP: SWCLK idles high, the host changes SWDIO with
# SWCLK low, both sides sample on the rising edge.
#
#   s = SWD()                      # 8 MHz SWCLK (12 MHz also verified)
#   s.connect()                    # -> DPIDR, debug powered up, AP0 (Cortex-M7 AHB-AP)
#   s.read32(a)  s.write32(a, v)  s.write8(a, v)  s.read_block8(a, n) -> bytes
#   s.close()                      # give the pins back
import array
import time

import micropython
import rp2
from machine import Pin

OK, WAIT, FAULT = 1, 2, 4
DP_ABORT, DP_CTRL, DP_SELECT, DP_RDBUFF = 0x0, 0x4, 0x8, 0xC   # DPIDR = 0x0 on read
AP_CSW, AP_TAR, AP_DRW = 0x00, 0x04, 0x0C
CSW_BASE = 0x23000010        # debug master, privileged, auto-increment (single)
CSW_8, CSW_32 = 0, 2         # CSW size field
RETRIES = 100
PIO0 = 0x50200000            # RP2350 PIO0; SM0 FIFOs at FSTAT +0x04, TXF0 +0x10, RXF0 +0x20

# DPv2 dormant -> SWD selection alert, LSB first (byte by byte)
ALERT = (0x92, 0xF3, 0x09, 0x62, 0x95, 0x2D, 0x85, 0x86,
         0xE9, 0xAF, 0xDD, 0xE3, 0xA2, 0x0E, 0xBC, 0x19)


class SWDError(Exception):
    pass


@rp2.asm_pio(sideset_init=rp2.PIO.OUT_HIGH, out_init=rp2.PIO.OUT_HIGH,
             set_init=rp2.PIO.OUT_HIGH, out_shiftdir=rp2.PIO.SHIFT_RIGHT,
             in_shiftdir=rp2.PIO.SHIFT_RIGHT)
def _swd_pio():
    # command word: bit 0 = 1 write / 0 read, bits 1-5 = bit count - 1.
    # A write's data word follows; a read pushes its bits (in the top of the word).
    # 4 PIO cycles per SWCLK period, both directions.
    label("top")
    pull()                  .side(1)
    out(y, 1)               .side(1)
    out(x, 5)               .side(1)
    jmp(not_y, "rd")        .side(1)
    set(pindirs, 1)         .side(1)
    pull()                  .side(1)
    label("wr")
    out(pins, 1)            .side(0) [1]
    jmp(x_dec, "wr")        .side(1) [1]
    jmp("top")              .side(1)
    label("rd")
    set(pindirs, 0)         .side(1)
    label("rl")
    nop()                   .side(0) [1]
    in_(pins, 1)            .side(1)
    jmp(x_dec, "rl")        .side(1)
    push()                  .side(1)


def _par(v):
    v ^= v >> 16
    v ^= v >> 8
    v ^= v >> 4
    return (0x6996 >> (v & 0xF)) & 1


# request byte for (APnDP, RnW, A[3:2]): start, ap, rnw, a2, a3, parity, stop, park
_REQ = bytes([1 | ap << 1 | rnw << 2 | (a & 1) << 3 | (a >> 1) << 4
             | ((ap + rnw + (a & 1) + (a >> 1)) & 1) << 5 | 1 << 7
             for ap in (0, 1) for rnw in (0, 1) for a in range(4)])


@micropython.viper
def _read_words(buf, off: int, n: int, req_ap: int, req_last: int) -> int:
    """SM0 must be idle. n posted AP DRW reads, then one req_last (DP RDBUFF) read; the
    n results land in buf[off:off + n]. Returns 0, or kind << 16 | index on error
    (kind 1 parity, 2 WAIT timeout, 3 FAULT, 4 no ACK). Same bits as SWD.xfer()."""
    p = ptr32(PIO0)
    o = ptr32(buf)
    i = 0
    while i <= n:
        req = req_ap if i < n else req_last
        tries = 0
        while True:
            while p[1] & 0x10000:              # TX full
                pass
            p[4] = 15                          # write 8 bits: the request
            while p[1] & 0x10000:
                pass
            p[4] = req
            while p[1] & 0x10000:
                pass
            p[4] = 6                           # read 4: turnaround + ACK
            while p[1] & 0x100:                # RX empty
                pass
            ack = (p[8] >> 29) & 7
            if ack == 1:
                p[4] = 62                      # read 32: data
                while p[1] & 0x10000:
                    pass
                p[4] = 2                       # read 2: parity + turnaround
                while p[1] & 0x100:
                    pass
                v = p[8]
                while p[1] & 0x100:
                    pass
                par = (p[8] >> 30) & 1
                while p[1] & 0x10000:
                    pass
                p[4] = 15                      # write 8: idle
                while p[1] & 0x10000:
                    pass
                p[4] = 0
                x = v ^ (v >> 16)
                x ^= x >> 8
                x ^= x >> 4
                if par != (0x6996 >> (x & 0xF)) & 1:
                    return 1 << 16 | i
                if i > 0:
                    o[off + i - 1] = v
                break
            p[4] = 0                           # read 1: turnaround back to the host
            while p[1] & 0x100:
                pass
            x = p[8]
            if ack == 2 and tries < 100:
                tries += 1
                while p[1] & 0x10000:
                    pass
                p[4] = 15
                while p[1] & 0x10000:
                    pass
                p[4] = 0
                continue
            if ack == 2:
                return 2 << 16 | i
            while p[1] & 0x10000:
                pass
            if ack == 4:
                p[4] = 15
                while p[1] & 0x10000:
                    pass
                p[4] = 0
                return 3 << 16 | i
            p[4] = 62                          # no ACK: let the target finish, then idle
            while p[1] & 0x100:
                pass
            x = p[8]
            p[4] = 15
            while p[1] & 0x10000:
                pass
            p[4] = 0
            return 4 << 16 | i
        i += 1
    return 0


class SWD:
    def __init__(self, khz=8000, clk=14, dio=15, sm=0):
        self.pins = (clk, dio)
        Pin(dio, Pin.IN, Pin.PULL_UP)          # pull-ups only (RP2350 erratum E9)
        self.sm = rp2.StateMachine(sm, _swd_pio, freq=khz * 4000,
                                   sideset_base=Pin(clk), out_base=Pin(dio),
                                   set_base=Pin(dio), in_base=Pin(dio))
        self.sm.active(1)
        self.khz = khz
        self.sel = self.csw = self.tar = None

    def close(self):
        self.sm.active(0)
        for p in self.pins:
            Pin(p, Pin.IN)

    # ---- bits ----
    def _w(self, v, n):
        self.sm.put(2 * n - 1)                 # ((n - 1) << 1) | write
        self.sm.put(v)

    def _r(self, n):
        self.sm.put((n - 1) << 1)
        return self.sm.get() >> (32 - n)

    # ---- transactions ----
    def xfer(self, ap, rnw, addr, data=0):
        req = _REQ[ap << 3 | rnw << 2 | (addr >> 2) & 3]
        for _ in range(RETRIES):
            self._w(req, 8)
            if rnw:
                ack = (self._r(4) >> 1) & 7    # turnaround + ACK
                if ack == OK:
                    v = self._r(32)
                    p = self._r(2) & 1         # parity + turnaround
                    self._w(0, 8)              # idle
                    if p != _par(v):
                        raise SWDError("read parity error")
                    return v
                self._r(1)                     # turnaround back to the host
            else:
                ack = (self._r(5) >> 1) & 7    # turnaround + ACK + turnaround
                if ack == OK:
                    self._w(data, 32)
                    self._w(_par(data), 9)     # parity + 8 idle
                    return None
            if ack == WAIT:
                self._w(0, 8)
                continue
            if ack == FAULT:
                self._w(0, 8)
                self.sel = self.csw = self.tar = None
                self.xfer(0, 0, DP_ABORT, 0x1E)   # clear the sticky error flags
                raise SWDError("FAULT (%s %s 0x%X)" % (
                    "AP" if ap else "DP", "read" if rnw else "write", addr))
            self._r(32)                        # protocol error: let the target finish
            self._r(1)
            self._w(0, 8)
            self.sel = self.csw = self.tar = None
            raise SWDError("no ACK (0b%s) on %s %s 0x%X" % (
                "{:03b}".format(ack), "AP" if ap else "DP", "read" if rnw else "write", addr))
        raise SWDError("WAIT never cleared")

    # ---- connect ----
    def _line_reset(self):
        self._w(0xFFFFFFFF, 32)
        self._w(0xFFFFFF, 24)                  # 56 ones (>= 50)
        self._w(0, 8)

    def _jtag_to_swd(self):
        self._w(0xFFFFFFFF, 32)
        self._w(0xFFFFFF, 24)
        self._w(0xE79E, 16)
        self._line_reset()

    def _dormant_to_swd(self):
        self._w(0xFF, 8)
        for b in ALERT:
            self._w(b, 8)
        self._w(0x1A << 4, 12)                 # 4 low cycles, then the SW-DP activation code
        self._line_reset()

    def connect(self):
        """Wake the SW-DP, power up the debug domain. Returns DPIDR."""
        self.sel = self.csw = self.tar = None
        err = None
        for seq in (self._jtag_to_swd, self._dormant_to_swd):
            seq()
            try:
                dpidr = self.xfer(0, 1, 0)
                break
            except SWDError as e:
                err = e
        else:
            raise SWDError("no SWD response (%s)" % err)
        self.xfer(0, 0, DP_ABORT, 0x1E)
        self.xfer(0, 0, DP_CTRL, 0x50000000)   # CSYSPWRUPREQ | CDBGPWRUPREQ
        for _ in range(100):
            if self.xfer(0, 1, DP_CTRL) & 0xA0000000 == 0xA0000000:
                return dpidr
            time.sleep_ms(1)
        raise SWDError("debug power-up not acknowledged")

    # ---- AP ----
    def _select(self, apsel, bank):
        s = apsel << 24 | bank
        if s != self.sel:
            self.xfer(0, 0, DP_SELECT, s)
            self.sel = s

    def ap_write(self, reg, v, apsel=0):
        self._select(apsel, reg & 0xF0)
        self.xfer(1, 0, reg & 0xC, v)

    def ap_read(self, reg, apsel=0):
        self._select(apsel, reg & 0xF0)
        self.xfer(1, 1, reg & 0xC)             # posted: the value arrives in RDBUFF
        return self.xfer(0, 1, DP_RDBUFF)

    # ---- memory (AP0) ----
    def _csw_size(self, size):
        if self.csw != size:
            self.ap_write(AP_CSW, CSW_BASE | size)
            self.csw = size

    def _set_tar(self, a):
        if self.tar != a:
            self.ap_write(AP_TAR, a)
        self.tar = a

    def read32(self, a):
        self._csw_size(CSW_32)
        self._set_tar(a)
        v = self.ap_read(AP_DRW)
        self.tar = a + 4 if (a + 4) & 0x3FF else None   # auto-increment wraps at 1 KB
        return v

    def write32(self, a, v):
        self._csw_size(CSW_32)
        self._set_tar(a)
        self.ap_write(AP_DRW, v)
        self.tar = a + 4 if (a + 4) & 0x3FF else None

    def write8(self, a, v):
        self._csw_size(CSW_8)
        self._set_tar(a)
        self.ap_write(AP_DRW, (v & 0xFF) << (8 * (a & 3)))   # byte lane
        self.tar = None

    def read_block32(self, a, n):
        """n words from word-aligned a, as an array('I')."""
        out = array.array("I", [0] * n)
        self._csw_size(CSW_32)
        i = 0
        while i < n:
            k = min(n - i, (0x400 - (a & 0x3FF)) // 4)   # stay inside the 1 KB TAR wrap
            self._set_tar(a)
            self._select(0, 0)
            err = _read_words(out, i, k, _REQ[1 << 3 | 1 << 2 | 3], _REQ[1 << 2 | 3])
            if err:
                self.sel = self.csw = self.tar = None
                kind = err >> 16
                if kind == 3:
                    self.xfer(0, 0, DP_ABORT, 0x1E)
                raise SWDError("block read at 0x%08X: %s" % (
                    a + 4 * max(0, (err & 0xFFFF) - 1),
                    ("", "parity error", "WAIT never cleared", "FAULT", "no ACK")[kind]))
            i += k
            a += 4 * k
            self.tar = a if a & 0x3FF else None
        return out

    def read_block8(self, a, n):
        lo = a & ~3
        words = (a + n - lo + 3) // 4
        b = bytes(self.read_block32(lo, words))
        return b[a - lo:a - lo + n]
