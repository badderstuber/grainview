# Multigrain knob values -> real units: tools/gv_units.js ported for the Pico UI (same
# formulas, from the 1.4.8.0 firmware; see the JS file for the RE notes). Input = the
# stored scene value (0..1, SCAN/TONE -1..1). ctx: link_rs, link_sp, sync, size, pitch.
import math

FS = 48076                                    # engine sample rate (Hz)
SHAPES = ("BELL", "SINC", "TRI", "DECAY", "RAMP", "TUKEY", "SQUARE")
SYNC_MULT = (0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8, 16)
SYNC_TXT = ("/16", "/8", "/4", "/2", "x1", "x2", "x4", "x8", "x16")


def jround(x):                                # JS Math.round (halves go up)
    return math.floor(x + 0.5)


def clamp01(v):
    return min(1, max(0, v))


def rate_hz(v):
    x = v * v
    return 0.25 if x < 0.001911125 else min(x, 1) * 130.813


def size_ms(v):
    s = clamp01(v)
    return math.floor(960 + s * s * (192000 - 960)) / FS * 1000


def pitch_st(v):
    return v * 48 - 24


def grain_ms(size, pitch, link_sp):
    return size_ms(size) / (2 ** (pitch_st(pitch) / 12) if link_sp else 1)


def rate_linked_hz(rate, gms):               # RATE-SIZE link: overlap / grain length
    hz = (1 + 7 * clamp01(rate)) / (gms / 1000)
    while hz > 130.813:
        hz /= 2
    return hz


def sync_idx(v):
    return 0 if v < 0 else 8 if v >= 1 else min(math.floor(v * 9), 8)


def shape_idx(v):
    return 0 if v < 0.03 else 6 if v > 0.97 else 1 + int(5 * (v - 0.03) / 0.94)


def tone(t):
    if abs(t) < 0.005:
        return "FLAT", 0
    c = 0.6 * t * t if t > 0 else (1 - 0.8 * abs(t)) ** 2
    return ("HP" if t > 0 else "LP"), -FS * math.log(max(1 - c, 1e-9)) / (2 * math.pi)


def fixed(v, dp):                             # JS toFixed
    return ("%." + str(dp) + "f") % v


def fmt_hz(hz):
    if hz >= 1000:
        return fixed(hz / 1000, 0 if hz >= 9950 else 1) + "k"
    return fixed(hz, 0 if hz >= 99.5 else 1 if hz >= 9.95 else 2)


def fmt_pct(v, bip):
    p = jround(v * 100)
    return ("+" if bip and p > 0 else "") + str(p) + "%"


def unit_text(k, v, ctx=None):
    if v is None or v != v:
        return "-"
    ctx = ctx or {}
    if k == "RATE":
        if ctx.get("sync"):
            return "SYN" + SYNC_TXT[sync_idx(v)]
        if ctx.get("link_rs"):
            return "x" + fixed(1 + 7 * clamp01(v), 1)
        return fmt_hz(rate_hz(v)) + "Hz"
    if k == "SIZE":
        ms = (grain_ms(ctx.get("size", 0.5), ctx.get("pitch", 0.5), True) if ctx.get("link_sp")
              else size_ms(v))
        return fixed(ms / 1000, 2) + "s" if ms >= 1000 else fixed(ms, 0) + "ms"
    if k == "PITCH":
        r = jround(pitch_st(v) * 10) / 10
        return ("+" if r > 0 else "") + fixed(r, 0 if abs(r) >= 10 else 1) + "st"
    if k == "SHAPE":
        return SHAPES[shape_idx(v)]
    if k == "TONE":
        typ, hz = tone(v)
        if typ == "FLAT":
            return "FLAT"
        return typ + " " + (str(jround(hz / 1000)) + "k" if hz >= 999.5 else str(jround(hz)))
    if k == "SCAN":
        return fmt_pct(v, True)
    return fmt_pct(v, False)                  # START WRAP LEVEL BLUR MORPH
