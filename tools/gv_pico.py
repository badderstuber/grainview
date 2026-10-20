#!/usr/bin/env python3
"""gv_pico.py - the GRAINVIEW Pico as a USB screen + keys + SWD probe.

The Pico runs pico/main.py: it shows the 128x128 frames we send and reports its
buttons and encoder as text lines. grainview_server.py uses PicoLink to forward the
emulator's frames and pass the key events back to the browser (GET /events).
PicoTarget drives the Pico's SWD master (pico/swd.py) over the same link, shaped like
the pyOCD target the mg_* helpers use, so they run without the ST-Link.

CLI:
    tools/venv/bin/python tools/gv_pico.py deploy   # copy pico/*.py to the board + restart it
    tools/venv/bin/python tools/gv_pico.py quit     # stop the screen, free the REPL for mpremote
    tools/venv/bin/python tools/gv_pico.py keys     # print key events (screen test)
    tools/venv/bin/python tools/gv_pico.py swd      # SWD over the Pico: IDs + timings (read-only)
"""
import argparse
import glob
import os
import queue
import struct
import subprocess
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
        self.swd_lock = threading.Lock()    # one SWD request in flight
        self.seq = 0
        self.replies = queue.Queue()
        threading.Thread(target=self._run, daemon=True).start()

    # ----- status / events -----
    def status(self):
        return {"connected": self.ser is not None, "port": self.port, "frames": self.frames}

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
        """Give the SWD pins back (the Multigrain keeps running)."""
        self.link.swd("x")

    # ----- memory -----
    def _read(self, addr, n):
        out = b""
        while len(out) < n:
            k = min(n - len(out), SWD_CHUNK)
            out += self.link.swd("r", struct.pack("<II", addr + len(out), k))
        return out

    def read_spans(self, spans):
        """[(addr, n), ...] -> [bytes, ...], as few round trips as fit SWD_CHUNK."""
        out, i = [], 0
        while i < len(spans):
            j, size = i, 0
            while j < len(spans) and (j == i or size + spans[j][1] <= SWD_CHUNK):
                size += spans[j][1]
                j += 1
            if j == i + 1 and size > SWD_CHUNK:          # one big span: plain reads
                out.append(self._read(*spans[i]))
            else:
                data = self.link.swd("R", b"".join(struct.pack("<IH", a, n)
                                                    for a, n in spans[i:j]))
                for a, n in spans[i:j]:
                    out.append(data[:n])
                    data = data[n:]
            i = j
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


class ReplayReads:
    """A PicoTarget for a read pass that repeats (grainview_server's poll). begin()
    fetches the spans the last pass read in one scatter request and serves reads from
    that; a read outside them goes live and joins the next pass's list (end()). One or
    two USB round trips per poll instead of ~75, and all values from the same moment.
    Anything that isn't a read (writes, halt) goes straight to the target."""
    GAP = 48                            # merge spans closer than this

    def __init__(self, t):
        self.t = t
        self.want, self.used, self.blocks = set(), set(), []

    def begin(self):
        spans = []
        for a, n in sorted(self.want):
            if spans and a <= spans[-1][1] + self.GAP:
                spans[-1][1] = max(spans[-1][1], a + n)
            else:
                spans.append([a, a + n])
        spans = [(lo, hi - lo) for lo, hi in spans]
        self.blocks = list(zip((lo for lo, _ in spans), self.t.read_spans(spans)))
        self.used = set()
        return self

    def end(self):
        self.want, self.blocks = self.used, []

    def _get(self, a, n):
        self.used.add((a, n))
        for lo, b in self.blocks:
            if lo <= a and a + n <= lo + len(b):
                return b[a - lo:a - lo + n]
        return self.t._read(a, n)

    def read_memory(self, addr, transfer_size=32):
        return int.from_bytes(self._get(addr, transfer_size // 8), "little")

    def read_memory_block8(self, addr, n):
        return list(self._get(addr, n))

    def read_memory_block32(self, addr, n):
        return list(struct.unpack(f"<{n}I", self._get(addr, 4 * n)))

    def __getattr__(self, name):
        return getattr(self.t, name)


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


def main():
    ap = argparse.ArgumentParser(description="GRAINVIEW Pico screen helper")
    ap.add_argument("cmd", choices=["deploy", "quit", "keys", "swd"])
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
        quit_screen(port)
        mp = os.path.join(os.path.dirname(sys.executable), "mpremote")
        files = sorted(glob.glob(os.path.join(PICO_DIR, "*.py")))
        subprocess.run([mp, "connect", port, "cp", *files, ":", "+", "reset"], check=True)
        print("deployed:", ", ".join(os.path.basename(f) for f in files))
    elif a.cmd == "swd":
        swd_check(port, a.khz)
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
