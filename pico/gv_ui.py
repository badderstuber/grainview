# GRAINVIEW UI on the Pico, drawn from its own poll (mgpoll.py). A port of the emulator
# (tools/grainview_emulator.html, the spec): same layout maths, same fonts, so the frames
# match pixel for pixel - check with: tools/venv/bin/python tools/gv_pico.py ui PARAM
# Ported so far: header, status line, WAVE (waveform + animated grain dots, style B with
# the knob readout), PARAM, MOD, SETTINGS (browse; live = read-only, as the emulator), the
# knob-touch hero, the NO MODULE LINK / flash boxes. Still Mac-only: FILE, SETUP, A/B.
#
#   ui = UI()
#   ui.render(snap)                     # into ui.buf (128x128 GS4, the SSD1327's layout)
#   ui.update(snap)                     # new data only; the next animate() draws it
#   ui.animate()                        # WAVE: next grain frame (~30 fps) -> the rows it
#                                       # changed (r0, n), or None
#   act = ui.btn("SOUND>")              # -> None or ("select", n) for main.py to do
# A snapshot with "_steps" (clock values, ms) + "_rand" (random numbers) renders once per
# step with those - the same script the emulator runs in tools/gv_render.js (tests); also
# "_touch": [knob, mod source or null], "_dived", "_setCur" set that UI state for the test;
# "_prev": earlier snapshots fed through the knob-touch detection first (as polls).
import framebuf
import math
import micropython
import random
import time

from gv_cat import CAT
from gv_draw import FONT, H, W, Draw, fit
from gv_units import (SYNC_MULT, fixed, grain_ms, jround, pitch_st, rate_hz, rate_linked_hz,
                      shape_idx, sync_idx, unit_text)

VIEWS = ("WAVE", "PARAM", "MOD", "SETTINGS")
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
BIPOLAR = ("SCAN", "TONE")
# knob touched -> hero value (the emulator's detectTouch: a stored scene value or mod depth
# of the focused sound moving; >= BULK at once = a preset load etc., silent)
TOUCH_MS, TOUCH_EPS, BULK = 1500, 0.004, 3
NOTE = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
SCALES = (                                    # the emulator's SCALES: short, long, intervals
    ("MAJ", "MAJOR", (0, 2, 4, 5, 7, 9, 11)), ("MIN", "MINOR", (0, 2, 3, 5, 7, 8, 10)),
    ("DOR", "DORIAN", (0, 2, 3, 5, 7, 9, 10)), ("PHR", "PHRYGIAN", (0, 1, 3, 5, 7, 8, 10)),
    ("LYD", "LYDIAN", (0, 2, 4, 6, 7, 9, 11)), ("MIX", "MIXOLYDIAN", (0, 2, 4, 5, 7, 9, 10)),
    ("LOC", "LOCRIAN", (0, 1, 3, 5, 6, 8, 10)), ("HMIN", "HARMONIC MIN", (0, 2, 3, 5, 7, 8, 11)),
    ("MMIN", "MELODIC MIN", (0, 2, 3, 5, 7, 9, 11)), ("PMAJ", "PENTA MAJOR", (0, 2, 4, 7, 9)),
    ("PMIN", "PENTA MINOR", (0, 3, 5, 7, 10)), ("BLUE", "BLUES", (0, 3, 5, 6, 7, 10)),
    ("WHOL", "WHOLE TONE", (0, 2, 4, 6, 8, 10)), ("MAJ3", "MAJOR TRIAD", (0, 4, 7)),
    ("MIN3", "MINOR TRIAD", (0, 3, 7)), ("5TH", "FIFTHS", (0, 7)), ("ROOT", "ROOT ONLY", (0,)),
    ("CHROM", "CHROMATIC", (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)))
# grain dots (the emulator's grainsStep / grains, see its notes): simulated from the
# knobs, one dot per live grain. SCAN_STEP + the sample length are placeholders there too.
GRAIN_MIN_MS, GRAIN_MAX, GRAIN_PX, GRAIN_SPREAD, SCAN_STEP = 80, 160, 2, 0.02, 0.05


def fmt(v, bip):                              # normalized: unipolar .42, bipolar +.42
    if v is None:
        return "-"
    a = abs(v)
    s = "1.0" if a >= 0.995 else "." + ("%02d" % jround(a * 100))
    return ("-" if v < 0 else "+") + s if bip else s


def scale_of(q):                              # named relative to the root, or None
    if not q["notes"][q["root"]]:
        return None
    iv = tuple(i for i in range(12) if q["notes"][(q["root"] + i) % 12])
    for sc in SCALES:
        if sc[2] == iv:
            return sc
    return None


def stext(e, v):                              # a setting's value as the list shows it
    if v is None:
        return "-"
    t, o = e["type"], e.get("options")
    if t == "enum" or t == "info" and o:
        return o[v] if 0 <= v < len(o) else "?"
    if t == "info":
        return str(v)
    if t == "num":
        return e["fmt"].replace("{v}", ("+" if e.get("signed") and v > 0 else "") + fixed(v, e["dp"]))
    if t == "quant":
        n, sc = sum(1 for x in v["notes"] if x), scale_of(v)
        if not n:
            return "OFF"
        if sc:
            return sc[0] if sc[0] == "CHROM" else NOTE[v["root"]] + " " + sc[0]
        return NOTE[v["root"]] + " %dnt" % n
    return "?"


def seed_of(s):
    h = 0
    for ch in s or "":
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return 1 + h % 9


@micropython.viper
def dot(buf, gx: int, gy: int, v: int):
    """A GRAIN_PX (2x2) dot of grey v at gx, gy, straight into the GS4 buffer (left pixel
    = high nibble); a pixel that's already >= 8 (the bright wave) goes black instead."""
    p = ptr8(buf)
    for j in range(2):
        y = gy + j
        if y < 0 or y >= 128:
            continue
        for i in range(2):
            x = gx + i
            if x < 0 or x >= 128:
                continue
            k = y * 64 + (x >> 1)
            b = int(p[k])
            if x & 1:
                p[k] = (b & 0xF0) | (0 if (b & 15) >= 8 else v)
            else:
                p[k] = (b & 0x0F) | ((0 if (b >> 4) >= 8 else v) << 4)


@micropython.viper
def vdots(buf, x: int, y: int, h: int, v: int):
    """Every other pixel of column x, rows y..y+h-1 (the scan playhead)."""
    if x < 0 or x >= 128:
        return
    p = ptr8(buf)
    sh = 0 if x & 1 else 4
    keep = 0xF0 if x & 1 else 0x0F
    yy = y
    while yy < y + h:
        if yy >= 0 and yy < 128:
            k = yy * 64 + (x >> 1)
            p[k] = (int(p[k]) & keep) | (v << sh)
        yy += 2


def band(h):                                  # max half-height of the wave band
    return jround(((h >> 1) - 1) * WAVE_AMP)


# SHAPE windows over a grain's life t 0..1 (the emulator's shapeEnv), in SHAPES order
def _bell(t):
    return math.exp(-0.5 * ((t - 0.5) / 0.17) ** 2)


def _sinc(t):
    x = (t - 0.5) * 4 * math.pi
    return abs(math.sin(x) / x) if x else 1


def _tukey(t):
    if t < 0.2:
        return 0.5 - 0.5 * math.cos(math.pi * t / 0.2)
    return 0.5 - 0.5 * math.cos(math.pi * (1 - t) / 0.2) if t > 0.8 else 1


ENVS = (_bell, _sinc, lambda t: 1 - abs(2 * t - 1), lambda t: (1 - t) ** 2, lambda t: t,
        _tukey, lambda t: 1)                  # BELL SINC TRI DECAY RAMP TUKEY SQUARE


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
        self.bg = bytearray(len(self.buf))    # WAVE without playhead + dots (animate() base)
        self.bg_key = self.box_ = None        # what bg shows / the wave box (x, y, w, h)
        self.clock, self.rand = time.ticks_ms, random.random
        self.g_list, self.g_acc, self.g_t, self.g_key, self.g_ph = [], 0, None, None, 0
        self.touch_on, self.touch, self.tb = True, None, None   # (knob, src, ms) / baseline
        self.touch_drawn = False
        self.dived, self.set_cur = False, 0   # SETTINGS: cursor shown / row
        self.testing = False

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
        """The static part (into bg, redrawn only when it changes); wave_live() adds the
        scan playhead + grain dots on top, every frame."""
        d, M, s, snap = self.d, self.M, self.snd(), self.snap
        pl = snap.get("playing") if snap and snap.get("connected") else None
        p = s[self.scene] if s else None
        ro = self.touch_text() if self.touch_recent() else None   # style B: knob readout
        hot = self.wave_hot()
        key = (self.sound, self.scene, pl, s and s["file"], p and p["START"], p and p["WRAP"],
               ro, hot)
        if key != self.bg_key:
            self.fb.fill(0)
            top = self.header()
            bot = self.status("WAVE", ro or "PLAY S%s" % (pl + 1 if pl is not None else "-"),
                              15 if ro else 10)
            h = bot - top - 2
            self.box_ = None
            if s and s["file"]:
                s0 = p["START"]
                self.box_ = (1, top, W - 2, h)
                self.draw_wave(1, top, W - 2, h, seed_of(s["file"]), s0, min(1, s0 + p["WRAP"]), hot)
            else:
                d.text(M, "no sample", (W - M.width("no sample")) >> 1, top + (h >> 1) + (M.cap >> 1), 5)
            self.bg[:] = self.buf
            self.bg_key = key
        else:
            self.buf[:] = self.bg
        self.wave_live(self.clock())

    def draw_wave(self, x, y, w, h, seed, s, e, hot=None):
        """Waveform band, window START..START+WRAP bright, START / WRAP markers (2 px wide
        while that knob is turned)."""
        d = self.d
        if self.wave_key != (w, seed):
            self.wave_key, self.wave = (w, seed), make_wave(w, seed)
        mid, bd = y + (h >> 1), band(h)
        for i, v in enumerate(self.wave):
            amp, win = jround(v * bd), s <= i / w <= e
            d.rect(x + i, mid - amp, 1, amp * 2 + 1, 9 if win else 3)
            d.px(x + i, mid - amp, 15 if win else 7)
            d.px(x + i, mid + amp, 15 if win else 7)
        for v, wide in ((s, hot == "START"), (e, hot == "WRAP")):
            mx = jround(v * (w - 1))
            d.rect(x + (mx - 1 if wide and mx == w - 1 else mx), y, 2 if wide else 1, h, 15)

    def wave_live(self, now):
        self.grains_step(now)
        if self.box_ is None:
            return
        x, y, w, h = self.box_
        sx = x + jround(self.scan_pos() * (w - 1))     # scan playhead: dotted, solid if turned
        if self.bg_key[-1] == "SCAN":
            self.d.rect(sx, y, 1, h, 15)
        else:
            vdots(self.buf, sx, y, h, 12)
        self.grains(x, y, w, h, now)

    # ---- grain dots ----
    def scan_pos(self):                       # playhead, 0..1 of the sample
        s = self.snd()
        p = s[self.scene] if s else None
        s0 = p["START"] if p else 0
        e = min(1, s0 + (p["WRAP"] if p else 0))
        return s0 + self.g_ph * (e - s0)

    def grain_rate(self, s, p, gms):          # grains launched per second
        snap = self.snap
        if snap.get("sync") == 1 and snap.get("clock_period"):
            return SYNC_MULT[sync_idx(p["RATE"])] / snap["clock_period"]
        return rate_linked_hz(p["RATE"], gms) if s["link_rs"] == 1 else rate_hz(p["RATE"])

    def grains_step(self, now):
        s, snap = self.snd(), self.snap
        dt = min(0.1, (time.ticks_diff(now, self.g_t) if self.g_t is not None else 0) / 1000)
        self.g_t = now
        key = (self.sound, s and s["file"])
        if key != self.g_key:
            self.g_key, self.g_list, self.g_acc, self.g_ph = key, [], 0, 0
        td = time.ticks_diff
        self.g_list = [g for g in self.g_list if td(now, g[2]) < g[3]]
        if not (s and s["file"] and snap and snap.get("connected") and snap.get("playing") == self.sound):
            self.g_acc = 0
            return
        p = s[self.scene]
        gms = grain_ms(p["SIZE"], p["PITCH"], s["link_sp"] == 1)
        life = max(GRAIN_MIN_MS, gms)
        dist = gms / 1000 * 2 ** (pitch_st(p["PITCH"]) / 12) / (1 + seed_of(s["file"]))
        self.g_acc = min(self.g_acc + dt * self.grain_rate(s, p, gms), GRAIN_MAX)
        while self.g_acc >= 1:
            x = self.scan_pos() + (self.rand() - 0.5) * GRAIN_SPREAD
            self.g_list.append((x, self.rand(), now, life, gms, dist))
            self.g_ph = ((self.g_ph + p["SCAN"] * SCAN_STEP) % 1 + 1) % 1
            self.g_acc -= 1
        if len(self.g_list) > GRAIN_MAX:      # oldest go first
            del self.g_list[:len(self.g_list) - GRAIN_MAX]

    @micropython.native
    def grains(self, x, y, w, h, now):
        """Dots above / below the band; one that lands on the bright wave is cut out.
        (Hot loop: rounding inlined as int(v + 0.5) - every value here is >= 0.)"""
        p, buf = self.snd()[self.scene], self.buf
        env = ENVS[shape_idx(p["SHAPE"])]
        k15 = 15 * math.sqrt(min(1, max(0, p["LEVEL"])))
        mid, gap = y + (h >> 1), band(h) + 2
        zone = max(0, (h >> 1) - gap - GRAIN_PX)
        up, dn, span, td = mid - gap - GRAIN_PX, mid + gap, w - GRAIN_PX, time.ticks_diff
        for gx0, gy0, t0, life, gms, dist in self.g_list:
            age = td(now, t0)
            v = int(k15 * env(age / life) + 0.5)
            if v < 1:
                continue
            f = age / gms
            xf = gx0 + dist * (f if f < 1 else 1)
            xf = 0 if xf < 0 else 1 if xf > 1 else xf
            dot(buf, x + int(xf * span + 0.5),
                up - int(gy0 * 2 * zone + 0.5) if gy0 < 0.5 else dn + int((gy0 - 0.5) * 2 * zone + 0.5),
                v)

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

    # ---- SETTINGS (the focused sound's; catalogue gv_cat.py) ----
    def sget(self, e):
        s = self.snd()
        return s["settings"].get(e["key"]) if s and s.get("settings") else None

    def s_list(self, items, cur, top, bot, show_cur):
        """label ...... value rows, cursor row inverted, scroll mark if they don't fit."""
        d, M = self.d, self.M
        rh = M.lh + 2
        rows, n = (bot - top) // rh, len(items)
        first = max(0, min(cur - (rows >> 1), max(0, n - rows)))
        sb = n > rows
        xr = W - (5 if sb else 2)
        for r in range(rows):
            i = first + r
            if i >= n:
                break
            e, y = items[i], top + r * rh
            on = show_cur and i == cur
            v = self.sget(e)
            by = y + 1 + M.asc
            if on:
                d.rect(0, y, xr + 2, rh, 15)
            d.text(M, e["label"], 2, by, 0 if on else 11)
            d.text_r(M, stext(e, v), xr, by,
                     0 if on else 5 if v is None else 8 if e["type"] == "info" else 15)
        if sb:
            th = max(4, jround((bot - top) * rows / n))
            ty = top + jround((bot - top - th) * first / (n - rows))
            d.rect(W - 2, top, 1, bot - top, 3)
            d.rect(W - 3, ty, 3, th, 12)

    def v_set(self):
        items = CAT["sound"]
        e = items[self.set_cur] if self.set_cur < len(items) else None
        top = self.header()
        bot = self.status("SETTINGS", e.get("panel", "") if self.dived and e else "PUSH EDIT")
        self.s_list(items, self.set_cur, top, bot, self.dived)

    def edit_start(self, e):                  # live module: nothing is editable yet
        v = self.sget(e)
        if e["type"] == "info":
            self.flash("read-only")
        elif v is None:
            self.flash("not mapped yet")
        elif self.snap and self.snap.get("mode") != "mock":
            self.flash("read-only (live)")

    # ---- knob touch ----
    def detect_touch(self):
        s = self.snd()
        if not s:
            self.tb = None
            return
        key, P, Md = (self.sound, self.scene), s[self.scene], s["mod"][self.scene]
        if self.tb is None or self.tb[0] != key:
            self.tb = (key, dict(P), {src: dict(Md[src]) for src in Md})
            return
        bp, bm = self.tb[1], self.tb[2]
        hits = []
        for k in MKEYS:
            dv = abs(P[k] - bp[k])
            if dv > TOUCH_EPS:                # in 1e-4 steps: equal moves tie (as the JS)
                hits.append((jround(dv * 1e4), k, None))
        for src in SOURCES:
            for k in MKEYS:
                dv = abs(Md[src][k] - bm[src][k])
                if dv > TOUCH_EPS:
                    hits.append((jround(dv * 1e4), k, src))
        for _, k, src in hits:                # baselines per value: slow turns add up
            if src:
                bm[src][k] = Md[src][k]
            else:
                bp[k] = P[k]
        if len(hits) >= BULK:                 # preset load etc. (also cancels a split one)
            self.touch = None
            return
        if not hits or not self.touch_on:
            return
        best = hits[0]
        for h in hits[1:]:                    # biggest move; ties: the first (as the JS sort)
            if h[0] > best[0]:
                best = h
        self.touch = (best[1], best[2], time.ticks_ms())

    def touch_recent(self):
        t = self.touch
        return bool(self.touch_on and t and time.ticks_diff(time.ticks_ms(), t[2]) < TOUCH_MS
                    and self.snd())

    def wave_hot(self):                       # the knob being turned (not a mod depth)
        return self.touch[0] if self.touch_recent() and not self.touch[1] else None

    def touch_active(self):                   # hero instead of the view?
        if not self.touch_recent() or self.view == "SETTINGS" and self.dived:
            return False
        return self.view != "WAVE"            # WAVE (style B): the status-line readout

    def touch_text(self):
        k, src, _ = self.touch
        if src:
            return src + ">" + k + " " + fmt(self.snd()["mod"][self.scene][src][k], True)
        return k + " " + self.pval(k)

    def uctx_of(self, sc):
        s = self.snd()
        return {"link_rs": s["link_rs"] == 1, "link_sp": s["link_sp"] == 1,
                "sync": self.snap.get("sync") == 1, "size": s[sc]["SIZE"], "pitch": s[sc]["PITCH"]}

    def v_touch(self):
        """Hero: the touched value big, a position bar, the other scene's value."""
        d, T, X = self.d, self.T, FONT("X")
        top = self.header()
        bot = self.status(self.view, "SCENE " + self.scene)
        k, src, _ = self.touch
        s, o = self.snd(), "B" if self.scene == "A" else "A"
        v = s["mod"][self.scene][src][k] if src else s[self.scene][k]
        ov = s["mod"][o][src][k] if src else s[o][k]
        bip = bool(src or k in BIPOLAR)

        def show(x, sc):
            return fmt(x, True) if src else unit_text(k, x, self.uctx_of(sc))
        val, bar_h = show(v, self.scene), 6
        block_h = T.lh + 3 + X.lh + 4 + bar_h + 5 + T.lh
        y = top + max(0, (bot - top - block_h) >> 1)          # centre the block
        d.text(T, src + " > " + k if src else k, 2, y + T.asc, 12)
        d.text_r(T, "DEPTH" if src else "SCENE " + self.scene, W - 2, y + T.asc, 6)
        y += T.lh + 3
        d.text(X, val, (W - X.width(val)) >> 1, y + X.asc, 15)
        y += X.lh + 4
        bx, bw = 4, W - 8
        d.frame(bx, y, bw, bar_h, 6)                           # position bar
        if bip:
            c, ln = bx + (bw >> 1), jround((bw / 2 - 1) * min(1, abs(v)))
            d.rect(c - ln if v < 0 else c, y + 1, ln, bar_h - 2, 13)
            d.rect(c, y - 1, 1, bar_h + 2, 10)
        else:
            d.rect(bx + 1, y + 1, jround((bw - 2) * min(1, max(0, v))), bar_h - 2, 13)
        y += bar_h + 5
        d.text(T, "SCENE " + o, 2, y + T.asc, 6)
        d.text_r(T, show(ov, o), W - 2, y + T.asc, 8)

    # ---- render / input ----
    def render(self, snap):
        if snap and snap.get("_steps"):
            return self.render_scripted(snap)
        self.update(snap)
        if self.view == "WAVE" and not self.touch_active():
            self.v_wave()
        else:
            self.bg_key = None
            self.fb.fill(0)
            if self.touch_active():
                self.v_touch()
            elif self.view == "PARAM":
                self.v_param()
            elif self.view == "MOD":
                self.v_mod()
            else:
                self.v_set()
        self.overlays()
        self.touch_drawn = self.touch_recent()

    def update(self, snap):
        self.snap = snap
        if snap and snap.get("connected"):
            self.sound = snap["selected"] if 0 <= snap["selected"] < 8 else self.sound
            self.scene = snap.get("edit_scene") or self.scene
            if not self.testing:
                self.detect_touch()

    def overlays(self):
        snap = self.snap
        if self.flash_msg and time.ticks_diff(self.flash_until, time.ticks_ms()) > 0:
            self.box(self.flash_msg)
        elif not (snap and snap.get("connected")):
            self.box("NO MODULE LINK")

    def animating(self):
        """WAVE with dots alive or being launched (else frames wouldn't change)."""
        s, snap = self.snd(), self.snap
        return (self.view == "WAVE" and self.bg_key is not None
                and (bool(self.g_list) or bool(s and s["file"] and snap.get("playing") == self.sound)))

    def animate(self):
        if not self.animating():
            return None
        key = self.bg_key
        self.v_wave()                         # bg (redrawn if update() changed it) + live
        self.overlays()                       # (the flash box sits inside the wave box)
        b = self.box_
        return (b[1], b[3]) if b and self.bg_key == key else (0, H)

    def render_scripted(self, snap):
        """Tests: one render per snap["_steps"] clock value, randoms from snap["_rand"]."""
        r = list(snap.get("_rand", ()))
        clock, rand = self.clock, self.rand
        kept = self.touch, self.tb, self.dived, self.set_cur
        self.rand = lambda: r.pop(0)
        self.g_list, self.g_acc, self.g_t, self.g_key, self.g_ph = [], 0, None, None, 0
        self.bg_key, self.testing = None, True
        tt = snap.get("_touch")
        self.touch = (tt[0], tt[1], time.ticks_ms()) if tt else None
        if snap.get("_prev"):                 # detection over a scripted run of polls
            self.tb, self.testing = None, False
            for p in snap["_prev"] + [snap]:
                self.update(p)
            self.testing = True
        self.dived, self.set_cur = bool(snap.get("_dived")), snap.get("_setCur", 0)
        live = {k: v for k, v in snap.items() if k != "_steps"}
        try:
            for t in snap["_steps"]:
                self.clock = lambda: t
                self.render(live)
        finally:
            self.clock, self.rand, self.testing = clock, rand, False
            self.touch, self.tb, self.dived, self.set_cur = kept
            self.g_list, self.g_acc, self.g_t, self.g_key, self.g_ph = [], 0, None, None, 0
            self.bg_key = None

    def flash(self, msg):
        self.flash_msg, self.flash_until = msg, time.ticks_add(time.ticks_ms(), FLASH_MS)

    def wake_due(self):
        """True once when a flash box or the knob hero / readout has just run out (main.py
        redraws then)."""
        if self.flash_msg and time.ticks_diff(self.flash_until, time.ticks_ms()) <= 0:
            self.flash_msg = None
            return True
        if self.touch_drawn and not self.touch_recent():
            self.touch_drawn = False
            return True
        return False

    def enc(self, n):
        if self.view == "SETTINGS" and self.dived:
            self.set_cur = max(0, min(len(CAT["sound"]) - 1, self.set_cur + n))
        else:                                 # page the views (clamped, as the emulator)
            i = VIEWS.index(self.view) + n
            self.view = VIEWS[max(0, min(len(VIEWS) - 1, i))]

    def btn(self, name):
        if name == "VIEW":
            self.dived = False
            self.view = VIEWS[(VIEWS.index(self.view) + 1) % len(VIEWS)]
        elif name == "BACK":
            if self.dived:
                self.dived = False
            else:
                self.view = "WAVE"
        elif name in ("SOUND<", "SOUND>"):
            n = (self.sound + (7 if name == "SOUND<" else 1)) % 8
            self.sound = n
            return ("select", n)
        elif name == "PUSH" and self.view == "SETTINGS":
            if not self.dived:
                self.dived = True
            else:
                self.edit_start(CAT["sound"][self.set_cur])
        elif name == "PUSH":
            self.flash("-" if self.view == "WAVE" else "view-only")
        else:                                 # FILE, A/B, SETUP
            self.flash("on the Mac (soon)")
        return None
