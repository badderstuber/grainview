// gv_units.js - Multigrain knob values -> real units, for GRAINVIEW.
// Formulas from the 1.4.8.0 firmware (grain engine FUN_08016278, offline RE
// 2026-10-12); ranges agree with the manual. Input = the knob value as stored
// in the scene (0..1, SCAN/TONE -1..1), i.e. before CV/mod.
// Context flags (ctx, from /state; addresses hardware-confirmed 2026-10-12):
//   linkRS  RATE-SIZE link  -> RATE = overlap (1..8 grains) / grain length
//   linkSP  SIZE-PITCH link -> grain length divided by the pitch ratio
//   sync    RATE locked to the SYNC clock -> RATE = clock division x1/16..x16
// Not handled: SIZE max-length modes beyond 4 s (mode byte 2/3: 8 s / buffer).

const GV_FS = 48076;                                  // engine sample rate (Hz)
const SHAPES = ['BELL', 'SINC', 'TRI', 'DECAY', 'RAMP', 'TUKEY', 'SQUARE'];   // order: manual
const SYNC_MULT = [0.0625, 0.125, 0.25, 0.5, 1, 2, 4, 8, 16];                // flash 0x0805c738
const SYNC_TXT = ['/16', '/8', '/4', '/2', 'x1', 'x2', 'x4', 'x8', 'x16'];

const clamp01 = v => Math.min(1, Math.max(0, v));
const units = {
  // RATE (free-running): (v^2) * 130.813 Hz, floor 0.25 Hz      [0x080173ec]
  rateHz: v => { const x = v * v; return x < 0.001911125 ? 0.25 : Math.min(x, 1) * 130.813; },
  // SIZE: 960 + v^2 * (192000 - 960) samples                    [0x08016350]
  sizeMs: v => { const s = clamp01(v); return Math.floor(960 + s * s * (192000 - 960)) / GV_FS * 1000; },
  // grain length heard (SIZE-PITCH link divides by the pitch ratio)
  grainMs: (size, pitch, linkSP) => units.sizeMs(size) / (linkSP ? Math.pow(2, units.pitchSt(pitch) / 12) : 1),
  // RATE with RATE-SIZE link: overlap 1..8 grains / grain length, folded <= 130.813  [0x080172d0]
  rateLinkedHz: (rate, grainMs) => { let hz = (1 + 7 * clamp01(rate)) / (grainMs / 1000); while (hz > 130.813) hz /= 2; return hz; },
  // RATE synced: division table index floor(v*9)                 [0x080174e2]
  syncIdx: v => v < 0 ? 0 : v >= 1 ? 8 : Math.min(Math.floor(v * 9), 8),
  // PITCH: v*48 - 24 semitones, 0.5 = no transposition          [0x0801636e]
  pitchSt: v => v * 48 - 24,
  // SHAPE: 7 windows, thresholds 0.03 / 0.97                     [0x0804dcd0]
  shapeIdx: v => v < 0.03 ? 0 : v > 0.97 ? 6 : 1 + Math.trunc(5 * (v - 0.03) / 0.94),
  // TONE: + = high-pass, - = low-pass, two cascaded one-poles; ~cutoff  [0x08017d28]
  tone: t => {
    if (Math.abs(t) < 0.005) return {type: 'FLAT', hz: 0};
    const c = t > 0 ? 0.6 * t * t : (1 - 0.8 * Math.abs(t)) ** 2;
    return {type: t > 0 ? 'HP' : 'LP', hz: -GV_FS * Math.log(Math.max(1 - c, 1e-9)) / (2 * Math.PI)};
  },
};

// short display strings (fit a 7-char PARM cell)
function fmtHz(hz) { return hz >= 1000 ? (hz / 1000).toFixed(hz >= 9950 ? 0 : 1) + 'k' : hz >= 99.5 ? hz.toFixed(0) : hz >= 9.95 ? hz.toFixed(1) : hz.toFixed(2); }
function fmtPct(v, bip) { const p = Math.round(v * 100); return (bip && p > 0 ? '+' : '') + p + '%'; }
// ctx (optional): {linkRS, linkSP, sync, size, pitch} - size/pitch = same scene's knob values
function unitText(k, v, ctx = {}) {
  if (v == null || isNaN(v)) return '-';
  const gms = () => units.grainMs(ctx.size ?? 0.5, ctx.pitch ?? 0.5, ctx.linkSP);
  switch (k) {
    case 'RATE':  if (ctx.sync) return 'SYN' + SYNC_TXT[units.syncIdx(v)];
                  return fmtHz(ctx.linkRS ? units.rateLinkedHz(v, gms()) : units.rateHz(v)) + 'Hz';
    case 'SIZE':  { const ms = ctx.linkSP ? gms() : units.sizeMs(v); return ms >= 1000 ? (ms / 1000).toFixed(2) + 's' : ms.toFixed(0) + 'ms'; }
    case 'PITCH': { const st = units.pitchSt(v), r = Math.round(st * 10) / 10; return (r > 0 ? '+' : '') + r.toFixed(Math.abs(r) >= 10 ? 0 : 1) + 'st'; }
    case 'SHAPE': return SHAPES[units.shapeIdx(v)];
    case 'TONE':  { const t = units.tone(v); return t.type === 'FLAT' ? 'FLAT' : t.type + ' ' + fmtHz(t.hz); }
    case 'SCAN':  return fmtPct(v, true);
    default:      return fmtPct(v, false);   // START WRAP LEVEL BLUR MORPH
  }
}
