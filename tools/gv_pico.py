#!/usr/bin/env python3
"""gv_pico.py - the GRAINVIEW breadboard Pico as a USB screen + keys.

The Pico runs pico/main.py: it shows the 128x128 frames we send and reports its
buttons and encoder as text lines. grainview_server.py uses PicoLink to forward the
emulator's frames and pass the key events back to the browser (GET /events).

CLI:
    tools/venv/bin/python tools/gv_pico.py deploy   # copy pico/*.py to the board + restart it
    tools/venv/bin/python tools/gv_pico.py quit     # stop the screen, free the REPL for mpremote
    tools/venv/bin/python tools/gv_pico.py keys     # print key events (screen test)
"""
import argparse
import glob
import os
import queue
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


class PicoLink:
    """Background serial link. Thread-safe send_frame(); subscribe() for key events."""

    def __init__(self, port=None, log=print):
        self.port_arg, self.log = port, log
        self.ser = None
        self.port = None
        self.lock = threading.Lock()
        self.subs = []
        self.last = None            # last frame from the browser (re-sent on reconnect)
        self.sent = None            # what the panel shows now
        self.frames = 0
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
            if line:
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


def main():
    ap = argparse.ArgumentParser(description="GRAINVIEW Pico screen helper")
    ap.add_argument("cmd", choices=["deploy", "quit", "keys"])
    ap.add_argument("--port", help="serial port (default: first Raspberry Pi board)")
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
