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
#   "@W 192.168.1.20"         WiFi status (SETUP > GRAINVIEW > IP; also after 'H')
#   "@D <seq> <status> <n>" + n raw bytes   SWD reply (status 0 ok, 1 = n bytes of error text)
#
# WiFi (gvnet.py, unless SETUP > GRAINVIEW > WiFi is OFF): the same panel in a browser - the
# OLED's frames out, presses in, as if on the panel (the Mac hears them too).
#
# Ctrl-C is disabled while running (frames are binary). Escape hatch: hold BACK while
# plugging in and it stops before taking over, leaving the REPL free.
import array
import gc
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

# --- encoder: Gray-code decoder in a hard IRQ, one step per detent (rest A=B=1); the
# table's sign is anticlockwise-positive with this wiring, flipped below ---
enc_a, enc_b = inp(pins.ENC_A), inp(pins.ENC_B)
TR = array.array('b', (0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0))
es = array.array('i', [(enc_a() << 1) | enc_b(), 0, 0])     # prev state, accumulator, steps

def enc_irq(_):
    cur = (enc_a() << 1) | enc_b()
    prev = es[0]
    if cur != prev:
        es[1] += TR[(prev << 2) | cur]
        es[0] = cur
        if cur == 3:                          # clockwise = +1 (down / next / up a value)
            if es[1] >= 2:
                es[2] -= 1
            elif es[1] <= -2:
                es[2] += 1
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
GC_FREE = 120_000                             # collect (at a poll, not mid-frame) below this
VTREF_MIN = 49648                             # ADC counts for 2.5 V
WRITES = (0x77, 0x62, 0x68, 0x75, 0x69, 0x47)  # w b h u i G: the next 'S' polls afresh
dbg = [None]                                  # the SWD object
mg = {"poll": None, "auto": True, "stale": True, "err": "connecting", "at": 0, "next": 0,
      "full_at": None,                        # last poll of all 8 sounds (else: the focused one)
      "mac_at": None,                         # last 'S': while the Mac reads, poll all 8
      "fix": None,                            # a load's 2nd half, due later (mgfile.fix)
      "fw": None, "fwc": None}                # firmware: True = ours, False = another build,
                                              # None = not known (yet); fwc = the check running
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

def mg_poll(full=False):
    """Poll the Multigrain now: all 8 sounds for the Mac ('S'), else just the selected one
    (all our UI shows; ~1/4 the time, so WAVE's animation doesn't stall). A failure is
    kept for 'S' and retried after RETRY_MS. Nothing is read until the module's firmware
    is known to be ours (mgfw.py, run by fw_step()); it's checked again after a reset."""
    import mgfw
    now = time.ticks_ms()
    try:
        if mg["err"] is not None:             # (re)connect first
            if vtref.read_u16() < VTREF_MIN:
                raise RuntimeError("Multigrain off")
            mg_link(dbg[0].khz if dbg[0] else 8000)
        if mgfw.was_reset(dbg[0]):
            mg["fw"] = mg["fwc"] = None
        if mg["fw"] is None and mg["fwc"] is None:
            mg["fwc"] = mgfw.Check()          # (the first poll after a (re)connect too)
        if mg["fw"] is True:
            if mg["fix"] is not None:
                mg_fix()
            mac = mg["mac_at"] is not None and time.ticks_diff(now, mg["mac_at"]) < 1000
            full = full or mac
            mg["poll"].read(focus=not full)
            gv["perf"][3] += 1
            gv["perf"][4] += time.ticks_diff(time.ticks_ms(), now)
            if full:
                mg["full_at"] = now
        mg["err"] = None
        mg["next"] = time.ticks_add(now, POLL_MS)
    except Exception as e:                    # SWDError, a module mid-reset, ...
        mg["err"] = str(e) or type(e).__name__
        mg["next"] = time.ticks_add(now, RETRY_MS)
        mg["fw"] = mg["fwc"] = None           # gone: check its firmware again when it's back
    mg["at"], mg["stale"] = now, False
    ui_data()
    if gc.mem_free() < GC_FREE:               # ~17 ms: here, not mid-animation, and only when
        t = time.ticks_us()                   # needed (the grain maths makes ~300 KB/s of
        gc.collect()                          # garbage), so the heap stays in one piece
        gv["perf"][7] += time.ticks_diff(time.ticks_us(), t)

def fw_step():
    """The next piece of the firmware check (mgfw.Check); when it's done, poll at once."""
    try:
        r = mg["fwc"].step(dbg[0])
    except Exception as e:                    # the link went: reconnect + check again
        mg["fwc"], mg["err"] = None, str(e) or type(e).__name__
        mg["next"] = time.ticks_add(time.ticks_ms(), RETRY_MS)
        return
    if r is not None:
        mg["fwc"], mg["fw"], mg["stale"] = None, r, True
        mg["next"] = time.ticks_ms()

def mg_live():
    """Is there a poll to show: linked, and the firmware checked as ours?"""
    p = mg["poll"]
    return mg["err"] is None and mg["fw"] is True and p is not None and p.snap is not None

def mg_down():
    """The snapshot while there's no poll to show: no link, or the firmware being checked
    ("fw": "checking") / not ours ("fw": "unknown": we don't read or write it then)."""
    if mg["err"] is not None or dbg[0] is None:
        return {"mode": "swd", "connected": False, "error": mg["err"]}
    import mg_map as M
    fw = "unknown" if mg["fw"] is False else "checking"
    return {"mode": "swd", "connected": False, "fw": fw, "error":
            "unknown Multigrain firmware (GRAINVIEW is for %s)" % M.FW_VERSION
            if mg["fw"] is False else "checking the Multigrain's firmware"}

def mg_json(file=None):
    """The latest poll as JSON pieces (see Poller.json), + "_file" if given."""
    if mg_live():
        js = mg["poll"].json()
        if file is None:
            return js
        return js[:-1] + [js[-1][:-1] + b', "_file": ' + json.dumps(file).encode() + b"}"]
    return [json.dumps(mg_down()).encode()]

def mg_select(n):
    """Edit focus -> sound n, no halt: mg_load.select_nohalt's two writes."""
    import mg_map as M
    s = dbg[0]
    if mg["err"] is not None or s is None:
        raise RuntimeError("NO MODULE LINK")
    s.write8(M.CUR_SOUND, n)
    s.write8(M.STATE + 0x11, s.read_block8(M.STATE + 0x08, 1)[0])
    mg_poll()                                 # show it at once

def mg_scene(sc):
    """Edited scene -> "A"/"B", no halt: grainview_server.set_scene's two writes (the setter
    FUN_080114e4's stores without its notify; panel A/B + knob LEDs follow)."""
    import mg_map as M
    s = dbg[0]
    s.write8(M.EDIT_SCENE, 1 if sc == "B" else 0)
    s.write8(M.STATE + 0x30, 0)
    mg_poll()

def mg_play(timeout_ms=500):
    """Playback -> the selected sound: mg_load.post_event_nohalt(EV_PLAY_SELECTED). The
    firmware posts events with |= and the engine fetch-and-clears them each tick, so we
    only write when the word reads 0, then wait for the engine to take it."""
    import mg_map as M
    s, bit = dbg[0], 1 << M.EV_PLAY_SELECTED
    if mg["err"] is not None or s is None:
        raise RuntimeError("NO MODULE LINK")
    t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < timeout_ms:
        if s.read32(M.EVENTS) == 0:
            s.write32(M.EVENTS, bit)
            while time.ticks_diff(time.ticks_ms(), t0) < timeout_ms:
                if not s.read32(M.EVENTS) & bit:
                    mg_poll()
                    return
                time.sleep_ms(1)
            break
        time.sleep_ms(1)
    raise RuntimeError("play: try again")

def mg_do(act):
    """A UI action (gv_ui.UI.btn) on the module -> its result, or raises with the reason."""
    s, k = dbg[0], act[0]
    if not mg_live():
        raise RuntimeError(mg_down()["error"] or "NO MODULE LINK")
    if k == "select":
        mg_select(act[1])
        if act[2]:                            # SETUP > GRAINVIEW > Sel plays
            mg_play()
        return None
    if k == "scene":
        mg_scene(act[1])
        return None
    if k == "rec":
        import mgrec
        mgrec.rec_do(s, act[1], act[2])
        mg_poll()
        return None
    if k == "live":
        import mgrec
        mgrec.set_live(s, act[1], act[2])
        mg["poll"].st_for = None              # its settings (Type) re-read at once (keeping
                                              # the cache: st = None would lose module / preset)
        mg_poll()
        return None
    if k == "set":                            # ("set", key, value, sound or None)
        import mgset
        mgset.write(s, act[1], act[2], act[3])
        mg["poll"].st_for = None              # (as Live: re-read the settings at once)
        mg_poll()
        return None
    import mgfile as F
    if k == "root":
        return F.counts(s)
    if k == "files":
        return F.files(s, act[1] or None)
    mg["stale"] = True
    if k == "load":
        mg["fix"] = F.load(s, act[1] or None, act[2])
    elif act[1] == "preset":
        F.preset(s, act[2], act[3])
    else:
        F.project(s, act[2], act[3])
    return None

def mg_fix():
    """An empty sound loaded from another folder got reset to file 0: once that's done,
    load the file asked for (mgfile.fix; checked at each poll)."""
    import mgfile as F
    try:
        if F.fix(dbg[0], mg["fix"]):
            mg["fix"] = None
    except Exception as e:
        mg["fix"] = None
        if gv["ui"] is not None:
            gv["ui"].flash(str(e) or type(e).__name__)

# --- the Pico's own UI (gv_ui.py) ---
MAC_MS = 3000                                 # no Mac frame for this long -> our own UI
FRAME_MS = 33                                 # WAVE's grain animation, ~30 fps
gv = {"ui": None, "mac_at": None, "own": False, "frame": 0, "net": None,
      "perf": [0, 0, 0, 0, 0, time.ticks_ms(), 0, 0, 0, 0, 0]}  # anim frames, anim us, push us,
                    # polls, poll ms, since, all frames pushed, gc us, loops, last push, max gap

def ui_snap():
    return mg["poll"].snap if mg_live() else mg_down()

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
        gv["ui"].net, gv["ui"].on_wifi = gv["net"], net_set
    gv["ui"].render(ui_snap())
    ui_push()
    gv["frame"] = time.ticks_add(time.ticks_ms(), FRAME_MS)   # this was a frame too

def ui_data():
    """A poll came in: an animating WAVE takes it at its next frame (no extra redraw, so
    the frame cadence holds); anything else redraws now."""
    ui = gv["ui"]
    if ui is not None and gv["own"] and ui_own() and ui.view == "WAVE":
        ui.update(ui_snap())
        if ui.animating():
            return
    ui_draw()

def ui_push(rows=None):
    """Send what changed in the UI's frame to the panel: rows = (r0, n) when the caller
    knows (the animation: no compare, no allocation), else the changed band."""
    a, b = gv["ui"].buf, oled.buffer
    if not gv["own"]:                         # taking the screen back: send it all
        gv["own"] = True
        b[:] = a
        oled.show()
        return
    if rows is None:
        if a == b:
            return
        r0 = 0
        while a[r0 * BPR:(r0 + 1) * BPR] == b[r0 * BPR:(r0 + 1) * BPR]:
            r0 += 1
        r1 = 127
        while a[r1 * BPR:(r1 + 1) * BPR] == b[r1 * BPR:(r1 + 1) * BPR]:
            r1 -= 1
        rows = (r0, r1 - r0 + 1)
    r0, n = rows
    fb[r0 * BPR:(r0 + n) * BPR] = memoryview(a)[r0 * BPR:(r0 + n) * BPR]
    oled.show_rows(r0, n)
    pf, t = gv["perf"], time.ticks_ms()
    pf[6] += 1
    if pf[9]:
        pf[10] = max(pf[10], time.ticks_diff(t, pf[9]))
    pf[9] = t

def ui_key(name):
    if not ui_own() or gv["ui"] is None:
        return
    act = gv["ui"].btn(name)
    if act:
        ui_act(act)
    ui_draw()

def ui_act(act):
    ui = gv["ui"]
    if act[0] == "files":
        ui_draw()                             # "loading list..." while the names are read
    try:
        res = mg_do(act)
    except Exception as e:
        ui.done(act, err=str(e) or type(e).__name__)
    else:
        ui.done(act, res)

def ui_file_live():
    """FILE as it opens on the selected sound's folder (the 'v' FILE check), else the root."""
    import mgfile as F
    try:
        folder, cur, names = F.files(dbg[0])
    except Exception:
        return {"folder": "ROOT", "cur": 0}
    return {"folder": folder, "files": names, "cur": max(0, min(len(names) - 1, cur)) if names else -1}

def ui_enc(n):
    if ui_own() and gv["ui"] is not None:
        gv["ui"].enc(n)
        ui_draw()

# --- WiFi: the panel in a browser (gvnet.py) ---
net = [None]
KEYS = [name for name, _ in buttons]

def net_key(k):
    """A press from a browser = the panel's own (steps, or a button name)."""
    if isinstance(k, int):
        print("@E %+d" % k)
        ui_enc(k)
    elif k in KEYS:
        print("@B %s 1" % k)
        print("@B %s 0" % k)
        ui_key(k)

def net_set(on):
    """WiFi on / off: at power-up, and SETUP > GRAINVIEW > WiFi (whose redraw follows)."""
    if on and net[0] is None:
        import gvnet
        try:
            net[0] = gvnet.Net(oled.buffer, net_key)
        except Exception as e:                # no radio / bad wifi.json: the panel goes on
            sys.print_exception(e)
            net_show("ERROR", False)
            return
    elif not on and net[0] is not None:
        net[0].stop()
        net[0] = None
    net_show(None, False)

def net_show(text=None, draw=True):
    """The WiFi status -> SETUP > GRAINVIEW > IP + the Mac, when it changes."""
    text = text or (net[0].text if net[0] else "OFF")
    if text != gv["net"]:
        gv["net"] = text
        print("@W " + text)
        if gv["ui"] is not None:
            gv["ui"].net = text
            if draw and gv["ui"].overlay == "SETUP":
                ui_draw()

def swd_op(op, body):
    """One SWD request -> reply bytes. All little-endian; addresses/words u32.
    c khz(u16) -> DPIDR      r addr n -> n bytes      w addr words...      b addr bytes...
    h -> DHCSR (halted)      u (resume)               g regs(u8)... -> words
    i lo hi tries(u16) -> pc xpsr, halted with pc in lo..hi (or b"": missed, running)
    G (reg u8, word)...      x (release the pins, stop polling until the next c)
    S -> the latest poll as JSON (polls first if a write came in or it's > FRESH_MS old)
    v [view] -> our UI rendered from the latest poll (8192 bytes) + that poll as JSON
    (view "SETUP" = the SETUP overlay; a snapshot's "_setup" opens a group / row in it;
    view "FILE" = FILE on the selected sound's folder, read from the module, "_file" in the JSON)
    v snapshot JSON (+ "_view") -> just the frame, for that snapshot (tests; the panel
                 stays live; the JSON is parsed in place: no copy from a busy heap)
    P -> UI / poll timing since the last P, as JSON
    (test renders start the grain dots afresh at clock 0 unless the snapshot scripts them)"""
    if op in WRITES:
        if mg["fw"] is not True:              # not on a firmware we don't know (or yet)
            raise RuntimeError(mg_down()["error"] or "NO MODULE LINK")
        mg["stale"] = True
    if op == 0x63:                            # 'c'
        mg["auto"], mg["stale"] = True, True
        dpidr = mg_link(struct.unpack("<H", body)[0])
        mg["err"] = None
        return struct.pack("<I", dpidr)
    if op == 0x78:                            # 'x'
        if dbg[0] is not None:
            dbg[0].close()
        dbg[0] = mg["poll"] = mg["fw"] = mg["fwc"] = None
        mg["auto"], mg["err"] = False, "SWD released"
        return b""
    if op == 0x53:                            # 'S'
        mg["mac_at"] = time.ticks_ms()
        fa = mg["full_at"]
        if mg["auto"] and (mg["stale"] or fa is None or mg["at"] != fa
                           or time.ticks_diff(time.ticks_ms(), fa) > FRESH_MS):
            mg_poll(full=True)
        return mg_json()
    if op == 0x50:                            # 'P'
        f, au, pu, n, pm, t0, frames, gu, loops, _, gap = gv["perf"]
        now = time.ticks_ms()
        gv["perf"] = [0, 0, 0, 0, 0, now, 0, 0, 0, 0, 0]
        secs = max(1, time.ticks_diff(now, t0)) / 1000
        return json.dumps({"secs": secs, "fps": frames / secs, "anim_ms": au / max(1, f) / 1000,
                           "push_ms": pu / max(1, f) / 1000, "polls": n,
                           "poll_ms": pm / max(1, n), "gc_ms": gu / max(1, n) / 1000,
                           "anim_fps": f / secs, "loops": loops / secs, "max_gap_ms": gap,
                           "free": gc.mem_free()}).encode()
    if op == 0x76:                            # 'v'
        if gv["ui"] is None:
            from gv_ui import UI
            gv["ui"] = UI()
        given = body[:1] == b"{"
        snap = json.loads(body) if given else dict(ui_snap())
        view = snap.pop("_view", None) if given else bytes(body).decode()
        del body
        if view == "SETUP":                   # the overlays (on the current view)
            snap.setdefault("_setup", [None, 0, 0])
        elif view == "FILE":
            if "_file" not in snap:
                snap["_file"] = {"folder": "ROOT", "cur": 0} if given else ui_file_live()
        elif view:
            gv["ui"].view = view
        snap.setdefault("_steps", [0])
        gv["ui"].render(snap)
        out = [bytes(gv["ui"].buf)] + ([] if given else mg_json(snap.get("_file")))
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
    if n > 4096:
        gc.collect()                          # big test snapshots: room in one piece
    try:
        body = inb.read(n) if n else b""      # bytes: json.loads takes it as it is
    except MemoryError:                       # no room: drop it (drained), say so, keep going
        body = None
        while n:
            n -= len(inb.read(min(n, 512)))
    try:
        if body is None:
            raise MemoryError("packet too big for the heap")
        out, st = swd_op(op, body), 0         # bytes, or a list of pieces
    except Exception as e:                    # SWDError, bad args: report, keep running
        out, st = str(e).encode(), 1
    if not isinstance(out, list):
        out = [out]
    sys.stdout.buffer.write(("@D %d %d %d\n" % (seq, st, sum(len(b) for b in out))).encode())
    for b in out:
        sys.stdout.buffer.write(b)

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
        if gv["net"]:
            print("@W " + gv["net"])
    elif t == 0x44:                           # 'D'
        swd_packet()
    elif t == 0x51:                           # 'Q'
        raise SystemExit

state = [p() for _, p in buttons]
changed = [0] * len(buttons)

# SOUND< + SOUND> held together = "LIVE" (toggle the sound's Live mode). So a lone SOUND
# key acts when it's let go (unless it was part of the chord), and the Mac hears the
# resolved key (@B SOUND< / @B LIVE), not the raw presses.
SND = ("SOUND<", "SOUND>")
snd = [False, None]                           # chord on; the lone key down (acts on release)

def snd_key(name, down):
    # the other key as debounced (not its raw pin: let go of both at once and the raw pin
    # is up before its own release is handled - the chord would end early and that
    # release then count as a lone press, moving the sound)
    held = state[KEYS.index(SND[name == SND[0]])] == 0
    if down:
        if snd[0]:
            return
        if not held:                          # alone so far: wait for its release
            snd[1] = name
            return
        snd[0], snd[1] = True, None           # the other one is held: the chord
        name = "LIVE"
    elif snd[0]:
        if not held:                          # both up: the chord's over
            snd[0] = False
        return
    elif snd[1] != name:                      # no lone press of this key to finish
        return
    else:
        snd[1] = None
    print("@B %s 1" % name)
    print("@B %s 0" % name)
    ui_key(name)
try:
    with open("gv_cfg.json") as f:            # gv_ui's settings: WiFi unless it's OFF
        wifi = json.load(f).get("wifi", 1) != 0
except (OSError, ValueError):
    wifi = True
net_set(wifi)                                 # (~1 s: the radio boots; the splash stays)
micropython.kbd_intr(-1)
try:
    while True:
        gv["perf"][8] += 1
        if net[0] is not None:
            try:
                net[0].step()
            except Exception as e:            # a browser's trouble is never the panel's
                sys.print_exception(e)
            net_show()
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
                if name in SND:               # chord-aware: see snd_key()
                    snd_key(name, not v)
                    continue
                print("@B %s %d" % (name, 1 - v))
                if not v:
                    ui_key(name)
        if poller.poll(2):
            packet()
        elif mg["fwc"] is not None and mg["err"] is None:
            fw_step()                         # a chunk of the firmware check (~12 ms)
            if mg["fwc"] is None:
                mg_poll()                     # done: show the outcome / the module now
        elif mg["auto"] and time.ticks_diff(now, mg["next"]) >= 0:
            mg_poll()
        elif not gv["own"] and ui_own() or gv["ui"] and gv["ui"].wake_due():
            ui_draw()                         # the Mac went quiet / a flash box ran out
        elif gv["own"] and time.ticks_diff(now, gv["frame"]) >= 0:
            late = time.ticks_diff(now, gv["frame"])
            gv["frame"] = time.ticks_add(gv["frame"] if late < FRAME_MS else now, FRAME_MS)
            t0 = time.ticks_us()
            rows = gv["ui"].animate()         # WAVE: the next grain frame
            if rows:
                t1 = time.ticks_us()
                ui_push(rows)
                pf = gv["perf"]
                pf[0] += 1
                pf[1] += time.ticks_diff(t1, t0)
                pf[2] += time.ticks_diff(time.ticks_us(), t1)
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
    if net[0] is not None:
        net[0].stop()
    if dbg[0] is not None:
        dbg[0].close()
    for p in (enc_a, enc_b):
        p.irq(None)
