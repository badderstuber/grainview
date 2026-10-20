# GRAINVIEW UI on the Pico, drawn from its own poll (mgpoll.py). A port of the emulator
# (tools/grainview_emulator.html, the spec): same layout maths, same fonts, so the frames
# match pixel for pixel - check with: tools/venv/bin/python tools/gv_pico.py ui PARAM
# Ported so far: header, status line, WAVE (static: no grain dots yet), PARAM, MOD, the
# NO MODULE LINK / flash boxes. SETTINGS, FILE, SETUP and the knob hero: still Mac-only.
#
#   ui = UI()
#   ui.render(snap)                     # into ui.buf (128x128 GS4, the SSD1327's layout)
#   act = ui.btn("SOUND>")              # -> None or ("select", n) for main.py to do
import framebuf
import math
import time

from gv_draw import FONT, H, W, Draw, fit
from gv_units import jround, unit_text

VIEWS = ("WAVE", "PARAM", "MOD", "SETTINGS")
PORTED = ("WAVE", "PARAM", "MOD")
MKEYS = ("START", "WRAP", "SCAN", "SHAPE", "SIZE", "RATE", "PITCH", "TONE", "LEVEL", "BLUR")
SOURCES = ("RAND", "X", "Y", "Z")
PARM_ORDER = ("START", "WRAP", "SCAN", "RATE", "SIZE", "PITCH", "SHAPE", "TONE", "LEVEL",
              "BLUR", "MORPH")
PARM_LINKS = (("RATE", "SIZE", "RATE"), ("SIZE", "PITCH", "SIZE"))   # left, right, derived
CHAIN = (".###...###.",                       # 11x5: two links + bar
         "#...#.#...#",
         "#..#####..#",
         "#...#.#...#",
         ".###...###.")
WAVE_AMP = 0.35
FLASH_MS = 1100


def fmt(v, bip):                              # normalized: unipolar .42, bipolar +.42
    if v is None:
        return "-"
    a = abs(v)
    s = "1.0" if a >= 0.995 else "." + ("%02d" % jround(a * 100))
    return ("-" if v < 0 else "+") + s if bip else s


def seed_of(s):
    h = 0
    for ch in s or "":
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return 1 + h % 9


def make_wave(n, seed):                       # synthetic until the WAV is read (as the emulator)
    a, f1, f2, tau = [], 5 + seed * 1.7, 37 + seed * 3, 2 * math.pi
    for i in range(n):
        t = i / n
        env = math.sin(math.pi * t) ** 0.6
        body = 0.55 + 0.45 * math.sin(tau * f1 * t + seed)
        det = 0.5 + 0.5 * math.sin(tau * f2 * t)
        burst = 1 if 0.33 < t < 0.42 else 0
        a.append(min(1, env * (0.75 * body + 0.25 * det) + burst * 0.4 * env))
    return a


class UI:
    def __init__(self):
        self.buf = bytearray(W * H // 2)
        self.fb = framebuf.FrameBuffer(self.buf, W, H, framebuf.GS4_HMSB)
        self.d = Draw(self.fb)
        self.T, self.M = FONT("T"), FONT("M")
        self.view = "WAVE"
        self.sound, self.scene = 0, "A"
        self.snap = None
        self.flash_msg, self.flash_until = None, 0
        self.wave_key = self.wave = None      # cached synthetic waveform

    # ---- data ----
    def snd(self):
        s = self.snap
        return s["sounds"][self.sound] if s and s.get("sounds") else None

    def uctx(self):
        s = self.snd()
        if not s:
            return {}
        p = s[self.scene]
        return {"link_rs": s["link_rs"] == 1, "link_sp": s["link_sp"] == 1,
                "sync": self.snap.get("sync") == 1, "size": p["SIZE"], "pitch": p["PITCH"]}

    def pval(self, k):
        if k == "MORPH":
            return unit_text("MORPH", self.snap.get("morph") if self.snap else None)
        s = self.snd()
        return unit_text(k, s[self.scene][k], self.uctx()) if s else "-"

    def linked(self, k):
        s = self.snd()
        return bool(s) and ((k == "RATE" and s["link_rs"] == 1 and self.snap.get("sync") != 1)
                            or (k == "SIZE" and s["link_sp"] == 1))

    # ---- chrome ----
    def header(self):
        """S# [>] filename ...... [A]  -> content top y."""
        d, M, s = self.d, self.M, self.snd()
        lh, base = M.lh, M.asc + 1
        x = 1 + d.text(M, "S%d" % (self.sound + 1), 1, base, 15) + 2
        if self.snap and self.snap.get("playing") == self.sound:
            y, h = base - M.cap + 1, M.cap - 1
            for i in range(3):                # small play mark
                d.rect(x + i, y + i, 1, h - 2 * i, 15)
        x += 7
        bw = M.width(self.scene) + 5
        d.rect(W - bw, 0, bw, lh + 1, 15)
        d.text(M, self.scene, W - bw + 3, base, 0)
        name = s["file"] if s and s["file"] else "- empty -"
        d.text(M, fit(M, name, W - bw - 3 - x), x, base, 11 if s and s["file"] else 5)
        d.hline(0, W - 1, lh + 2, 4)
        return lh + 4

    def status(self, name, right, rv=10):
        """Page dots + NAME ...... right  -> its top y."""
        d, T = self.d, self.T
        y, top, x = H - 1 - T.desc, H - T.lh - 1, 1
        if name in VIEWS:
            for v in VIEWS:
                if v == self.view:
                    d.rect(x, y - 3, 3, 3, 15)
                else:
                    d.px(x + 1, y - 2, 6)
                x += 4
            x += 2
        x += d.text(T, name, x, y, 10) + 3
        rw = T.width(right)
        d.dots(x + (x & 1), W - rw - 4, y - 1, 5)
        d.text_r(T, right, W - 1, y, rv)
        return top

    def box(self, msg, label=None):
        d, T, M = self.d, self.T, self.M
        m = fit(M, msg, W - 14)
        lt = T.lh + 1 if label else 0
        w = max(M.width(m), T.width(label) if label else 0) + 10
        h = M.lh + 6 + lt
        x, y = (W - w) >> 1, (H - h) >> 1
        d.rect(x - 1, y - 1, w + 2, h + 2, 0)
        d.rect(x, y, w, h, 15)
        if label:
            d.text(T, label, x + 5, y + 3 + T.asc, 0)
        d.text(M, m, x + 5, y + 3 + lt + M.asc, 0)

    # ---- views ----
    def v_wave(self):
        d, M = self.d, self.M
        top = self.header()
        pl = self.snap.get("playing") if self.snap and self.snap.get("connected") else None
        bot = self.status("WAVE", "PLAY S%s" % (pl + 1 if pl is not None else "-"), 10)
        s, h = self.snd(), 0
        h = bot - top - 2
        if s and s["file"]:
            p = s[self.scene]
            s0 = p["START"]
            self.draw_wave(1, top, W - 2, h, seed_of(s["file"]), s0, min(1, s0 + p["WRAP"]), s0)
        else:
            d.text(M, "no sample", (W - M.width("no sample")) >> 1, top + (h >> 1) + (M.cap >> 1), 5)

    def draw_wave(self, x, y, w, h, seed, s, e, sc):
        """Waveform band, window START..START+WRAP bright, scan playhead dotted."""
        d = self.d
        if self.wave_key != (w, seed):
            self.wave_key, self.wave = (w, seed), make_wave(w, seed)
        mid, band = y + (h >> 1), jround(((h >> 1) - 1) * WAVE_AMP)
        for i, v in enumerate(self.wave):
            amp, win = jround(v * band), s <= i / w <= e
            d.rect(x + i, mid - amp, 1, amp * 2 + 1, 9 if win else 3)
            d.px(x + i, mid - amp, 15 if win else 7)
            d.px(x + i, mid + amp, 15 if win else 7)
        for v in (s, e):
            d.rect(x + jround(v * (w - 1)), y, 1, h, 15)
        sx = x + jround(sc * (w - 1))
        for yy in range(y, y + h, 2):
            d.px(sx, yy, 12)

    def v_param(self):
        d, T, M = self.d, self.T, self.M
        top = self.header()
        bot = self.status("PARAM", "SCENE " + self.scene)
        cols, rows = 3, (len(PARM_ORDER) + 2) // 3
        cw = W // cols
        ch = min(T.lh + M.lh + 3, (bot - top) // rows)
        pos = {}
        for i, k in enumerate(PARM_ORDER):
            x, y = 1 + (i % cols) * cw, top + (i // cols) * ch
            pos[k] = (x, y)
            d.text(T, k, x, y + T.asc, 6 if k == "MORPH" else 8)
            d.text(M, self.pval(k), x, y + T.lh + 1 + M.asc, 10 if k == "MORPH" else 15)
        for l, r, k in PARM_LINKS:            # chain icon centred in the label gap
            if self.linked(k):
                ax, ay = pos[l]
                cx = (ax + T.width(l) + pos[r][0] - len(CHAIN[0])) >> 1
                cy = ay + T.asc - T.cap + 1 + ((T.cap - len(CHAIN) + 1) >> 1)
                for j, row in enumerate(CHAIN):
                    for i, c in enumerate(row):
                        if c == "#":
                            d.px(cx + i, cy + j, 15)

    def v_mod(self):
        d, T = self.d, self.T
        top = self.header()
        bot = self.status("MOD", "SCENE " + self.scene)
        lw = max(T.width(k) for k in MKEYS) + 3
        cw = (W - lw) // 4
        rh = min(T.lh + 1, (bot - top) // (len(MKEYS) + 1))
        for i, src in enumerate(SOURCES):
            l = src[0]
            d.text(T, l, lw + i * cw + ((cw - T.width(l)) >> 1), top + T.asc, 10)
        s = self.snd()
        for r, k in enumerate(MKEYS):
            y = top + (r + 1) * rh + T.asc
            d.text(T, k, 1, y, 8)
            for i, src in enumerate(SOURCES):
                v = s["mod"][self.scene][src][k] if s else 0
                cx = lw + i * cw
                if not v:                     # empty = dim dot, routings bright
                    d.px(cx + (cw >> 1), y - (T.cap >> 1), 5)
                else:
                    t = fmt(v, True)
                    d.text(T, t, cx + ((cw - T.width(t)) >> 1), y, 15)

    def v_todo(self):
        d, M = self.d, self.M
        top = self.header()
        bot = self.status(self.view, "")
        for i, line in enumerate(("not on the", "Pico yet")):
            d.text(M, line, (W - M.width(line)) >> 1, top + ((bot - top) >> 1) + i * M.lh, 5)

    # ---- render / input ----
    def render(self, snap):
        self.snap = snap
        if snap and snap.get("connected"):
            self.sound = snap["selected"] if 0 <= snap["selected"] < 8 else self.sound
            self.scene = snap.get("edit_scene") or self.scene
        self.fb.fill(0)
        if self.view == "WAVE":
            self.v_wave()
        elif self.view == "PARAM":
            self.v_param()
        elif self.view == "MOD":
            self.v_mod()
        else:
            self.v_todo()
        if self.flash_msg and time.ticks_diff(self.flash_until, time.ticks_ms()) > 0:
            self.box(self.flash_msg)
        elif not (snap and snap.get("connected")):
            self.box("NO MODULE LINK")

    def flash(self, msg):
        self.flash_msg, self.flash_until = msg, time.ticks_add(time.ticks_ms(), FLASH_MS)

    def flash_due(self):
        """True once when a flash box has just run out (main.py redraws)."""
        if self.flash_msg and time.ticks_diff(self.flash_until, time.ticks_ms()) <= 0:
            self.flash_msg = None
            return True
        return False

    def enc(self, n):                         # page the views (clamped, as the emulator)
        i = VIEWS.index(self.view) + n
        self.view = VIEWS[max(0, min(len(VIEWS) - 1, i))]

    def btn(self, name):
        if name == "VIEW":
            self.view = VIEWS[(VIEWS.index(self.view) + 1) % len(VIEWS)]
        elif name == "BACK":
            self.view = "WAVE"
        elif name in ("SOUND<", "SOUND>"):
            n = (self.sound + (7 if name == "SOUND<" else 1)) % 8
            self.sound = n
            return ("select", n)
        elif name == "PUSH":
            self.flash("-" if self.view == "WAVE" else "view-only")
        else:                                 # FILE, A/B, SETUP
            self.flash("on the Mac (soon)")
        return None
