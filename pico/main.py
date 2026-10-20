# GRAINVIEW USB screen (autostarts on power-up).
# Shows the frames the Mac sends (tools/grainview_server.py) and reports the buttons and
# encoder back. The emulator in the browser does all the UI; this is a dumb screen + keys.
#
# Mac -> Pico, binary packets:  A5 5A <type> <payload>
#   'F' + 8192 bytes          full frame, 128x128, 2 px per byte, left px in the high nibble
#   'R' + r0 + n + n*64 bytes rows r0..r0+n-1
#   'C' + 1 byte              contrast
#   'H'                       hello -> replies "@HELLO 1"
#   'Q'                       quit to the REPL (lets mpremote in; tools/gv_pico.py does this)
#   'D' + seq + op + len(u16) + body    SWD to the Multigrain (pico/swd.py), see swd_op()
# Pico -> Mac, text lines:  "@E +1" (encoder steps)  "@B BACK 1" (button down / 0 = up)
#   "@D <seq> <status> <n>" + n raw bytes   SWD reply (status 0 ok, 1 = n bytes of error text)
#
# Ctrl-C is disabled while running (frames are binary). Escape hatch: hold BACK while
# plugging in and it stops before taking over, leaving the REPL free.
import array
import machine
import micropython
import select
import struct
import sys
import time
from machine import Pin, SPI
import pins
from ssd1327 import SSD1327

micropython.alloc_emergency_exception_buf(100)

def inp(n):
    return Pin(n, Pin.IN, Pin.PULL_UP)

buttons = [(name, inp(gp)) for name, gp in pins.BUTTONS] + [("PUSH", inp(pins.ENC_SW))]
if buttons[0][1]() == 0:                      # BACK held at power-up
    print("BACK held: GRAINVIEW screen not started")
    raise SystemExit

spi = SPI(pins.SPI_ID, baudrate=10_000_000, polarity=0, phase=0,
          sck=Pin(pins.SCR_SCK), mosi=Pin(pins.SCR_MOSI))
oled = SSD1327(spi, dc=Pin(pins.SCR_DC, Pin.OUT, value=0),
               cs=Pin(pins.SCR_CS, Pin.OUT, value=1),
               rst=Pin(pins.SCR_RST, Pin.OUT, value=1))
oled.text("GRAINVIEW", 28, 52, 15)
oled.text("waiting for Mac", 4, 68, 6)
oled.show()

# --- encoder: Gray-code decoder in a hard IRQ, one step per detent (rest A=B=1) ---
enc_a, enc_b = inp(pins.ENC_A), inp(pins.ENC_B)
TR = array.array('b', (0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0))
es = array.array('i', [(enc_a() << 1) | enc_b(), 0, 0])     # prev state, accumulator, steps

def enc_irq(_):
    cur = (enc_a() << 1) | enc_b()
    prev = es[0]
    if cur != prev:
        es[1] += TR[(prev << 2) | cur]
        es[0] = cur
        if cur == 3:
            if es[1] >= 2:
                es[2] += 1
            elif es[1] <= -2:
                es[2] -= 1
            es[1] = 0

for p in (enc_a, enc_b):
    p.irq(enc_irq, Pin.IRQ_RISING | Pin.IRQ_FALLING, hard=True)

# --- serial ---
inb = sys.stdin.buffer
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)
hdr = bytearray(2)
one = bytearray(1)
fb = memoryview(oled.buffer)
BPR = 64

def read_into(mv):
    inb.readinto(mv)                          # blocks until mv is full

# --- SWD (to the Multigrain through J3 -> JTRACE) ---
dbg = [None]                                  # the SWD object, made on the first 'c'

def swd_op(op, body):
    """One SWD request -> reply bytes. All little-endian; addresses/words u32.
    c khz(u16) -> DPIDR      r addr n -> n bytes      w addr words...      b addr bytes...
    R (addr, n u16)... -> the spans' bytes, back to back
    h -> DHCSR (halted)      u (resume)               g regs(u8)... -> words
    i lo hi tries(u16) -> pc xpsr, halted with pc in lo..hi (or b"": missed, running)
    G (reg u8, word)...      x (release the pins)"""
    s = dbg[0]
    if op == 0x63:                            # 'c'
        khz = struct.unpack("<H", body)[0]
        if s is None or s.khz != khz:
            if s is not None:
                s.close()
            from swd import SWD
            s = dbg[0] = SWD(khz=khz)
        return struct.pack("<I", s.connect())
    if op == 0x78:                            # 'x'
        if s is not None:
            s.close()
            dbg[0] = None
        return b""
    if s is None:
        raise RuntimeError("SWD not connected")
    if op == 0x72:                            # 'r'
        a, n = struct.unpack("<II", body)
        return s.read_block8(a, n)
    if op == 0x52:                            # 'R'
        return b"".join(s.read_block8(*struct.unpack_from("<IH", body, i))
                        for i in range(0, len(body), 6))
    if op == 0x77:                            # 'w'
        a = struct.unpack_from("<I", body)[0]
        for i in range(4, len(body), 4):
            s.write32(a, struct.unpack_from("<I", body, i)[0])
            a += 4
        return b""
    if op == 0x62:                            # 'b'
        a = struct.unpack_from("<I", body)[0]
        for v in body[4:]:
            s.write8(a, v)
            a += 1
        return b""
    if op == 0x68:                            # 'h'
        return struct.pack("<I", s.halt())
    if op == 0x69:                            # 'i'
        r = s.halt_in(*struct.unpack("<IIH", body))
        return struct.pack("<II", *r) if r else b""
    if op == 0x75:                            # 'u'
        s.resume()
        return b""
    if op == 0x67:                            # 'g'
        return b"".join(struct.pack("<I", s.read_reg(i)) for i in body)
    if op == 0x47:                            # 'G'
        for i in range(0, len(body), 5):
            s.write_reg(body[i], struct.unpack_from("<I", body, i + 1)[0])
        return b""
    raise RuntimeError("unknown SWD op 0x%02X" % op)

def swd_packet():
    hd = bytearray(4)
    read_into(hd)
    seq, op, n = hd[0], hd[1], hd[2] | hd[3] << 8
    body = bytearray(n)
    if n:
        read_into(body)
    try:
        out, st = swd_op(op, body), 0
    except Exception as e:                    # SWDError, bad args: report, keep running
        out, st = str(e).encode(), 1
    sys.stdout.buffer.write(("@D %d %d %d\n" % (seq, st, len(out))).encode())
    sys.stdout.buffer.write(out)

def packet():
    read_into(one)                            # hunt for the A5 5A sync
    if one[0] != 0xA5:
        return
    read_into(one)
    if one[0] != 0x5A:
        return
    read_into(one)
    t = one[0]
    if t == 0x46:                             # 'F'
        read_into(fb)
        oled.show()
    elif t == 0x52:                           # 'R'
        read_into(hdr)
        r0, n = hdr[0], hdr[1]
        if r0 + n <= 128 and n:
            read_into(fb[r0 * BPR:(r0 + n) * BPR])
            oled.show_rows(r0, n)
    elif t == 0x43:                           # 'C'
        read_into(one)
        oled.contrast(one[0])
    elif t == 0x48:                           # 'H'
        print("@HELLO 1")
    elif t == 0x44:                           # 'D'
        swd_packet()
    elif t == 0x51:                           # 'Q'
        raise SystemExit

state = [p() for _, p in buttons]
changed = [0] * len(buttons)
micropython.kbd_intr(-1)
try:
    while True:
        if es[2]:
            irq = machine.disable_irq()
            n = es[2]
            es[2] = 0
            machine.enable_irq(irq)
            print("@E %+d" % n)
        now = time.ticks_ms()
        for i, (name, p) in enumerate(buttons):
            v = p()
            if v != state[i] and time.ticks_diff(now, changed[i]) > 20:
                state[i] = v
                changed[i] = now
                print("@B %s %d" % (name, 1 - v))
        if poller.poll(2):
            packet()
except SystemExit:
    oled.fill(0)
    oled.text("GRAINVIEW", 28, 52, 15)
    oled.text("REPL mode", 28, 68, 6)
    oled.show()
    print("@BYE")
except Exception as e:
    oled.fill(0)
    oled.text("ERROR", 44, 52, 15)
    oled.text(str(e)[:16], 0, 68, 8)
    oled.show()
    sys.print_exception(e)
finally:
    micropython.kbd_intr(3)
    if dbg[0] is not None:
        dbg[0].close()
    for p in (enc_a, enc_b):
        p.irq(None)
