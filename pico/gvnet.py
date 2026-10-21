# GRAINVIEW over WiFi: the panel in a browser (gv_web.html), for a phone or a desktop.
# Joins the WiFi in wifi.json ({"ssid", "password"}) as grainview.local; with no file, or if
# it can't join within JOIN_MS (retrying), it runs its own hotspot instead (GRAINVIEW / "grainview",
# or "ap_ssid" / "ap_password" from wifi.json; WPA2 needs 8+ characters). Once joined, a
# lost connection is rejoined, not swapped for the hotspot; SETUP > GRAINVIEW > WiFi OFF/ON
# starts over.
#
# A tiny HTTP server serves the page (gzipped by gv_pico.py deploy) and a WebSocket at /ws:
#   out (binary)  r0 n + n*64 bytes   rows r0..r0+n-1 of what the OLED shows, left px in the
#                                     high nibble (the Mac's frames too), at most every FRAME_MS
#   in (text)     "B BACK"  "E +1"    a button press / encoder steps, as the panel's own
# Every client gets the same frames, sent straight from the one copy of what they have (only
# there while one is connected: the heap is tight), so a new frame waits until all have
# taken the last one, and a new client gets a full one.
# Nothing blocks except the page itself (~6 KB) and the handshake. step() is driven from
# main.py's loop. Runs under CPython too (no WiFi): Net(buf, key, wifi=False, port=...).
import binascii
import errno
import hashlib
import json
import select
import socket
import time

JOIN_MS = 15000
RETRY_MS = 2000                               # a failed try: again after this, until JOIN_MS
FRAME_MS = 50                                 # ~20 fps to the browser (WAVE animates at 30)
FLUSH_MS = 15                                 # a new frame: keep sending it this long (the
                                              # rest would wait a whole main-loop pass)
STALL_MS = 2000                               # a browser that doesn't take a frame: dropped
STATUS_MS = 250
MAX_WS = 3
PAGES = (("gv_web.html.gz", True), ("gv_web.html", False))
WS_GUID = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
AGAIN = (errno.EAGAIN, getattr(errno, "EWOULDBLOCK", errno.EAGAIN))


class Client:
    def __init__(self, s):
        self.s, self.inb, self.ws = s, b"", False
        self.fd = s.fileno() if hasattr(s, "fileno") else None   # CPython's poll gives fds
        self.at = time.ticks_ms()             # HTTP: when it came (dropped if it dawdles)


class Net:
    def __init__(self, buf, key, wifi=True, port=80):
        """buf = the OLED's framebuffer (bytearray, 128 rows); key(name) / key(+-steps) = a
        press from a browser."""
        self.buf, self.key, self.port = buf, key, port
        self.bpr = len(buf) // 128
        self.last = None                      # what the browsers have (while there are any)
        self.hd = bytearray(6)                # a frame's WebSocket header + r0 n
        self.pend = []                        # [client, [memoryviews still to send]]
        self.full, self.sent_at = True, time.ticks_ms()
        self.cs, self.srv, self.p = [], None, select.poll()
        self.wl, self.mode, self.ip, self.cfg = None, None, None, {}
        self.text = "-"                       # SETUP > GRAINVIEW > IP
        if wifi:
            self.start()
        else:
            self.listen()
            self.text = "PORT %d" % port

    # ---- WiFi ----
    def start(self):
        import network
        network.hostname("grainview")         # grainview.local (mDNS)
        try:
            with open("wifi.json") as f:
                self.cfg = json.load(f)
        except (OSError, ValueError):
            self.cfg = {}
        if not self.cfg.get("ssid"):
            return self.hotspot()
        wl = self.wl = network.WLAN(network.STA_IF)
        wl.active(True)                       # (~1 s, blocking: the radio boots)
        wl.config(pm=network.WLAN.PM_NONE)    # no power-save: keys + frames without lag
        self.join()

    def join(self):
        self.wl.connect(self.cfg["ssid"], self.cfg.get("password", ""))
        self.mode, self.ip, self.text, self.had = "sta", None, "JOINING", False
        self.t0 = self.chk = self.tj = time.ticks_ms()

    def hotspot(self):
        import network
        if self.wl is not None:
            self.wl.active(False)
        wl = self.wl = network.WLAN(network.AP_IF)
        wl.config(ssid=self.cfg.get("ap_ssid", "GRAINVIEW"),
                  key=self.cfg.get("ap_password", "grainview"))
        wl.active(True)
        self.mode, self.ip = "ap", wl.ifconfig()[0]
        self.text = "AP " + self.ip
        self.listen()

    def wifi_step(self, now):
        if self.mode != "sta" or time.ticks_diff(now, self.chk) < STATUS_MS:
            return
        import network
        self.chk = now
        st = self.wl.status()
        if st == network.STAT_GOT_IP:
            if self.ip is None:
                self.ip = self.text = self.wl.ifconfig()[0]
                self.had = True
                self.listen()
        elif self.ip is not None:             # had it, lost it: rejoin, for as long as it
            self.ip, self.text, self.tj = None, "JOINING", now   # takes (the hotspot is for a
                                              # WiFi that isn't there, not one that blinked)
        elif not self.had and time.ticks_diff(now, self.t0) > JOIN_MS:
            print("gvnet: no WiFi (status %d): hotspot" % st)
            self.hotspot()                    # wrong password / no such network / too slow
        elif (st < 0 and time.ticks_diff(now, self.tj) > RETRY_MS
              or time.ticks_diff(now, self.tj) > JOIN_MS):
            self.wl.disconnect()              # (one failed try isn't the WiFi being gone)
            self.wl.connect(self.cfg["ssid"], self.cfg.get("password", ""))
            self.tj = now

    def stop(self):
        for c in list(self.cs):
            self.drop(c)
        if self.srv is not None:
            self.p.unregister(self.srv)
            self.srv.close()
            self.srv = None
        if self.wl is not None:
            self.wl.active(False)
            self.wl = None
        self.mode, self.ip, self.text = None, None, "-"

    # ---- server ----
    def listen(self):
        if self.srv is not None:
            return
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", self.port))
        s.listen(4)
        s.setblocking(False)
        self.srv = s
        self.p.register(s, select.POLLIN)

    def step(self):
        now = time.ticks_ms()
        if self.wl is not None:
            self.wifi_step(now)
        if self.srv is None:
            return
        for t in self.p.poll(0):              # (obj or fd, event, maybe more)
            o, ev = t[0], t[1]
            if o is self.srv or o == getattr(self.srv, "fileno", lambda: -1)():
                self.accept()
                continue
            for c in self.cs:
                if c.s is o or o == c.fd:
                    if ev & (select.POLLHUP | select.POLLERR):
                        self.drop(c)
                    else:
                        self.read(c)
                    break
        for c in self.cs:
            if not c.ws and time.ticks_diff(now, c.at) > 3000:
                self.drop(c)                  # a request that never finished
                break
        self.frame()

    def accept(self):
        try:
            s, _ = self.srv.accept()
        except OSError:
            return
        if len(self.cs) >= MAX_WS + 1:
            s.close()
            return
        s.setblocking(False)
        self.cs.append(Client(s))
        self.p.register(s, select.POLLIN)

    def drop(self, c):
        if c in self.cs:
            self.cs.remove(c)
            try:
                self.p.unregister(c.s)
            except (OSError, KeyError, ValueError):
                pass
        c.s.close()
        self.pend = [q for q in self.pend if q[0] is not c]
        if not any(x.ws for x in self.cs):
            self.last = None                  # the last browser went: give the 8 KB back

    def read(self, c):
        try:
            d = c.s.recv(512)
        except OSError as e:
            if e.args[0] not in AGAIN:
                self.drop(c)
            return
        if not d:
            return self.drop(c)
        c.inb += d
        if c.ws:
            self.ws_in(c)
        elif b"\r\n\r\n" in c.inb:
            self.request(c)
        elif len(c.inb) > 2048:
            self.drop(c)

    def send_now(self, c, data):
        """A short blocking send (the page, a handshake, a pong), then back to non-blocking."""
        c.s.setblocking(True)
        try:
            c.s.settimeout(1)
            c.s.sendall(data)
        finally:
            c.s.setblocking(False)

    def request(self, c):
        head = c.inb.split(b"\r\n\r\n", 1)[0].decode().split("\r\n")
        path = (head[0].split(" ") + ["", ""])[1].split("?", 1)[0]
        hdr = {}
        for h in head[1:]:
            k, _, v = h.partition(":")
            hdr[k.strip().lower()] = v.strip()
        try:
            if path == "/ws" and "sec-websocket-key" in hdr and len([x for x in self.cs if x.ws]) < MAX_WS:
                acc = binascii.b2a_base64(hashlib.sha1(hdr["sec-websocket-key"].encode()
                                                       + WS_GUID).digest()).strip()
                self.send_now(c, b"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\n"
                                 b"Connection: Upgrade\r\nSec-WebSocket-Accept: " + acc + b"\r\n\r\n")
                c.ws, c.inb, self.full = True, b"", True      # a full frame for everyone next
                c.s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)   # no Nagle wait
                if self.last is None:
                    self.last = bytearray(len(self.buf))
                return
            if path in ("/", "/index.html"):
                self.page(c, "gzip" in hdr.get("accept-encoding", ""))
                return
            self.send_now(c, b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
        except OSError:
            pass
        except Exception as e:                # (a bug here mustn't leave the socket open)
            print("gvnet request", path, repr(e))
        self.drop(c)

    def page(self, c, gz_ok):
        for name, gz in PAGES if gz_ok else (PAGES[1], PAGES[0]):   # gzip if it's taken
            try:
                f = open(name, "rb")
            except OSError:
                continue
            with f:
                f.seek(0, 2)
                n = f.tell()
                f.seek(0)
                self.send_now(c, ("HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n"
                                  "Content-Length: %d\r\nCache-Control: no-cache\r\n%s"
                                  "Connection: close\r\n\r\n" % (n, "Content-Encoding: gzip\r\n"
                                                                 if gz else "")).encode())
                chunk = bytearray(1024)
                while True:
                    k = f.readinto(chunk)
                    if not k:
                        break
                    self.send_now(c, memoryview(chunk)[:k])
            break
        else:
            self.send_now(c, b"HTTP/1.1 500 No Page\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
        self.drop(c)

    # ---- WebSocket ----
    def ws_in(self, c):
        while len(c.inb) >= 2:
            b0, b1 = c.inb[0], c.inb[1]
            op, n, i = b0 & 15, b1 & 127, 2
            if n == 126:
                if len(c.inb) < 4:
                    return
                n, i = c.inb[2] << 8 | c.inb[3], 4
            elif n == 127:                    # nothing we'd take is that big
                return self.drop(c)
            m = i + 4 if b1 & 128 else i
            if len(c.inb) < m + n:
                return
            pl = bytearray(c.inb[m:m + n])
            if m > i:                         # browsers always mask
                for k in range(n):
                    pl[k] ^= c.inb[i + (k & 3)]
            c.inb = c.inb[m + n:]
            if op == 8:                       # close
                return self.drop(c)
            if op == 9:                       # ping -> pong, after any frame half sent
                pong = bytes((0x8A, n)) + bytes(pl)
                q = [q for q in self.pend if q[0] is c]
                if q:
                    q[0][1].append(memoryview(pong))
                    continue
                try:
                    self.send_now(c, pong)
                except OSError:
                    return self.drop(c)
            elif op == 1:
                self.cmd(pl.decode())

    def cmd(self, t):
        k, _, v = t.partition(" ")
        try:
            if k == "B":
                self.key(v)
            elif k == "E":
                self.key(max(-8, min(8, int(v))))
        except Exception as e:                # a bad key from a browser: not the panel's end
            print("gvnet key", t, e)

    def frame(self):
        """When every browser has the last frame, make the next one from what changed (or
        all of it, for a new browser); then send what's pending, straight away."""
        ws = [c for c in self.cs if c.ws]
        now = time.ticks_ms()                 # (not step()'s: a key may have taken a while)
        if not self.pend and ws and time.ticks_diff(now, self.sent_at) >= FRAME_MS:
            self.build(now, ws)
            while True:                       # ACKs come back in a few ms: finish it now
                self.flush()
                if not self.pend or time.ticks_diff(time.ticks_ms(), now) >= FLUSH_MS:
                    break
                time.sleep_ms(1)
        elif self.pend and time.ticks_diff(now, self.sent_at) > STALL_MS:
            for q in list(self.pend):         # gone without a word (out of range): don't
                self.drop(q[0])               # hold the others up (the page reconnects)
        else:
            self.flush()

    def flush(self):
        for q in list(self.pend):
            c, parts = q
            while parts:
                try:
                    k = c.s.send(parts[0])
                except OSError as e:
                    if e.args[0] not in AGAIN:
                        self.drop(c)
                    break
                if k is None or k >= len(parts[0]):
                    parts.pop(0)
                else:
                    parts[0] = parts[0][k:]
                    break
            if not parts and q in self.pend:
                self.pend.remove(q)

    def build(self, now, ws):
        a, b, bpr = self.buf, self.last, self.bpr
        if self.full:
            r0, r1 = 0, 127
        else:
            if a == b:
                return
            r0 = 0
            while a[r0 * bpr:(r0 + 1) * bpr] == b[r0 * bpr:(r0 + 1) * bpr]:
                r0 += 1
            r1 = 127
            while a[r1 * bpr:(r1 + 1) * bpr] == b[r1 * bpr:(r1 + 1) * bpr]:
                r1 -= 1
        n = r1 - r0 + 1
        ln, h, i = n * bpr, self.hd, r0 * bpr
        h[0], h[1], h[2], h[3], h[4], h[5] = 0x82, 126, (ln + 2) >> 8, (ln + 2) & 255, r0, n
        b[i:i + ln] = memoryview(a)[i:i + ln]  # (stays put until every browser has it)
        self.full, self.sent_at = False, now
        self.pend = [[c, [memoryview(h), memoryview(b)[i:i + ln]]] for c in ws]
