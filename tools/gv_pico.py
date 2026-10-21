#!/usr/bin/env python3
"""gv_pico.py - the GRAINVIEW Pico as a USB screen + keys + SWD probe.

The Pico runs pico/main.py: it shows the 128x128 frames we send and reports its
buttons and encoder as text lines. grainview_server.py uses PicoLink to forward the
emulator's frames and pass the key events back to the browser (GET /events).
PicoTarget drives the Pico's SWD master (pico/swd.py) over the same link, shaped like
the pyOCD target the mg_* helpers use, so they run without the ST-Link. The Pico also
polls the module itself (pico/mgpoll.py); PicoTarget.snapshot() fetches that.

CLI:
    tools/venv/bin/python tools/gv_pico.py deploy   # regenerate pico/mg_map.py, copy pico/*.py
                                                    # + the web page (gzipped) + pico/wifi.json
                                                    # to the board + restart it
    tools/venv/bin/python tools/gv_pico.py quit     # stop the screen, free the REPL for mpremote
    tools/venv/bin/python tools/gv_pico.py keys     # print key events (screen test)
    tools/venv/bin/python tools/gv_pico.py swd      # SWD over the Pico: IDs + timings (read-only)
    tools/venv/bin/python tools/gv_pico.py poll     # the Pico's own poll vs the Mac's decode
    tools/venv/bin/python tools/gv_pico.py ui [VIEW...]   # the Pico's UI vs the emulator, pixel
                                                    # for pixel (+ tmp/gv_ui_VIEW.png)
    tools/venv/bin/python tools/gv_pico.py ui --all-sounds   # same for sounds 1-8 (moves the
                                                    # edit focus through them, then back)
    tools/venv/bin/python tools/gv_pico.py ui --cases        # same for made-up edge cases
                                                    # (mod routings, scene B, empty...)
"""
import argparse
import glob
import gzip
import json
import os
import queue
import struct
import subprocess
import tempfile
import zlib
import sys
import threading
import time

import serial
import serial.tools.list_ports

HERE = os.path.dirname(os.path.abspath(__file__))
PICO_DIR = os.path.join(os.path.dirname(HERE), "pico")
VID = 0x2E8A                        # Raspberry Pi (MicroPython rp2 = 2E8A:0005)
MAGIC = b"\xA5\x5A"
W, H = 128, 128
FRAME = W * H // 2                  # 2 px per byte
BPR = W // 2
SWD_CHUNK = 16384                   # max bytes per SWD read request (Pico heap)


def find_port():
    for p in serial.tools.list_ports.comports():
        if p.vid == VID:
            return p.device
    return None


def quit_screen(port=None):
    """Ask main.py to drop to the REPL (Ctrl-C is disabled while it runs)."""
    port = port or find_port()
    if not port:
        raise SystemExit("no Pico found")
    with serial.Serial(port, timeout=0.5) as s:
        s.write(MAGIC + b"Q")
        s.flush()
        time.sleep(0.3)


class PicoSWDError(RuntimeError):
    pass


class PicoLink:
    """Background serial link. Thread-safe send_frame() and swd(); subscribe() for
    key events."""

    def __init__(self, port=None, log=print):
        self.port_arg, self.log = port, log
        self.ser = None
        self.port = None
        self.lock = threading.Lock()
        self.subs = []
        self.last = None            # last frame from the browser (re-sent on reconnect)
        self.sent = None            # what the panel shows now
        self.frames = 0
        self.wifi = None            # the Pico's WiFi status ("@W ...")
        self.swd_lock = threading.Lock()    # one SWD request in flight
        self.seq = 0
        self.replies = queue.Queue()
        threading.Thread(target=self._run, daemon=True).start()

    # ----- status / events -----
    def status(self):
        return {"connected": self.ser is not None, "port": self.port, "frames": self.frames,
                "wifi": self.wifi}

    def subscribe(self):
        q = queue.Queue(maxsize=256)
        with self.lock:
            self.subs.append(q)
        return q

    def unsubscribe(self, q):
        with self.lock:
            if q in self.subs:
                self.subs.remove(q)

    def _emit(self, ev):
        with self.lock:
            subs = list(self.subs)
        for q in subs:
            try:
                q.put_nowait(ev)
            except queue.Full:
                pass

    # ----- frames -----
    def send_frame(self, data):
        if len(data) != FRAME:
            raise ValueError(f"frame must be {FRAME} bytes, got {len(data)}")
        with self.lock:
            self.last = bytes(data)
            self._push()

    def _push(self):                # lock held
        if self.ser is None or self.last is None or self.last == self.sent:
            return
        new, old = self.last, self.sent
        if old is None:
            pkt = MAGIC + b"F" + new
        else:                       # only the changed band of rows
            rows = [r for r in range(H) if new[r * BPR:(r + 1) * BPR] != old[r * BPR:(r + 1) * BPR]]
            r0, r1 = rows[0], rows[-1]
            pkt = MAGIC + b"R" + bytes([r0, r1 - r0 + 1]) + new[r0 * BPR:(r1 + 1) * BPR]
        try:
            self.ser.write(pkt)
            self.sent = new
            self.frames += 1
        except (serial.SerialException, OSError) as e:
            self._drop(e)

    # ----- SWD -----
    def swd(self, op, body=b"", timeout=2.0):
        """One SWD request (see swd_op() in pico/main.py) -> reply bytes."""
        with self.swd_lock:
            self.seq = (self.seq + 1) & 0xFF
            with self.lock:
                if self.ser is None:
                    raise PicoSWDError("Pico not connected")
                try:
                    self.ser.write(MAGIC + b"D" + bytes([self.seq, ord(op)])
                                   + struct.pack("<H", len(body)) + body)
                except (serial.SerialException, OSError) as e:
                    self._drop(e)
                    raise PicoSWDError(f"Pico write failed ({e})") from None
            end = time.time() + timeout
            while True:
                try:
                    seq, ok, data = self.replies.get(timeout=max(0.0, end - time.time()))
                except queue.Empty:
                    raise PicoSWDError(f"no SWD reply from the Pico ({op})") from None
                if seq == self.seq:         # else a late reply to a timed-out request
                    break
        if not ok:
            raise PicoSWDError(data.decode("utf-8", "replace"))
        return data

    def _reply(self, line):         # reader thread: "@D seq status n" + n bytes
        seq, st, n = (int(x) for x in line[3:].split())
        data = b""
        end = time.time() + 2.0
        while len(data) < n and time.time() < end:
            data += self.ser.read(n - len(data))
        if len(data) == n:
            self.replies.put((seq, st == 0, data))

    def _drop(self, why):           # lock held
        if self.ser is not None:
            self.log(f"Pico screen disconnected ({why})")
            try:
                self.ser.close()
            except Exception:        # noqa: BLE001
                pass
        self.ser = None
        self.sent = None

    # ----- reader thread -----
    def _run(self):
        while True:
            if self.ser is None:
                port = self.port_arg or find_port()
                if not port:
                    time.sleep(1.5)
                    continue
                try:
                    s = serial.Serial(port, timeout=0.5, write_timeout=1)
                except (serial.SerialException, OSError):
                    time.sleep(1.5)
                    continue
                with self.lock:
                    self.ser, self.port, self.sent = s, port, None
                    s.write(MAGIC + b"H")
                    self._push()    # show the current emulator frame straight away
                self.log(f"Pico screen connected on {port}")
            try:
                line = self.ser.readline()
            except (serial.SerialException, OSError, TypeError, AttributeError) as e:
                with self.lock:
                    self._drop(e)
                time.sleep(1)
                continue
            if line.startswith(b"@D "):
                try:
                    self._reply(line)
                except (serial.SerialException, OSError, TypeError, AttributeError) as e:
                    with self.lock:
                        self._drop(e)
            elif line:
                self._line(line.decode("utf-8", "replace").strip())

    def _line(self, s):
        if s.startswith("@E "):
            self._emit({"t": "enc", "d": int(s[3:])})
        elif s.startswith("@B "):
            name, _, down = s[3:].rpartition(" ")
            self._emit({"t": "btn", "n": name, "down": down == "1"})
        elif s.startswith("@W "):
            self.wifi = s[3:]       # SETUP > GRAINVIEW > IP (pico/gvnet.py)
        elif s.startswith("@HELLO") or s.startswith("@BYE"):
            pass
        elif s:
            self.log(f"[pico] {s}")  # tracebacks etc.


# Cortex-M core registers by pyOCD name (DCRSR REGSEL)
REGS = {**{f"r{i}": i for i in range(13)}, "sp": 13, "r13": 13, "lr": 14, "r14": 14,
        "pc": 15, "r15": 15, "xpsr": 16, "msp": 17, "psp": 18}


class PicoTarget:
    """SWD through the Pico, with the pyOCD Target methods the mg_* helpers and
    grainview_server use (memory, halt/resume, core registers). Raises PicoSWDError."""

    def __init__(self, link, khz=8000):
        self.link, self.khz = link, khz

    def connect(self):
        """Wake the SW-DP (attach only: no reset, no halt). Returns DPIDR."""
        return struct.unpack("<I", self.link.swd("c", struct.pack("<H", self.khz)))[0]

    def close(self):
        """Give the SWD pins back (the Multigrain keeps running); the Pico stops polling
        until the next connect()."""
        self.link.swd("x")

    def snapshot(self):
        """The Pico's latest poll (pico/mgpoll.py): grainview_server's /state dict."""
        return json.loads(self.link.swd("S", timeout=5))

    # ----- memory -----
    def _read(self, addr, n):
        out = b""
        while len(out) < n:
            k = min(n - len(out), SWD_CHUNK)
            out += self.link.swd("r", struct.pack("<II", addr + len(out), k))
        return out

    def read_memory(self, addr, transfer_size=32):
        n = transfer_size // 8
        if n not in (1, 2, 4) or addr % n:
            raise ValueError(f"bad {transfer_size}-bit read at 0x{addr:08x}")
        return int.from_bytes(self._read(addr, n), "little")

    def read_memory_block8(self, addr, n):
        return list(self._read(addr, n))

    def read_memory_block32(self, addr, n):
        return list(struct.unpack(f"<{n}I", self._read(addr, 4 * n)))

    def write_memory(self, addr, value, transfer_size=32):
        if transfer_size == 32:
            self.write_memory_block32(addr, [value])
        elif transfer_size == 8:
            self.link.swd("b", struct.pack("<IB", addr, value & 0xFF))
        else:
            raise ValueError(f"{transfer_size}-bit writes not supported")

    def write_memory_block32(self, addr, data):
        per = SWD_CHUNK // 4
        for i in range(0, len(data), per):
            words = [v & 0xFFFFFFFF for v in data[i:i + per]]
            self.link.swd("w", struct.pack(f"<I{len(words)}I", addr + 4 * i, *words))

    def write_memory_block8(self, addr, data):
        data = bytes(data)
        for i in range(0, len(data), SWD_CHUNK):
            self.link.swd("b", struct.pack("<I", addr + i) + data[i:i + SWD_CHUNK])

    # ----- core -----
    def halt(self):
        self.link.swd("h")

    def resume(self):
        self.link.swd("u")

    def halt_in(self, lo, hi, tries=200):
        """Pico-side mg_load.wait_idle_and_halt: (pc, xpsr) halted with pc in lo..hi
        in thread mode, or None (still running)."""
        r = self.link.swd("i", struct.pack("<IIH", lo, hi, tries), timeout=tries * 0.01 + 2)
        return struct.unpack("<II", r) if r else None

    def is_halted(self):
        return bool(self.read_memory(0xE000EDF0) & (1 << 17))

    def read_core_registers_raw(self, names):
        regs = bytes(REGS[r] if isinstance(r, str) else r for r in names)
        return list(struct.unpack(f"<{len(regs)}I", self.link.swd("g", regs)))

    def write_core_registers_raw(self, names, values):
        body = b"".join(struct.pack("<BI", REGS[r] if isinstance(r, str) else r, v & 0xFFFFFFFF)
                        for r, v in zip(names, values))
        self.link.swd("G", body)

    def read_core_register(self, name):
        return self.read_core_registers_raw([name])[0]

    def write_core_register(self, name, value):
        self.write_core_registers_raw([name], [value])


def swd_check(port, khz):
    """Read-only: IDs, a flash compare against the .bin, and the server's poll timing."""
    link = PicoLink(port)
    for _ in range(50):
        if link.ser is not None:
            break
        time.sleep(0.1)
    t = PicoTarget(link, khz)
    print(f"DPIDR 0x{t.connect():08X}  CPUID 0x{t.read_memory(0xE000ED00):08X}"
          f"  IDCODE 0x{t.read_memory(0x5C001000):08X}")
    binf = os.path.join(os.path.dirname(HERE), "Multigrain.1.4.8.0.bin")
    t0 = time.time()
    fl = bytes(t.read_memory_block8(0x08000000, 65536))
    dt = time.time() - t0
    with open(binf, "rb") as f:
        same = f.read(65536) == fl
    print(f"flash 64 KB vs {os.path.basename(binf)}: {'MATCH' if same else 'MISMATCH'}"
          f"  ({dt * 1000:.0f} ms, {65536 / dt / 1024:.0f} KB/s)")
    n, t0 = 200, time.time()
    for _ in range(n):
        t.read_memory(0x5C001000)
    print(f"read32 round trip: {(time.time() - t0) / n * 1000:.2f} ms")
    t0 = time.time()
    for k in range(8):                  # grainview_server's per-sound param block
        t.read_memory_block8(0x24020B84 + k * 0x9F0 + 0x48, 0x424 - 0x48)
    print(f"8 sound blocks: {(time.time() - t0) * 1000:.0f} ms")
    t.close()


def diff(a, b, path="", tol=1e-3):
    """Differences between two snapshots (floats within tol count as equal)."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            out += diff(a.get(k, "<missing>"), b.get(k, "<missing>"), f"{path}.{k}", tol)
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in diff(x, y, f"{path}[{i}]", tol)]
    if isinstance(a, float) or isinstance(b, float):
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) <= tol:
            return []
    elif a == b:
        return []
    return [f"{path}: pico {a!r} / mac {b!r}"]


def poll_check(port, khz):
    """The Pico's own snapshot vs grainview_server's decode of the same RAM (read-only)."""
    import threading
    import grainview_server as G
    link = PicoLink(port, log=lambda *a: None)
    for _ in range(50):
        if link.ser is not None:
            break
        time.sleep(0.1)
    t = PicoTarget(link, khz)
    t.connect()
    be = G.SwdBackend.__new__(G.SwdBackend)      # just its decode, no poll thread
    be.t, be.st, be.st_t, be.lock = t, None, 0.0, threading.Lock()
    times = []
    for _ in range(5):
        t0 = time.time()
        pico = t.snapshot()
        times.append((time.time() - t0) * 1000)
        time.sleep(0.2)
    if not pico.get("connected"):
        raise SystemExit(f"Pico poll: {pico.get('error')}")
    mac = be._read_from(t)
    moving = ("live", "morph", "clock_period", "pico_ms")   # change between the two reads
    d = diff({k: v for k, v in pico.items() if k not in moving},
             {k: v for k, v in mac.items() if k not in moving})
    print(f"'S' round trip {min(times):.0f}-{max(times):.0f} ms; Pico poll {pico['pico_ms']} ms")
    print("Pico snapshot = Mac decode" if not d else f"{len(d)} differences:")
    for line in d[:40]:
        print("  " + line)


def png(path, rows):
    """8-bit greyscale PNG from a list of equal-length bytes rows."""
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    w, h = len(rows[0]), len(rows)
    raw = b"".join(b"\0" + r for r in rows)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def unpack(frame):
    """8192 packed bytes (left px = high nibble) -> 128x128 list of 0..15."""
    px = []
    for b in frame:
        px += (b >> 4, b & 15)
    return [px[y * W:(y + 1) * W] for y in range(H)]


def ui_cases(snap):
    """Edge cases the module may not be in right now, made from a live snapshot."""
    import copy
    n = snap["selected"]

    def case(fn):
        s = copy.deepcopy(snap)
        fn(s, s["sounds"][n])
        return s

    def mods(s, d):
        for sc, sign in (("A", 1), ("B", -1)):
            for i, src in enumerate(d["mod"][sc]):
                for j, k in enumerate(d["mod"][sc][src]):
                    if (i + j) % 3 == 0:
                        d["mod"][sc][src][k] = sign * round(((i * 10 + j) % 21) / 20, 4)
    def scene_b(s, d):
        s["edit_scene"] = "B"
        s["playing"] = (n + 1) % 8
    def empty(s, d):
        d["file"] = None
    def unlinked(s, d):
        d["link_rs"] = d["link_sp"] = 0
    def sync(s, d):
        s["sync"] = 1
    def long_name(s, d):
        d["file"] = "a_really_long_sample_name_for_the_header.wav"
    def edges(s, d):                          # extreme knob values
        for sc in "AB":
            for i, k in enumerate(d[sc]):
                d[sc][k] = (-1 if k in ("SCAN", "TONE") else 0) if i % 2 else 1
        s["morph"] = 1.0
    def grains(**knobs):                     # play it for ~1.4 s of scripted time
        def fn(s, d):
            import random
            rng = random.Random(7)
            s["playing"] = n
            d[s["edit_scene"]].update(knobs.get("p", {}))
            for k in ("link_rs", "link_sp"):
                if k in knobs:
                    d[k] = knobs[k]
            if "sync" in knobs:
                s["sync"], s["clock_period"] = 1, knobs["sync"]
            s["_steps"] = list(range(1000, 2400, 33))
            s["_rand"] = [round(rng.random(), 4) for _ in range(1200)]
        return fn
    out = [(name, case(fn)) for name, fn in (("mods", mods), ("sceneB", scene_b), ("empty", empty),
           ("unlinked", unlinked), ("sync", sync), ("longname", long_name), ("edges", edges))]
    shapes = (0.0, 0.2, 0.4, 0.55, 0.75, 0.9, 1.0)   # BELL SINC TRI DECAY RAMP TUKEY SQUARE
    out += [("grains%d" % i, case(grains(p={"SHAPE": v, "SCAN": 0.3, "LEVEL": 0.8})))
            for i, v in enumerate(shapes)]
    out += [("grainsLinked", case(grains(link_rs=1, link_sp=1, p={"RATE": 0.6, "SIZE": 0.2}))),
            ("grainsFree", case(grains(link_rs=0, link_sp=0, p={"RATE": 0.9, "SIZE": 0.1}))),
            ("grainsSync", case(grains(sync=0.25, p={"RATE": 0.7}))),
            ("grainsScan", case(grains(p={"SCAN": -0.9, "START": 0.2, "WRAP": 0.5}))),
            ("grainsDense", case(grains(link_rs=0, p={"RATE": 1.0, "SIZE": 0.9, "PITCH": 0.1})))]
    def touch(k, src=None, val=None, **top):  # that knob just turned
        def fn(s, d):
            sc = s["edit_scene"]
            if src:
                d["mod"][sc][src][k] = 0.42 if val is None else val
            elif val is not None:
                d[sc][k] = val
            s.update(top)
            s["_touch"] = [k, src]
        return fn
    out += [("touch" + name, case(fn)) for name, fn in (
        ("Size", touch("SIZE")), ("Start", touch("START")), ("Wrap", touch("WRAP")),
        ("Scan", touch("SCAN", val=-0.4)), ("Tone", touch("TONE", val=0.6)),
        ("Mod", touch("PITCH", "X", -0.55)), ("Sync", touch("RATE", sync=1, clock_period=0.5)))]

    def turned(*moves, sound=None):          # polls: before, then after these knob moves
        def fn(s, d):
            sc = s["edit_scene"]
            before = copy.deepcopy(s)
            for k, src, dv in moves:
                if src:
                    d["mod"][sc][src][k] = round(d["mod"][sc][src][k] + dv, 4)
                else:
                    d[sc][k] = round(d[sc][k] + dv, 4)
            if sound is not None:
                before["selected"] = sound
            s["_prev"] = [before, copy.deepcopy(before)]
        return fn
    out += [("turn" + name, case(fn)) for name, fn in (
        ("Size", turned(("SIZE", None, 0.02))),
        ("Tiny", turned(("SIZE", None, 0.003))),            # under TOUCH_EPS: nothing
        ("Two", turned(("RATE", None, 0.01), ("PITCH", None, -0.03))),   # the bigger wins
        ("Tie", turned(("WRAP", None, 0.05), ("SCAN", None, -0.05))),    # tie: the first
        ("Bulk", turned(("START", None, 0.1), ("WRAP", None, 0.1), ("SIZE", None, 0.1))),
        ("Mod", turned(("TONE", "Y", 0.2))),
        ("Switch", turned(("SIZE", None, 0.2), sound=(n + 1) % 8)))]     # new sound: silent

    def notes(*on):
        return [i in on for i in range(12)]

    def settings(cur, **vals):                # SETTINGS dived, cursor on row cur
        def fn(s, d):
            s["_dived"], s["_setCur"] = True, cur
            d["settings"].update(vals)
        return fn
    out += [("set" + name, case(fn)) for name, fn in (
        ("Top", settings(0)), ("Fine", settings(5, fine_tune=2.3)), ("End", settings(9)),
        ("QuantMaj", settings(6, quantizer={"notes": notes(0, 2, 4, 5, 7, 9, 11), "root": 0})),
        ("QuantOdd", settings(6, quantizer={"notes": notes(2, 3), "root": 2})),
        ("Chrom", settings(6, quantizer={"notes": notes(*range(12)), "root": 5})),
        ("Unmapped", settings(3, link_sp=None, choke=None)))]

    def setup(g, gc, cur=0, edit=None, gv=None, **vals):   # SETUP overlay open there
        def fn(s, d):
            s["_setup"] = [g, gc, cur]
            if edit is not None:
                s["_edit"] = edit
            if gv:
                s["_gv"] = gv
            for grp, kv in vals.items():
                s["settings"][grp].update(kv)
        return fn
    out += [("setup" + name, case(fn)) for name, fn in (
        ("Groups", setup(None, 0)), ("Preset", setup(None, 1)), ("Soon", setup(None, 2)),
        ("Gv", setup(None, 3)),
        ("Mod", setup(0, 0)), ("ModMid", setup(0, 0, 5)), ("ModEnd", setup(0, 0, 10)),
        ("ModUnmapped", setup(0, 0, 1, module={"next_input": None, "gate_delay": None})),
        ("ModEdit", setup(0, 0, 3, edit=2.5)),
        ("Pre", setup(1, 1, 2)), ("GvTop", setup(3, 3)), ("GvLink", setup(3, 3, 4)),
        ("GvFw", setup(3, 3, 5)), ("GvEdit", setup(3, 3, 1, edit=0)),
        ("GvEditOn", setup(3, 3, 0, edit=1)),
        ("GvSet", setup(3, 3, 2, gv={"selPlays": 1, "touchOn": 0})),
        ("GvWifi", setup(3, 3, 6, gv={"net": "JOINING"})), ("GvWifiEdit", setup(3, 3, 6, edit=0)),
        ("GvWifiOff", setup(3, 3, 6, gv={"wifi": 0, "net": "OFF"})),
        ("GvIp", setup(3, 3, 7, gv={"net": "192.168.178.123"})),
        ("GvAp", setup(3, 3, 7, gv={"net": "AP 192.168.4.1"})))]
    wavs = ["Kick %02d.wav" % i for i in range(1, 12)]
    wavs[3] = "a_really_long_sample_name_in_the_list.wav"
    many = ["Loop%03d.wav" % i for i in range(30)]
    shelf = {"project": 2, "projects": [0, 1, 2, 7, 47], "presets": [0, 1, 2, 5, 47],
             "locked": [1, 47], "preset": 1}

    def files(folder, cur=0, names=None, store=None, sd=None, **f):   # FILE open there
        def fn(s, d):
            s["_file"] = {"folder": folder, "cur": cur, **({"files": names} if names is not None else {}), **f}
            if store:
                s["store"] = {**s.get("store", {}), **store}
            if sd is not None:
                s["sd_state"] = sd
        return fn
    out += [("file" + name, case(fn)) for name, fn in (
        ("Root", files("ROOT", 1, counts={"project": 3, "Wavs": 11, "Recs": 0}, store=shelf)),
        ("RootNoCounts", files("ROOT", 4, store=shelf)),
        ("Wavs", files("Wavs", 3, wavs)), ("WavsUp", files("Wavs", -1, wavs)),
        ("WavsEnd", files("Recs", 29, many)), ("WavsMid", files("project", 14, many)),
        ("Empty", files("Wavs", -1, [])), ("Loading", files("Wavs", -1, [], ok=False)),
        ("SdError", files("Wavs", -1, [], sd=3)),
        ("Presets", files("PRESETS", 1, store=shelf)), ("PresetsEnd", files("PRESETS", 47, store=shelf)),
        ("Projects", files("PROJECTS", 2, store=shelf)), ("ProjectsUp", files("PROJECTS", -1, store=shelf)),
        ("MenuPreset", files("PRESETS", 2, store=shelf, menu=[1, None])),
        ("MenuArmed", files("PRESETS", 2, store=shelf, menu=[1, 1])),
        ("MenuLocked", files("PRESETS", 1, store=shelf, menu=[0, None])),
        ("MenuEmpty", files("PRESETS", 3, store=shelf, menu=[0, None])),
        ("MenuProjectCur", files("PROJECTS", 2, store=shelf, menu=[0, None])),
        ("MenuProjectOpen", files("PROJECTS", 7, store=shelf, menu=[1, None])))]
    out += [("flashLoading", case(lambda s, d: s.update(_flash=["Kick 03.wav", "LOADING"]))),
            ("flashPlain", case(lambda s, d: s.update(_flash=["SD busy", None])))]
    off = {"mode": "swd", "connected": False, "error": "Multigrain off", "_sound": n}
    chk, unk = ({"mode": "swd", "connected": False, "error": "x", "fw": fw, "_sound": n}
                for fw in ("checking", "unknown"))
    out += [("fwChecking", chk), ("fwUnknown", unk), ("setupFw", case(lambda s, d: s.update(_setup=[3, 3, 5]))),
            ("setupFwUnknown", {**unk, "_setup": [3, 3, 5]}), ("setupFwChecking", {**chk, "_setup": [3, 3, 5]})]
    return out + [("nolink", off), ("setupNolink", {**off, "_setup": [3, 3, 4]}),
                  ("fileNolink", {**off, "_file": {"folder": "ROOT", "cur": 2}})]


def ui_check(port, views, all_sounds=False, cases=False, k=3):
    """The Pico's own UI (pico/gv_ui.py) vs the emulator (tools/gv_render.js, headless)
    rendering the same snapshot; the panel shows each view. Read-only on the Multigrain,
    except all_sounds: edit focus 1..8 (mg_load.select_nohalt, no halt), then restored."""
    link = PicoLink(port, log=lambda *a: None)
    for _ in range(50):
        if link.ser is not None:
            break
        time.sleep(0.1)
    if cases:
        live = json.loads(link.swd("S", timeout=5))
        for name, snap in ui_cases(live):     # an overlay case shows it on any view
            _ui_views(link, ["SETUP"] if "_setup" in snap else ["FILE"] if "_file" in snap
                      else views, name + " ", k, snap)
        return
    if not all_sounds:
        return _ui_views(link, views, "", k)
    import mg_load as L
    t = PicoTarget(link)
    t.connect()
    was = L.u8(t, L.CUR_SOUND)
    try:
        for n in range(8):
            L.select_nohalt(t, n)
            _ui_views(link, views, f"S{n + 1} ", k)
    finally:
        L.select_nohalt(t, was)


def _ui_views(link, views, tag, k, snap=None):
    out_dir = os.path.join(os.path.dirname(HERE), "tmp")
    os.makedirs(out_dir, exist_ok=True)
    for view in views:
        js = json.dumps({**snap, "_view": view}, separators=(",", ":")).encode() if snap else b""
        r = link.swd("v", js or view.encode(), timeout=10)
        pico, used = unpack(r[:FRAME]), js or r[FRAME:]
        with tempfile.NamedTemporaryFile("wb", suffix=".json", delete=False) as f:
            f.write(used)
        emu = unpack(subprocess.run(["node", os.path.join(HERE, "gv_render.js"), f.name, view],
                                    check=True, capture_output=True).stdout)
        os.unlink(f.name)
        bad = [(x, y) for y in range(H) for x in range(W) if pico[y][x] != emu[y][x]]
        gap = bytes(4 * k)                      # pico | emulator | diff, k x k per pixel
        rows = []
        for y in range(H):
            line = [bytes(v * 17 for v in pico[y] for _ in range(k)), gap,
                    bytes(v * 17 for v in emu[y] for _ in range(k)), gap,
                    bytes(255 if pico[y][x] != emu[y][x] else emu[y][x] * 4
                          for x in range(W) for _ in range(k))]
            rows += [b"".join(line)] * k
        path = os.path.join(out_dir, f"gv_ui_{tag.strip()}{'_' if tag else ''}{view}.png")
        png(path, rows)
        where = ""
        if bad:
            xs, ys = [p[0] for p in bad], [p[1] for p in bad]
            where = f" in x {min(xs)}..{max(xs)}, y {min(ys)}..{max(ys)}"
        print(f"{tag}{view:8} {'MATCH' if not bad else f'{len(bad)} pixels differ{where}'}"
              f"   ({os.path.relpath(path)})")


def main():
    ap = argparse.ArgumentParser(description="GRAINVIEW Pico screen helper")
    ap.add_argument("cmd", choices=["deploy", "quit", "keys", "swd", "poll", "ui"])
    ap.add_argument("views", nargs="*", help="ui: views to check (default: all 4 + SETUP + FILE)")
    ap.add_argument("--all-sounds", action="store_true", help="ui: check sounds 1-8")
    ap.add_argument("--cases", action="store_true", help="ui: check made-up edge cases")
    ap.add_argument("--port", help="serial port (default: first Raspberry Pi board)")
    ap.add_argument("--khz", type=int, default=8000, help="SWCLK for swd (default 8000)")
    a = ap.parse_args()
    port = a.port or find_port()
    if not port:
        raise SystemExit("no Pico found (USB plugged in?)")

    if a.cmd == "quit":
        quit_screen(port)
        print("screen stopped; REPL free")
    elif a.cmd == "deploy":
        import gen_pico_map
        gen_pico_map.main()             # the Pico's addresses always match the Mac tools
        quit_screen(port)
        mp = os.path.join(os.path.dirname(sys.executable), "mpremote")
        files = sorted(glob.glob(os.path.join(PICO_DIR, "*.py")))
        wifi = os.path.join(PICO_DIR, "wifi.json")      # (not in git: the WiFi password)
        files += [wifi] if os.path.exists(wifi) else []
        with tempfile.TemporaryDirectory() as tmp:     # the page, gzipped: ~3x less to send
            gz = os.path.join(tmp, "gv_web.html.gz")
            with open(os.path.join(PICO_DIR, "gv_web.html"), "rb") as f, gzip.open(gz, "wb", 9) as o:
                o.write(f.read())
            subprocess.run([mp, "connect", port, "cp", *files, gz, ":", "+", "reset"], check=True)
        print("deployed:", ", ".join(os.path.basename(f) for f in files + [gz]))
    elif a.cmd == "swd":
        swd_check(port, a.khz)
    elif a.cmd == "poll":
        poll_check(port, a.khz)
    elif a.cmd == "ui":
        ui_check(port, a.views or ["WAVE", "PARAM", "MOD", "SETTINGS", "SETUP", "FILE"], a.all_sounds,
                 a.cases)
    elif a.cmd == "keys":
        link = PicoLink(port)
        q = link.subscribe()
        print("press buttons / turn the encoder (Ctrl-C to stop)")
        try:
            while True:
                print(q.get())
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
