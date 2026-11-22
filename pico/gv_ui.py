# GRAINVIEW UI on the Pico, drawn from its own poll (mgpoll.py). A port of the emulator
# (tools/grainview_emulator.html, the spec): same layout maths, same fonts, so the frames
# match pixel for pixel - check with: tools/venv/bin/python tools/gv_pico.py ui PARAM
# Ported so far: header, status line, WAVE (waveform + animated grain dots, style B with
# the knob readout), PARAM, MOD, SETTINGS (every sound setting editable, + the quantizer
# keyboard page), the SETUP overlay (MODULE / PRESET editable; GRAINVIEW's own settings
# kept in CFG on flash), the FILE overlay (the card's folders, load a WAV, the PRESETS / PROJECTS
# slot menus), SOUND<> + A/B (the module's selected sound / edited scene), Live Sounds
# (SETTINGS > Type, the SOUND< + SOUND> chord, LIVE in the header), the knob-touch
# hero, the NO MODULE LINK / flash boxes - everything the emulator has.
#
#   ui = UI()
#   ui.render(snap)                     # into ui.buf (128x128 GS4, the SSD1327's layout)
#   ui.update(snap)                     # new data only; the next animate() draws it
#   ui.animate()                        # WAVE: next grain frame (~30 fps) -> the rows it
#                                       # changed (r0, n), or None
#   act = ui.btn("SOUND>")              # -> None or an action for main.py to do over SWD:
#                                       # ("select", n, play) ("scene", "A"|"B")
#                                       # ("root",) ("files", folder)
#                                       # ("load", folder, index, name)
#                                       # ("store", "preset"|"project", action, n, ...)
#                                       # ("rec", action, n) (RECORD: mg_rec.rec_do)
#                                       # ("live", n, 0|1) (SETTINGS > Type, or "LIVE" =
#                                       # main.py's SOUND< + SOUND> chord)
#                                       # ("set", key, value, sound or None) (mgset.write)
#   ui.done(act, res, err)              # ...and what came of it (the emulator's api() reply)
# A snapshot with "_steps" (clock values, ms) + "_rand" (random numbers) renders once per
# step with those - the same script the emulator runs in tools/gv_render.js (tests); also
# "_touch": [knob, mod source or null], "_dived", "_setCur" set that UI state for the test;
# "_setup": [group or null, group cursor, row] opens SETUP, "_edit": the cursor row's value
# being edited; "_gv": {"selPlays", "touchOn"} (else the defaults); "_prev": earlier
# snapshots fed through the knob-touch detection first (as polls); "_file": {"folder",
# "files" (a WAV folder's names), "cur", "ok", "counts", "menu": [cur, armed]} opens FILE
# there; "_flash": [message, label] shows that box; "_rec": [row, armed row or null] opens
# RECORD (FILE > RECS) there; "_dived" + "_edit": the SETTINGS row being edited; "_quant":
# [cursor, edit or None] opens SETTINGS > Quantizer.
import json
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
REC_RATE = 48000
REC_TAG = {"armed": "ARM", "pending": "TAKE", "frozen": "FRZ", "wait": "WAIT"}   # + "REC 12s"
REC_WORD = {"idle": "STOPPED", "listen": "LISTENING", "armed": "ARMED", "rec": "RECORDING",
            "pending": "TAKE", "loop": "LOOPING", "wait": "WAITING", "frozen": "FROZEN"}


def rec_secs(fr):                             # frames -> "12.3s" (tenths, rounded down)
    t = max(0, fr) * 10 // REC_RATE
    return "%d.%ds" % (t // 10, t % 10)


def rec_whole(fr):
    return "%ds" % (max(0, fr) // REC_RATE)
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
# SETUP overlay: the emulator's SETUP_GROUPS (None = not there yet); GRAINVIEW's own
# settings live in CFG (the emulator: localStorage)
SETUP_GROUPS = (("MODULE", "module"), ("PRESET", "preset"), ("SAMPLE", None), ("GRAINVIEW", "gv"))
CFG = "gv_cfg.json"
ONOFF = ("OFF", "ON")
# FILE overlay: the card's folders (the emulator's FOLDERS / FNAME); PRESETS / PROJECTS = the
# SLOTS of each, from the poll's "store" (no fetch)
FOLDERS = ("project", "Wavs", "Recs", "PRESETS", "PROJECTS")
FNAME = {"project": "PROJECT", "Wavs": "WAVS", "Recs": "RECS", "PRESETS": "PRESETS",
         "PROJECTS": "PROJECTS"}
SLOTS = 48
NO_STORE = {"projects": (), "presets": (), "locked": (), "project": None, "preset": None}


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


def q_transpose(q, d):                        # the scale moved with its root (p.33)
    return {"root": (q["root"] + d) % 12, "notes": [q["notes"][(i - d) % 12] for i in range(12)]}


WHITE, BLACK_L = (0, 2, 4, 5, 7, 9, 11), {1: 0, 3: 1, 6: 3, 8: 4, 10: 5}   # black -> white on its left


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
        self.flash_msg, self.flash_label, self.flash_until = None, None, 0
        self.wave_key = self.wave = None      # cached synthetic waveform
        self.bg = bytearray(len(self.buf))    # WAVE without playhead + dots (animate() base)
        self.bg_key = self.box_ = None        # what bg shows / the wave box (x, y, w, h)
        self.clock, self.rand = time.ticks_ms, random.random
        self.g_list, self.g_acc, self.g_t, self.g_key, self.g_ph = [], 0, None, None, 0
        self.touch_on, self.touch, self.tb = True, None, None   # (knob, src, ms) / baseline
        self.touch_drawn = False
        self.dived, self.set_cur = False, 0   # SETTINGS: cursor shown / row
        self.overlay, self.setup = None, [None, 0, 0]   # "SETUP" / [group, group cursor, row]
        self.edit = None                      # [group, entry, value, value before]
        self.quant = None                     # SETTINGS > Quantizer: {cur, edit} (vQuant)
        self.folder, self.files, self.file_cur = "", [], 0   # FILE: "ROOT" / a folder, its rows
        self.files_ok, self.root_counts = False, {}   # list read / WAV counts at the root
        self.menu = None                      # slot menu: [title, items, cur, armed]
        self.rec_cur, self.rec_armed, self.rec_phase = 0, None, None   # RECORD: row / 2nd push
        self.sel_plays = False                # SOUND<> also switches playback
        self.wifi_on, self.net = True, None   # WiFi wanted / its status (main.py sets it)
        self.on_wifi = None                   # main.py: turn WiFi on / off
        self.load_cfg()
        # SETUP > GRAINVIEW (the emulator's GV_SETTINGS; one wave style + font set here)
        self.gv = (
            {"label": "Sel plays", "type": "enum", "options": ONOFF,
             "get": lambda: int(self.sel_plays), "set": lambda v: setattr(self, "sel_plays", bool(v))},
            {"label": "Knob view", "type": "enum", "options": ONOFF,
             "get": lambda: int(self.touch_on), "set": lambda v: setattr(self, "touch_on", bool(v))},
            {"label": "Wave style", "type": "enum", "options": ("B",), "get": lambda: 0},
            {"label": "Font", "type": "enum", "options": ("Spleen",), "get": lambda: 0},
            {"label": "Link", "type": "info", "get": self.link_text},
            {"label": "Firmware", "type": "info",   # the module's, as checked (main.py)
             "get": lambda: self.snap and (self.snap.get("firmware") or self.snap.get("fw")) or "-"},
            {"label": "WiFi", "type": "enum", "options": ONOFF,   # the panel in a browser (gvnet.py)
             "get": lambda: int(self.wifi_on), "set": self.set_wifi},
            {"label": "IP", "type": "info", "get": lambda: self.net or "-"})
        self.testing = False

    # ---- data ----
    def snd(self):
        s = self.snap
        return s["sounds"][self.sound] if s and s.get("sounds") else None

    def live(self):                           # the focused sound is a Live Sound?
        s = self.snd()
        return bool(s) and bool(s.get("settings")) and s["settings"].get("type") == 1

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
        xr, tag = W - bw - 3, self.rec_tag()
        if tag:                               # the recorder, when it's doing something
            tw, hot = self.T.width(tag) + 4, tag == "ARM" or tag.startswith("REC")
            xr -= tw + 2
            d.rect(xr + 2, 1, tw, lh - 1, 15 if hot else 7)
            d.text(self.T, tag, xr + 4, base - 1, 0)
        live = self.live()
        name = "LIVE" if live else s["file"] if s and s["file"] else "- empty -"
        d.text(M, fit(M, name, xr - x), x, base, 15 if live else 11 if s and s["file"] else 5)
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
        key = (self.sound, self.scene, pl, s and s["file"], self.live(), self.rec_tag(),
               p and p["START"], p and p["WRAP"], ro, hot)   # (the header's too; hot last: wave_live)
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

    # ---- SETTINGS (the focused sound's) + SETUP (catalogue gv_cat.py; GRAINVIEW: self.gv) ----
    def items(self, g):
        return self.gv if g == "gv" else CAT[g]

    def sget(self, g, e):                     # None = not mapped on the live module (yet)
        if g == "gv":
            return e["get"]()
        if g == "sound":
            s = self.snd()
            src = s and s.get("settings")
        else:
            src = self.snap and self.snap.get("settings") and self.snap["settings"].get(g)
        return src.get(e["key"]) if src else None

    def link_text(self):
        s = self.snap
        if not s:
            return "-"
        return (s.get("mode") or "swd").upper() + ("" if s.get("connected") else " X")

    def s_list(self, g, items, cur, top, bot, show_cur):
        """label ...... value rows, cursor row inverted (just its value while editing),
        scroll mark if they don't fit."""
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
            ed = on and self.edit is not None
            v = self.edit[2] if ed else self.sget(g, e)
            vt, by = stext(e, v), y + 1 + M.asc
            if on and not ed:
                d.rect(0, y, xr + 2, rh, 15)
            d.text(M, e["label"], 2, by, 0 if on and not ed else 15 if ed else 11)
            if ed:
                vw = M.width(vt)
                d.rect(xr - vw - 2, y, vw + 4, rh, 15)
                d.text_r(M, vt, xr, by, 0)
            else:
                d.text_r(M, vt, xr, by,
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
        bot = self.status("SETTINGS", "PUSH OK" if self.edit else
                          e.get("panel", "") if self.dived and e else "PUSH EDIT")
        self.s_list("sound", items, self.set_cur, top, bot, self.dived)

    # ---- quantizer keyboard page (the emulator's vQuant: SETTINGS > Quantizer, p.33) ----
    def q_now(self):                          # pending edit wins
        S, ed = self.snd()["settings"], self.quant["edit"]
        q = ed and ed.get("q") or S["quantizer"]
        return q, ed["mode"] if ed and ed.get("mode") is not None else S["quant_mode"]

    def q_write(self, q, mode=None):
        S = self.snd()["settings"]            # (shown now; the poll after the write confirms)
        if q:
            S["quantizer"] = q
            return ("set", "quantizer", q, self.sound)
        if mode is not None and mode != S["quant_mode"]:
            S["quant_mode"] = mode
            return ("set", "quant_mode", mode, self.sound)
        return None

    def q_enc(self, n):
        Q = self.quant
        if not Q["edit"]:
            Q["cur"] = max(0, min(13, Q["cur"] + n))
        elif Q["cur"] == 12:
            Q["edit"]["q"] = q_transpose(Q["edit"]["q"], n)
        else:
            Q["edit"]["mode"] = max(0, min(1, Q["edit"]["mode"] + n))

    def q_push(self):
        Q = self.quant
        q, mode = self.q_now()
        if Q["cur"] < 12:
            notes = list(q["notes"])
            notes[Q["cur"]] = not notes[Q["cur"]]
            return self.q_write({"root": q["root"], "notes": notes})
        if not Q["edit"]:
            Q["edit"] = {"q": q} if Q["cur"] == 12 else {"mode": mode}
            return None
        ed, Q["edit"] = Q["edit"], None
        return self.q_write(ed.get("q"), ed.get("mode"))

    def v_quant(self):
        d, T, M, Q = self.d, self.T, self.M, self.quant
        q, mode = self.q_now()
        top = self.header()
        self.status("QUANTIZER", "PUSH OK" if Q["edit"] else "PUSH NOTE" if Q["cur"] < 12
                    else "PUSH ROOT" if Q["cur"] == 12 else "PUSH EDIT")
        kw, kh, x0, y0, bw, bh = 18, 40, 1, top + 2, 11, 24

        def key(n):
            if n in WHITE:
                return x0 + WHITE.index(n) * kw, y0, kw + 1, kh
            return x0 + (BLACK_L[n] + 1) * kw - (bw >> 1), y0, bw, bh

        for n in WHITE + (1, 3, 6, 8, 10):
            x, y, w, h = key(n)
            on, root = q["notes"][n], n == q["root"]
            d.rect(x + 1, y + 1, w - 2, h - 2, (15 if root else 10) if on else 0 if n in WHITE else 3)
            d.frame(x, y, w, h, 15 if Q["cur"] == n else 7)
            if root:                          # root dot
                d.rect(x + (w >> 1) - 1, y + h - 6, 3, 3, 0 if on else 12)
        if Q["cur"] < 12:                     # caret under the key
            x, _, w, _ = key(Q["cur"])
            cx = x + (w >> 1)
            for i in range(3):
                d.rect(cx - i, y0 + kh + 2 + i, 2 * i + 1, 1, 15)
        y = y0 + kh + 7                       # scale name
        n, sc = sum(1 for x in q["notes"] if x), scale_of(q)
        name = ("OFF - NO NOTES" if not n else ("" if sc[0] == "CHROM" else NOTE[q["root"]] + " ")
                + sc[1] if sc else "%d%s" % (n, " NOTES" if n > 1 else " NOTE"))
        d.text(T, name, (W - T.width(name)) >> 1, y + T.asc, 12 if n else 6)
        y += T.lh + 3
        for c, (lab, val, i) in enumerate((("ROOT", NOTE[q["root"]], 12),
                                           ("QUANT ON", ("ALL", "MOD ONLY")[mode], 13))):
            x, on = 1 + c * 64, Q["cur"] == i
            ed = on and Q["edit"]
            if on and not ed:
                d.rect(x - 1, y, 63, T.lh + M.lh + 2, 15)
            d.text(T, lab, x, y + T.asc, 0 if on and not ed else 8)
            if ed:
                d.rect(x - 1, y + T.lh + 1, M.width(val) + 2, M.lh + 1, 15)
            d.text(M, val, x, y + T.lh + 1 + M.asc, 0 if on else 15)

    def v_setup(self):
        """SETUP overlay: the groups, then a group's list."""
        d, T, M = self.d, self.T, self.M
        top = self.header()
        g, gc, cur = self.setup
        if g is None:
            bot = self.status("SETUP", "PUSH OPEN")
            rh = M.lh + 2
            for i, (name, grp) in enumerate(SETUP_GROUPS):
                y, on = top + i * rh, i == gc
                by = y + 1 + M.asc
                tag = str(len(self.items(grp))) if grp else "soon"
                if on:
                    d.rect(0, y, W, rh, 15)
                d.text(M, name, 2, by, 0 if on else 12 if grp else 5)
                d.text_r(T, tag, W - 2, by - (M.asc - T.asc), 0 if on else 8)
            return
        name, grp = SETUP_GROUPS[g]
        items = self.items(grp)
        e = items[cur] if cur < len(items) else None
        bot = self.status("SETUP>" + name, "PUSH OK" if self.edit else
                          e and e.get("panel") or "PUSH EDIT")
        self.s_list(grp, items, cur, top, bot, True)

    def edit_start(self, g, e):
        v = self.sget(g, e)
        if e["type"] == "info":
            self.flash("read-only")
        elif v is None:
            self.flash("not mapped yet")
        elif e["type"] == "quant":            # its own keyboard page
            self.quant = {"cur": v["root"], "edit": None}
        elif e["type"] in ("enum", "num"):
            self.edit = [g, e, v, v]

    def edit_step(self, n):
        e, v = self.edit[1], self.edit[2]
        if e["type"] == "enum":
            v = max(0, min(len(e["options"]) - 1, v + n))
        else:
            v = round(max(e["min"], min(e["max"], v + n * e["step"])), e["dp"])
        self.edit[2] = v

    def edit_commit(self):
        g, e, v, v0 = self.edit
        self.edit = None
        if v != v0 and g == "gv" and "set" in e:
            e["set"](v)
            self.save_cfg()
        elif v != v0 and g == "sound" and e["key"] == "type":
            return ("live", self.sound, v)
        elif v != v0:                         # the module's setter (main.py: mgset.write)
            return ("set", e["key"], v, self.sound if g == "sound" else None)
        return None

    def load_cfg(self):
        try:
            with open(CFG) as f:
                c = json.load(f)
            self.sel_plays, self.touch_on = bool(c.get("selPlays")), c.get("touchOn", 1) != 0
            self.wifi_on = c.get("wifi", 1) != 0
        except (OSError, ValueError):
            pass

    def save_cfg(self):
        try:
            with open(CFG, "w") as f:
                json.dump({"selPlays": int(self.sel_plays), "touchOn": int(self.touch_on),
                           "wifi": int(self.wifi_on)}, f)
        except OSError as x:
            self.flash("not saved: " + str(x))

    def set_wifi(self, v):
        self.wifi_on = bool(v)
        if self.on_wifi:
            self.on_wifi(self.wifi_on)

    # ---- FILE (the card; PRESETS / PROJECTS = slots + a menu) ----
    def store(self):
        return self.snap and self.snap.get("store") or NO_STORE

    def is_store(self, f=None):
        return (self.folder if f is None else f) in ("PRESETS", "PROJECTS")

    def file_lo(self):                        # rows run from -1 ('..' = up to the root);
        return 0 if self.folder == "ROOT" else -2 if self.folder == "Recs" else -1   # Recs: -1 RECORD

    def root_row(self, y, rh, f, on):
        """NAME ...... [CUR] count  (CUR = the selected sound's WAV folder)."""
        d, T, M, S, s = self.d, self.T, self.M, self.store(), self.snd()
        if on:
            d.rect(0, y, W, rh, 15)
        n = len(S["presets" if f == "PRESETS" else "projects"]) if self.is_store(f) \
            else self.root_counts.get(f)
        tag = (("CUR " if s and s["folder"] == f else "") + ("" if n is None else str(n))).strip()
        d.text(M, "/" + FNAME[f], 2, y + M.asc, 0 if on else 12)
        d.text_r(T, tag, W - 2, y + T.asc, 0 if on else 8)

    def slot_row(self, y, rh, i, on):
        """NN PresetNN ...... [LCK] [CUR]"""
        d, T, M, S = self.d, self.T, self.M, self.store()
        pre = self.folder == "PRESETS"
        have = i in S["presets" if pre else "projects"]
        cur = S["preset" if pre else "project"] == i
        lock = pre and i in S["locked"]
        if on:
            d.rect(0, y, W, rh, 15)
        nn, ty = "%02d" % (i + 1), y + T.asc
        d.text(T, nn, 2, ty, 0 if on else 7)
        x = 4 + T.width("00") + 3
        tags = (("LCK " if lock else "") + ("CUR" if cur else "")).strip()
        if tags:
            d.text_r(T, tags, W - 2, ty, 0 if on else 15 if cur else 8)
        nm = ("Preset" if pre else "Project") + nn if have else "- empty -"
        d.text(M, fit(M, nm, W - x - 4 - (T.width(tags) + 3 if tags else 0)), x, y + M.asc,
               0 if on else 12 if have else 5)

    def v_file(self):
        d, M, F = self.d, self.M, self.files
        top = self.header()
        root = self.folder == "ROOT"
        bot = self.status("FILE /" + ("" if root else FNAME.get(self.folder, "")),
                          "" if root or not F or self.file_cur < 0
                          else "%d/%d" % (self.file_cur + 1, len(F)))
        rh = M.lh + 1
        rows, lo = (bot - top) // rh, self.file_lo()
        first = lo + max(0, min(self.file_cur - lo - (rows >> 1), len(F) - lo - rows))
        for r in range(rows):
            i = first + r
            if i >= len(F):
                break
            y, on = top + r * rh, i == self.file_cur
            if i < 0:
                if on:
                    d.rect(0, y, W, rh, 15)
                if i == lo:
                    d.text(M, "..", 2, y + M.asc, 0 if on else 9)
                else:                         # Recs: the recorder
                    d.text(M, "RECORD", 2, y + M.asc, 0 if on else 15)
                    d.text_r(self.T, self.rec_tag() or "", W - 2, y + M.asc, 0 if on else 8)
                if i == -1 and not F:
                    sd = self.snap and self.snap.get("sd_state")
                    d.text(M, "SD error" if sd == 3 else "empty folder" if self.files_ok
                           else "loading list...", 2, y + rh + M.asc + 2, 8)
            elif root:
                self.root_row(y, rh, F[i], on)
            elif self.is_store():
                self.slot_row(y, rh, i, on)
            else:
                if on:
                    d.rect(0, y, W, rh, 15)
                d.text(M, fit(M, F[i], W - 4), 2, y + M.asc, 0 if on else 12)
        if self.menu:
            self.v_menu()

    def v_menu(self):
        d, T, M = self.d, self.T, self.M
        title, items, cur, armed = self.menu
        rh, lt = M.lh + 2, T.lh + 2
        w = max([T.width(title)] + [M.width(it[0]) for it in items]) + 14
        h = lt + len(items) * rh + 4
        x, y = (W - w) >> 1, (H - h) >> 1
        d.rect(x - 1, y - 1, w + 2, h + 2, 0)
        d.frame(x, y, w, h, 15)
        d.text(T, title if armed is None else "PUSH AGAIN", x + 4, y + 2 + T.asc,
               9 if armed is None else 15)
        for i, it in enumerate(items):
            yy, on = y + lt + 2 + i * rh, i == cur
            if on:
                d.rect(x + 2, yy, w - 4, rh, 15)
            d.text(M, it[0], x + 5, yy + 1 + M.asc, 0 if on else 12)

    # ---- the recorder (snap["rec"]: phase / take / fill / size in frames @48k, free sounds) ----
    def rec(self):
        s = self.snap
        return s.get("rec") if s and s.get("connected") else None

    def rec_tag(self):
        r = self.rec()
        if not r:
            return None
        p = r["phase"]
        return "REC " + rec_whole(r["take"]) if p == "rec" else REC_TAG.get(p)

    def rec_items(self):
        """(label, action, sound, needs a 2nd push) - what makes sense now."""
        r = self.rec()
        if not r:
            return []
        p, it = r["phase"], []
        if p == "pending":
            it.append(("SAVE TO RECS", "save", None, False))
            for n in r["free"]:
                it.append(("SAVE TO S%d" % (n + 1), "assign", n, False))
            it.append(("DISCARD", "discard", None, True))
        elif r["mode"] == 2:
            it.append(("UNFREEZE" if p == "frozen" else "FREEZE", "press", None, False))
            it.append(("KEEP LOOP", "grab", None, False))
        elif p == "armed":
            it.append(("CANCEL", "press", None, False))
        elif p == "rec":
            it.append(("STOP", "press", None, False))
        else:
            it.append(("START", "press", None, False))
            if r["state"] in (1, 3) and r["fill"] >= 4800:
                it.append(("GRAB LAST " + rec_whole(r["fill"]), "grab", None, False))
        return it

    def rec_sync(self):                       # a new state: cursor back to the top
        r = self.rec()
        p = r["phase"] if r else None
        if p != self.rec_phase:
            self.rec_phase, self.rec_cur, self.rec_armed = p, 0, None
        self.rec_cur = max(0, min(self.rec_cur, len(self.rec_items()) - 1))

    def v_rec(self):
        d, T, M, L = self.d, self.T, self.M, FONT("L")
        top = self.header()
        r = self.rec()
        self.rec_sync()
        bot = self.status("RECORD", "PUSH OK" if self.rec_armed is None else "PUSH AGAIN")
        if not r:
            return
        p = r["phase"]
        fr = r["take"] if p in ("rec", "pending") else 0 if p == "armed" else r["fill"]
        y = top + 1
        d.text(M, REC_WORD.get(p, p), 2, y + M.asc, 15 if p in ("rec", "armed") else 12)
        d.text_r(T, "LOOPER" if r["mode"] == 2 else "RESAMPLE" if r["mode"] == 1 else "INPUT",
                 W - 2, y + M.asc, 8)
        y += M.lh + 1
        d.text(L, rec_secs(fr), 2, y + L.asc, 15)
        d.text_r(T, "/ " + rec_whole(r["size"]), W - 2, y + L.asc, 8)
        y += L.lh + 2
        d.rect(2, y, W - 4, 3, 3)
        if r["size"] > 0:
            d.rect(2, y, (W - 4) * min(fr, r["size"]) // r["size"], 3, 15 if p == "rec" else 10)
        y += 6
        it, rh = self.rec_items(), M.lh + 2
        rows = max(1, (bot - y) // rh)
        first = max(0, min(self.rec_cur - (rows >> 1), len(it) - rows))
        for k in range(rows):
            i = first + k
            if i >= len(it):
                break
            yy, on = y + k * rh, i == self.rec_cur
            if on:
                d.rect(0, yy, W, rh, 15)
            d.text(M, it[i][0], 2, yy + 1 + M.asc, 0 if on else 12)

    def open_rec(self):
        self.overlay, self.menu, self.rec_phase = "REC", None, None
        self.rec_sync()

    def rec_push(self):
        it = self.rec_items()
        if self.rec_cur >= len(it):
            return None
        _, action, n, confirm = it[self.rec_cur]
        if confirm and self.rec_armed != self.rec_cur:
            self.rec_armed = self.rec_cur
            return None
        self.rec_armed = None
        return ("rec", action, n)

    def open_root(self, frm):
        """The card's root, cursor on the folder we came up from (WAV counts: main.py)."""
        self.menu, self.overlay, self.folder = None, "FILE", "ROOT"
        self.files, self.files_ok = list(FOLDERS), True
        self.file_cur = FOLDERS.index(frm) if frm in FOLDERS else 0
        return ("root",)

    def open_files(self, folder=None):
        """A folder (None = the selected sound's): its names come from main.py (-> done());
        PRESETS / PROJECTS are the slots, cursor on the current one."""
        self.menu, self.overlay = None, "FILE"
        self.files, self.files_ok, self.folder, self.file_cur = [], False, folder or "", -1
        if not self.is_store(folder):
            return ("files", folder)
        c = self.store()["preset" if folder == "PRESETS" else "project"]
        self.files, self.files_ok, self.file_cur = list(range(SLOTS)), True, 0 if c is None else c
        return None

    def open_menu(self):
        """A slot's menu: items (label, action, needs a 2nd push); BACK closes it."""
        S, n = self.store(), self.file_cur
        nn = "%02d" % (n + 1)
        items = []
        if self.folder == "PRESETS":
            have, lock, what = n in S["presets"], n in S["locked"], "Preset" + nn
            if have:
                items.append(("LOAD", ("store", "preset", "load", n, what, "LOADING", True), False))
            if not lock:
                items.append(("OVERWRITE" if have else "SAVE",
                              ("store", "preset", "save", n, what, "SAVING", False), have))
            if have:
                items.append(("UNLOCK" if lock else "LOCK", ("store", "preset", "lock", n, what,
                                                             "UNLOCKING" if lock else "LOCKING", False), False))
            title = "PRESET " + nn
        else:
            if n not in S["projects"]:
                self.flash("empty slot")
                return
            what = "Project" + nn
            if S["project"] == n:
                items.append(("SAVE NOW", ("store", "project", "save", n, what, "SAVING", False), False))
            else:
                items.append(("OPEN", ("store", "project", "load", n, what, "OPENING", True), False))
            title = "PROJECT " + nn
        items.append(("BACK", None, False))
        self.menu = [title, items, 0, None]

    def menu_push(self):
        m = self.menu
        _, act, confirm = m[1][m[2]]
        if not act:
            self.menu = None
        elif confirm and m[3] != m[2]:
            m[3] = m[2]
        else:
            self.menu = None
            return act
        return None

    def done(self, act, res=None, err=None):
        """main.py did act (from btn()): res = what it returned, err = why it failed."""
        k = act[0]
        if k == "root":                       # counts are extras: a failure leaves them
            if err is None:
                self.root_counts.update(res)
        elif k == "files":
            if err is not None:
                self.overlay = None
                self.flash(err)
            else:
                self.folder, cur, self.files = res
                self.files_ok = True
                self.file_cur = max(0, min(len(self.files) - 1, cur)) if self.files else -1
        elif err is not None:
            self.flash(err)
        elif k == "load":
            self.overlay = None
            self.flash(act[3], "LOADING")
        elif k == "rec":
            if act[1] == "save":
                self.flash("TO RECS", "SAVING")
            elif act[1] == "assign":
                self.flash("TO S%d" % (act[2] + 1), "SAVING")
            elif act[1] == "discard":
                self.flash("DISCARDED", "TAKE")
        elif k == "live":
            s = self.snap["sounds"][act[1]] if self.snap and self.snap.get("sounds") else None
            if s and s.get("settings"):       # show it now; the next poll confirms
                s["settings"]["type"] = act[2]
            self.flash("LIVE" if act[2] else "SAMPLE", "S%d" % (act[1] + 1))
        elif k == "set":                      # show it now; the poll after the write confirms
            if act[3] is not None:
                s = self.snap["sounds"][act[3]] if self.snap and self.snap.get("sounds") else None
                src = s and s.get("settings")
            else:
                st = self.snap and self.snap.get("settings")
                src = st and next((st[g] for g in ("module", "preset") if act[1] in st[g]), None)
            if src is not None:
                src[act[1]] = act[2]
        elif k == "store":
            if act[6]:
                self.overlay = None
            self.flash(act[4], act[5])

    def live_toggle(self):
        e = [e for e in CAT["sound"] if e["key"] == "type"][0]   # SAMPLE / LIVE
        v = self.sget("sound", e)
        if v is None:
            self.flash("not mapped yet")
            return None
        self.edit = None
        return ("live", self.sound, 1 - v)

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
        if not self.touch_recent() or self.overlay or self.view == "SETTINGS" and self.dived:
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
        if self.view == "WAVE" and not self.overlay and not self.touch_active():
            self.v_wave()
        else:
            self.bg_key = None
            self.fb.fill(0)
            if self.overlay == "FILE":
                self.v_file()
            elif self.overlay == "REC":
                self.v_rec()
            elif self.overlay == "SETUP":
                self.v_setup()
            elif self.touch_active():
                self.v_touch()
            elif self.view == "PARAM":
                self.v_param()
            elif self.view == "MOD":
                self.v_mod()
            elif self.quant and self.snd():
                self.v_quant()
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
            self.box(self.flash_msg, self.flash_label)
        elif not (snap and snap.get("connected")):
            self.box(self.link_msg())

    def link_msg(self):
        """No module to show: no link, or its firmware being checked / not the one we know."""
        fw = self.snap and self.snap.get("fw")
        return "CHECKING FIRMWARE" if fw == "checking" else "UNKNOWN FIRMWARE" \
            if fw == "unknown" else "NO MODULE LINK"

    def animating(self):
        """WAVE with dots alive or being launched (else frames wouldn't change)."""
        s, snap = self.snd(), self.snap
        return (self.view == "WAVE" and not self.overlay and self.bg_key is not None
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
        kept = (self.touch, self.tb, self.dived, self.set_cur, self.overlay, self.setup, self.edit,
                self.sel_plays, self.touch_on, self.folder, self.files, self.file_cur,
                self.files_ok, self.root_counts, self.menu, self.flash_msg, self.flash_label,
                self.flash_until, self.wifi_on, self.net, self.rec_cur, self.rec_armed,
                self.rec_phase, self.quant)
        gv = snap.get("_gv") or {}            # GRAINVIEW's own settings: the defaults unless given
        self.sel_plays, self.touch_on = bool(gv.get("selPlays")), gv.get("touchOn", 1) != 0
        self.wifi_on, self.net = gv.get("wifi", 1) != 0, gv.get("net")
        su = snap.get("_setup")
        self.overlay, self.setup = ("SETUP", list(su)) if su else (None, [None, 0, 0])
        self.edit = None
        if su and su[0] is not None and "_edit" in snap:
            grp = SETUP_GROUPS[su[0]][1]
            self.edit = [grp, self.items(grp)[su[2]], snap["_edit"], None]
        elif snap.get("_dived") and "_edit" in snap:   # SETTINGS: the cursor row being edited
            self.edit = ["sound", CAT["sound"][snap.get("_setCur", 0)], snap["_edit"], None]
        qq = snap.get("_quant")               # SETTINGS > Quantizer: [cursor, edit or None]
        self.quant = {"cur": qq[0], "edit": qq[1]} if qq else None
        live = {k: v for k, v in snap.items() if k != "_steps"}
        fl, self.menu, self.flash_msg = snap.get("_file"), None, None
        if fl:
            self.overlay, self.folder, self.snap = "FILE", fl["folder"], live
            self.files = (list(FOLDERS) if self.folder == "ROOT" else list(range(SLOTS))
                          if self.is_store() else fl.get("files") or [])
            self.file_cur, self.files_ok = fl.get("cur", 0), fl.get("ok", True) is not False
            self.root_counts = dict(fl.get("counts") or {})
            if fl.get("menu"):
                self.open_menu()
                self.menu[2], self.menu[3] = fl["menu"]
        if snap.get("_rec"):                  # RECORD open: [row, armed row or None]
            self.overlay, self.snap = "REC", live
            self.rec_phase = live.get("rec") and live["rec"]["phase"]
            self.rec_cur, self.rec_armed = snap["_rec"]
        if snap.get("_flash"):
            self.flash(*snap["_flash"])
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
        try:
            for t in snap["_steps"]:
                self.clock = lambda: t
                self.render(live)
        finally:
            self.clock, self.rand, self.testing = clock, rand, False
            (self.touch, self.tb, self.dived, self.set_cur, self.overlay, self.setup, self.edit,
             self.sel_plays, self.touch_on, self.folder, self.files, self.file_cur,
             self.files_ok, self.root_counts, self.menu, self.flash_msg, self.flash_label,
             self.flash_until, self.wifi_on, self.net, self.rec_cur, self.rec_armed,
             self.rec_phase, self.quant) = kept
            self.g_list, self.g_acc, self.g_t, self.g_key, self.g_ph = [], 0, None, None, 0
            self.bg_key = None

    def flash(self, msg, label=None):
        self.flash_msg, self.flash_label = msg, label
        self.flash_until = time.ticks_add(time.ticks_ms(), FLASH_MS)

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
        su = self.setup
        if self.quant and not self.overlay and self.view == "SETTINGS" and self.snd():
            self.q_enc(n)
        elif self.edit:
            self.edit_step(n)
        elif self.overlay == "SETUP" and su[0] is None:
            su[1] = max(0, min(len(SETUP_GROUPS) - 1, su[1] + n))
        elif self.overlay == "SETUP":
            su[2] = max(0, min(len(self.items(SETUP_GROUPS[su[0]][1])) - 1, su[2] + n))
        elif self.overlay == "FILE" and self.menu:
            m = self.menu
            m[2], m[3] = max(0, min(len(m[1]) - 1, m[2] + n)), None
        elif self.overlay == "REC":
            self.rec_cur = max(0, min(len(self.rec_items()) - 1, self.rec_cur + n))
            self.rec_armed = None
        elif self.overlay == "FILE":
            lo = self.file_lo()
            self.file_cur = max(lo, min(max(lo, len(self.files) - 1), self.file_cur + n))
        elif self.view == "SETTINGS" and self.dived:
            self.set_cur = max(0, min(len(CAT["sound"]) - 1, self.set_cur + n))
        else:                                 # page the views (clamped, as the emulator)
            i = VIEWS.index(self.view) + n
            self.view = VIEWS[max(0, min(len(VIEWS) - 1, i))]

    def push(self):
        su = self.setup
        if self.quant and not self.overlay and self.view == "SETTINGS" and self.snd():
            return self.q_push()
        elif self.edit:
            return self.edit_commit()
        elif self.overlay == "SETUP" and su[0] is None:
            if SETUP_GROUPS[su[1]][1]:
                su[0], su[2] = su[1], 0
            else:
                self.flash("coming soon")
        elif self.overlay == "SETUP":
            g = SETUP_GROUPS[su[0]][1]
            self.edit_start(g, self.items(g)[su[2]])
        elif self.overlay == "FILE" and self.menu:
            return self.menu_push()
        elif self.overlay == "REC":
            return self.rec_push()
        elif self.overlay == "FILE" and self.file_cur == self.file_lo() and self.folder != "ROOT":
            return self.open_root(self.folder)
        elif self.overlay == "FILE" and self.file_cur < 0:
            self.open_rec()
        elif self.overlay == "FILE" and self.folder == "ROOT":
            return self.open_files(self.files[self.file_cur])
        elif self.overlay == "FILE" and self.is_store():
            self.open_menu()
        elif self.overlay == "FILE":
            if self.file_cur < len(self.files):
                return ("load", self.folder, self.file_cur, self.files[self.file_cur])
        elif self.view == "SETTINGS":
            if not self.dived:
                self.dived = True
            else:
                self.edit_start("sound", CAT["sound"][self.set_cur])
        else:
            self.flash("-" if self.view == "WAVE" else "view-only")
        return None

    def btn(self, name):
        if name == "PUSH":
            return self.push()
        if name not in ("BACK", "A/B"):       # leaving = cancel an edit
            self.edit = None
            if self.quant:
                self.quant["edit"] = None
        if name in ("VIEW", "FILE", "SETUP"):  # ...and the keyboard page
            self.quant = None
        if name == "LIVE":                    # SOUND< + SOUND> together: toggle Live
            return self.live_toggle()
        if name == "BACK":
            if self.edit:
                self.edit = None
            elif self.menu:
                self.menu = None
            elif self.quant and not self.overlay:
                if self.quant["edit"]:
                    self.quant["edit"] = None
                else:
                    self.quant = None
            elif self.overlay == "REC":       # (its list again: new takes)
                return self.open_files("Recs")
            elif self.overlay == "FILE" and self.folder != "ROOT":
                return self.open_root(self.folder)
            elif self.overlay == "SETUP" and self.setup[0] is not None:
                self.setup[0] = None
            elif self.overlay:
                self.overlay = None
            elif self.dived:
                self.dived = False
            else:
                self.view = "WAVE"
        elif name == "VIEW":
            self.overlay, self.menu, self.dived = None, None, False
            self.view = VIEWS[(VIEWS.index(self.view) + 1) % len(VIEWS)]
        elif name in ("SOUND<", "SOUND>"):
            n = (self.sound + (7 if name == "SOUND<" else 1)) % 8
            self.sound = n
            return ("select", n, self.sel_plays)
        elif name == "SETUP":                 # SETUP again = close
            if self.overlay == "SETUP":
                self.overlay = None
            else:
                self.overlay, self.menu, self.setup = "SETUP", None, [None, 0, 0]
        elif name == "FILE":                  # opens on the sound's folder; again = the next
            if self.overlay != "FILE":
                return self.open_files()
            i = FOLDERS.index(self.folder) if self.folder in FOLDERS else -1
            return self.open_files(FOLDERS[(i + 1) % len(FOLDERS)])
        elif name == "A/B":                   # the module's edited scene, as its A/B button
            self.scene = "B" if self.scene == "A" else "A"
            return ("scene", self.scene)
        return None
