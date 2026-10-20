# GRAINVIEW (autostarts on power-up).
# Polls the Multigrain itself over SWD (mgpoll.py, every POLL_MS while VTREF says it's
# powered) and draws its own UI from that (gv_ui.py, a port of the emulator). While the Mac
# sends frames (tools/grainview_server.py + the emulator in a browser) it shows those
# instead, until none came for MAC_MS. Buttons + encoder always go to the Mac too; the Mac
# fetches the poll snapshot with 'S' instead of reading the module itself.
#
# Mac -> Pico, binary packets:  A5 5A <type> <payload>
#   'F' + 8192 bytes          full frame, 128x128, 2 px per byte, left px in the high nibble
#   'R' + r0 + n + n*64 bytes rows r0..r0+n-1
#   'C' + 1 byte              contrast
#   'H'                       hello -> replies "@HELLO 1"
#   'Q'                       quit to the REPL (lets mpremote in; tools/gv_pico.py does this)
#   'D' + seq + op + len(u16) + body    SWD to the Multigrain (pico/swd.py), see swd_op()
#                             (op 'S' = the latest poll snapshot as JSON, 'v' = a UI frame)
# Pico -> Mac, text lines:  "@E +1" (encoder steps)  "@B BACK 1" (button down / 0 = up)
#   "@D <seq> <status> <n>" + n raw bytes   SWD reply (status 0 ok, 1 = n bytes of error text)
#
# Ctrl-C is disabled while running (frames are binary). Escape hatch: hold BACK while
# plugging in and it stops before taking over, leaving the REPL free.
import array
import json
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
oled.text("GRAINVIEW", 28, 60, 15)
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

# --- SWD (to the Multigrain through J3 -> JTRACE) + the Pico's own poll ---
POLL_MS, RETRY_MS, FRESH_MS = 200, 2000, 100
VTREF_MIN = 49648                             # ADC counts for 2.5 V
WRITES = (0x77, 0x62, 0x68, 0x75, 0x69, 0x47)  # w b h u i G: the next 'S' polls afresh
dbg = [None]                                  # the SWD object
mg = {"poll": None, "auto": True, "stale": True, "err": "connecting", "at": 0, "next": 0}
vtref = machine.ADC(pins.VTREF)

def mg_link(khz=8000):
    """(Re)connect SWD at khz; the poller follows the SWD object. Returns DPIDR."""
    s = dbg[0]
    if s is None or s.khz != khz:
        if s is not None:
            s.close()
        from swd import SWD
        s = dbg[0] = SWD(khz=khz, clk=pins.SWCLK, dio=pins.SWDIO)
    dpidr = s.connect()
    if mg["poll"] is None or mg["poll"].s is not s:
        from mgpoll import Poller
        mg["poll"] = Poller(s)
    return dpidr

def mg_poll():
    """Poll the Multigrain now. A failure is kept for 'S' and retried after RETRY_MS."""
    now = time.ticks_ms()
    try:
        if mg["err"] is not None:             # (re)connect first
            if vtref.read_u16() < VTREF_MIN:
                raise RuntimeError("Multigrain off")
            mg_link(dbg[0].khz if dbg[0] else 8000)
        mg["poll"].read()
        mg["err"] = None
        mg["next"] = time.ticks_add(now, POLL_MS)
    except Exception as e:                    # SWDError, a module mid-reset, ...
        mg["err"] = str(e) or type(e).__name__
        mg["next"] = time.ticks_add(now, RETRY_MS)
    mg["at"], mg["stale"] = now, False
    ui_draw()

def mg_json():
    p = mg["poll"]
    if mg["err"] is None and p is not None and p.snap is not None:
        return p.json()
    return json.dumps({"mode": "swd", "connected": False, "error": mg["err"]}).encode()

def mg_select(n):
    """Edit focus -> sound n, no halt: mg_load.select_nohalt's two writes."""
    import mg_map as M
    s = dbg[0]
    if mg["err"] is not None or s is None:
        raise RuntimeError("NO MODULE LINK")
    s.write8(M.CUR_SOUND, n)
    s.write8(M.STATE + 0x11, s.read_block8(M.STATE + 0x08, 1)[0])
    mg_poll()                                 # show it at once

# --- the Pico's own UI (gv_ui.py) ---
MAC_MS = 3000                                 # no Mac frame for this long -> our own UI
gv = {"ui": None, "mac_at": None, "own": False}

def ui_snap():
    p = mg["poll"]
    if mg["err"] is None and p is not None and p.snap is not None:
        return p.snap
    return {"connected": False, "error": mg["err"]}

def ui_own():
    m = gv["mac_at"]
    return m is None or time.ticks_diff(time.ticks_ms(), m) > MAC_MS

def ui_draw():
    """Render our UI and send the changed rows, unless the Mac has the screen."""
    if not ui_own():
        gv["own"] = False
        return
    if gv["ui"] is None:
        from gv_ui import UI
        gv["ui"] = UI()
    ui = gv["ui"]
    ui.render(ui_snap())
    a, b = ui.buf, oled.buffer
    if not gv["own"]:                         # taking the screen back: send it all
        gv["own"] = True
        b[:] = a
        oled.show()
        return
    if a == b:
        return
    r0 = 0
    while a[r0 * BPR:(r0 + 1) * BPR] == b[r0 * BPR:(r0 + 1) * BPR]:
        r0 += 1
    r1 = 127
    while a[r1 * BPR:(r1 + 1) * BPR] == b[r1 * BPR:(r1 + 1) * BPR]:
        r1 -= 1
    b[r0 * BPR:(r1 + 1) * BPR] = a[r0 * BPR:(r1 + 1) * BPR]
    oled.show_rows(r0, r1 - r0 + 1)

def ui_key(name):
    if not ui_own() or gv["ui"] is None:
        return
    act = gv["ui"].btn(name)
    if act and act[0] == "select":
        try:
            mg_select(act[1])
        except Exception as e:
            gv["ui"].flash(str(e) or type(e).__name__)
    ui_draw()

def ui_enc(n):
    if ui_own() and gv["ui"] is not None:
        gv["ui"].enc(n)
        ui_draw()

def swd_op(op, body):
    """One SWD request -> reply bytes. All little-endian; addresses/words u32.
    c khz(u16) -> DPIDR      r addr n -> n bytes      w addr words...      b addr bytes...
    h -> DHCSR (halted)      u (resume)               g regs(u8)... -> words
    i lo hi tries(u16) -> pc xpsr, halted with pc in lo..hi (or b"": missed, running)
    G (reg u8, word)...      x (release the pins, stop polling until the next c)
    S -> the latest poll as JSON (polls first if a write came in or it's > FRESH_MS old)
    v [view] -> our UI rendered from the latest poll (8192 bytes) + that poll as JSON
    v view \n snapshot JSON -> the same for that snapshot (tests; the panel stays live)"""
    if op in WRITES:
        mg["stale"] = True
    if op == 0x63:                            # 'c'
        mg["auto"], mg["stale"] = True, True
        dpidr = mg_link(struct.unpack("<H", body)[0])
        mg["err"] = None
        return struct.pack("<I", dpidr)
    if op == 0x78:                            # 'x'
        if dbg[0] is not None:
            dbg[0].close()
        dbg[0] = mg["poll"] = None
        mg["auto"], mg["err"] = False, "SWD released"
        return b""
    if op == 0x53:                            # 'S'
        if mg["auto"] and (mg["stale"] or time.ticks_diff(time.ticks_ms(), mg["at"]) > FRESH_MS):
            mg_poll()
        return mg_json()
    if op == 0x76:                            # 'v'
        if gv["ui"] is None:
            from gv_ui import UI
            gv["ui"] = UI()
        view, _, js = bytes(body).partition(b"\n")
        if view:
            gv["ui"].view = view.decode()
        gv["ui"].render(json.loads(js) if js else ui_snap())
        out = bytes(gv["ui"].buf) + (js or mg_json())
        ui_draw()
        return out
    s = dbg[0]
    if s is None:
        raise RuntimeError("SWD not connected")
    if op == 0x72:                            # 'r'
        a, n = struct.unpack("<II", body)
        return s.read_block8(a, n)
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
        gv["mac_at"], gv["own"] = time.ticks_ms(), False
    elif t == 0x52:                           # 'R'
        read_into(hdr)
        r0, n = hdr[0], hdr[1]
        if r0 + n <= 128 and n:
            read_into(fb[r0 * BPR:(r0 + n) * BPR])
            oled.show_rows(r0, n)
            gv["mac_at"], gv["own"] = time.ticks_ms(), False
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
            ui_enc(n)
        now = time.ticks_ms()
        for i, (name, p) in enumerate(buttons):
            v = p()
            if v != state[i] and time.ticks_diff(now, changed[i]) > 20:
                state[i] = v
                changed[i] = now
                print("@B %s %d" % (name, 1 - v))
                if not v:
                    ui_key(name)
        if poller.poll(2):
            packet()
        elif mg["auto"] and time.ticks_diff(now, mg["next"]) >= 0:
            mg_poll()
        elif not gv["own"] and ui_own() or gv["ui"] and gv["ui"].flash_due():
            ui_draw()                         # the Mac went quiet / a flash box ran out
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
