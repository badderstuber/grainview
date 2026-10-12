// gv_draw.js - GRAINVIEW drawing core, shared by the emulator and font_compare.
// A 128x128 4-bit greyscale framebuffer (as the SSD1327 holds) + bitmap text
// from GV_FONTS (fonts/gv_fonts.js) + a pixel-exact display. Everything is
// drawn in whole OLED pixels, so this ports 1:1 to the Pico (LVGL / raw fb).

const W = 128, H = 128;

// ---------- font sets (SET > Font) ----------
// T = tiny (labels, status line), M = medium (must-read), L = large (values),
// X = hero (one value, read across the room; null = L pixel-doubled)
const FONT_SETS = {
  Spleen:  {T: 'spleen-5x8', M: 'spleen-6x12', L: 'spleen-8x16', X: 'spleen-16x32'},
  Classic: {T: 'tom-thumb',  M: '6x12',        L: 't0-16b-uni', X: null},
};
const fm = {                      // font metrics
  asc: f => GV_FONTS[f].ascent, desc: f => GV_FONTS[f].descent,
  lh: f => GV_FONTS[f].ascent + GV_FONTS[f].descent, cap: f => GV_FONTS[f].cap,
};

// ---------- framebuffer ----------
function fb(w = W, h = H) { return {w, h, p: new Uint8Array(w * h)}; }
function px(b, x, y, v) { if (x >= 0 && y >= 0 && x < b.w && y < b.h) b.p[y * b.w + x] = v; }
function rect(b, x, y, w, h, v) { for (let j = y; j < y + h; j++) for (let i = x; i < x + w; i++) px(b, i, j, v); }
function frame(b, x, y, w, h, v) { rect(b, x, y, w, 1, v); rect(b, x, y + h - 1, w, 1, v); rect(b, x, y, 1, h, v); rect(b, x + w - 1, y, 1, h, v); }
function hline(b, x0, x1, y, v) { rect(b, x0, y, x1 - x0 + 1, 1, v); }
function dots(b, x0, x1, y, v) { for (let x = x0; x <= x1; x += 2) px(b, x, y, v); }   // Metropolix-style leader

// ---------- bitmap text (baseline at y) ----------
function glyph(f, ch) { const g = GV_FONTS[f].g; return g[ch.codePointAt(0)] || g[63]; }   // '?' fallback
const ELL = '…';                                     // drawn as 3 pixels if the font lacks it
const ellW = f => hasGlyph(f, ELL) ? glyph(f, ELL)[0] : 6;
function hasGlyph(f, ch) { return !!GV_FONTS[f].g[ch.codePointAt(0)]; }
function textW(f, s) { let w = 0; for (const ch of s) w += ch === ELL ? ellW(f) : glyph(f, ch)[0]; return w; }
function text(b, f, s, x, y, v = 15) {
  let cx = x;
  for (const ch of s) {
    if (ch === ELL && !hasGlyph(f, ch)) { for (let i = 0; i < 3; i++) px(b, cx + i * 2, y, v); cx += 6; continue; }
    const [dw, w, h, xo, yo, hex] = glyph(f, ch), rl = Math.ceil(w / 8) * 2, nb = rl * 4;
    for (let r = 0; r < h; r++) {
      const bits = parseInt(hex.substr(r * rl, rl) || '0', 16);
      for (let c = 0; c < w; c++) if (bits & (1 << (nb - 1 - c))) px(b, cx + xo + c, y - yo - h + r + 1, v);
    }
    cx += dw;
  }
  return cx - x;
}
function textR(b, f, s, xr, y, v) { return text(b, f, s, xr - textW(f, s), y, v); }
// text drawn at k x k pixels (hero fallback when a set has no X font)
function textBig(b, f, s, x, y, k, v = 15) {
  const t = fb(textW(f, s), fm.lh(f)); text(t, f, s, 0, fm.asc(f), 1);
  for (let j = 0; j < t.h; j++) for (let i = 0; i < t.w; i++) if (t.p[j * t.w + i]) rect(b, x + i * k, y - fm.asc(f) * k + j * k, k, k, v);
  return t.w * k;
}
// shorten s to fit maxW px, ending in an ellipsis
function fit(f, s, maxW) {
  if (textW(f, s) <= maxW) return s;
  while (s.length && textW(f, s + ELL) > maxW) s = s.slice(0, -1);
  return s + ELL;
}

// ---------- display: zoom or calibrated actual size ----------
// ACTUAL = the SSD1327's 26.7 mm active area at real size. Browsers assume
// 96 CSS px/inch, real screens differ, so a ruler calibrates px/mm (saved;
// shared by every page served from the same origin).
const OLED_MM = 26.7, RULER_MM = 50, ZOOM = 3.5;
const sz = {actual: localStorage.gvActual === '1', pxPerMm: +localStorage.gvPxPerMm || 96 / 25.4};
function sizeSave() { localStorage.gvActual = sz.actual ? '1' : '0'; localStorage.gvPxPerMm = sz.pxPerMm; }
// Each lit OLED pixel = one square. ZOOM snaps to whole device pixels (crisp);
// ACTUAL uses the exact calibrated size. Skips the redraw if nothing changed.
function show(cv, b) {
  const dpr = devicePixelRatio;
  const d = sz.actual ? OLED_MM * sz.pxPerMm / W * dpr : Math.round(ZOOM * dpr);
  const key = d + '/' + b.w + 'x' + b.h;
  if (cv._key === key && cv._last && cv._last.every((v, i) => v === b.p[i])) return;
  cv._key = key; cv._last = b.p.slice();
  cv.style.width = b.w * d / dpr + 'px'; cv.style.height = b.h * d / dpr + 'px';
  cv.width = Math.round(b.w * d); cv.height = Math.round(b.h * d);
  const c = cv.getContext('2d'), gap = !sz.actual && d >= 5 ? d * 0.1 : 0;   // real pixels nearly touch
  c.fillStyle = '#000'; c.fillRect(0, 0, cv.width, cv.height);
  for (let y = 0; y < b.h; y++) for (let x = 0; x < b.w; x++) {
    const v = b.p[y * b.w + x]; if (!v) continue;
    const q = v / 15 * 255; c.fillStyle = `rgb(${q * 0.92 | 0},${q * 0.98 | 0},${q | 0})`;
    c.fillRect(x * d, y * d, d - gap, d - gap);
  }
}
