# GRAINVIEW drawing core on the Pico: tools/gv_draw.js ported onto MicroPython's framebuf
# (128x128 GS4, as the SSD1327 holds), so the panel draws what the emulator draws, pixel
# for pixel. Fonts: gv_fonts.py (generated from the emulator's fonts/gv_fonts.js).
#
#   d = Draw(framebuf.FrameBuffer(buf, 128, 128, framebuf.GS4_HMSB))
#   T, M = FONT("T"), FONT("M")       # the Spleen set: T tiny, M medium, L large, X hero
#   d.text(M, "S1", 1, base, 15)      # baseline at y, returns the width
import framebuf

from gv_fonts import FONTS

W = H = 128
SET = {"T": "spleen-5x8", "M": "spleen-6x12", "L": "spleen-8x16", "X": "spleen-16x32"}
ELL = "…"                                # drawn as 3 pixels if the font lacks it


class Font:
    def __init__(self, name):
        self.asc, self.desc, self.cap, self.g = FONTS[name]
        self.lh = self.asc + self.desc
        self.fbs = {}                         # code -> glyph FrameBuffer (made on first use)

    def glyph(self, c):
        return self.g.get(c) or self.g[63]    # '?' fallback

    def gfb(self, c):
        f = self.fbs.get(c)
        if f is None:
            g = self.glyph(c)
            f = self.fbs[c] = framebuf.FrameBuffer(bytearray(g[5]), g[1], g[2], framebuf.MONO_HLSB)
        return f

    def ellw(self):
        return self.glyph(0x2026)[0] if 0x2026 in self.g else 6

    def width(self, s):
        w = 0
        for ch in s:
            w += self.ellw() if ch == ELL else self.glyph(ord(ch))[0]
        return w


_fonts = {}


def FONT(role):
    f = _fonts.get(role)
    if f is None:
        f = _fonts[role] = Font(SET[role])
    return f


class Draw:
    def __init__(self, fb):
        self.fb = fb
        self.pal = framebuf.FrameBuffer(bytearray(1), 2, 1, framebuf.GS4_HMSB)

    def px(self, x, y, v):
        self.fb.pixel(x, y, v)                # framebuf clips

    def rect(self, x, y, w, h, v):
        if w > 0 and h > 0:
            self.fb.fill_rect(x, y, w, h, v)

    def frame(self, x, y, w, h, v):
        if w > 0 and h > 0:
            self.fb.rect(x, y, w, h, v)

    def hline(self, x0, x1, y, v):
        self.rect(x0, y, x1 - x0 + 1, 1, v)

    def dots(self, x0, x1, y, v):             # Metropolix-style leader
        for x in range(x0, x1 + 1, 2):
            self.fb.pixel(x, y, v)

    def text(self, f, s, x, y, v=15):
        """s with its baseline at y; returns the width drawn."""
        key = (v + 1) & 15                    # glyph background -> a colour blit skips
        self.pal.pixel(0, 0, key)
        self.pal.pixel(1, 0, v)
        cx = x
        for ch in s:
            c = ord(ch)
            if ch == ELL and c not in f.g:
                for i in range(3):
                    self.fb.pixel(cx + i * 2, y, v)
                cx += 6
                continue
            dw, w, h, xo, yo, _ = f.glyph(c)
            if w and h:
                self.fb.blit(f.gfb(c), cx + xo, y - yo - h + 1, key, self.pal)
            cx += dw
        return cx - x

    def text_r(self, f, s, xr, y, v=15):
        return self.text(f, s, xr - f.width(s), y, v)


def fit(f, s, max_w):
    """s shortened to fit max_w px, ending in an ellipsis."""
    if f.width(s) <= max_w:
        return s
    # = the emulator's "drop the last char until s + ELL fits", in one pass (that re-measured
    # the whole name per char: ~1000 glyph lookups a row for a 45-char file name, every redraw)
    room, w = max_w - f.ellw(), 0
    for i, ch in enumerate(s):
        w += f.ellw() if ch == ELL else f.glyph(ord(ch))[0]
        if w > room:
            return s[:i] + ELL
    return s + ELL
