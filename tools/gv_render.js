// gv_render.js - render one emulator frame headless (Node), for checking the Pico UI
// (pico/gv_ui.py) against the spec pixel for pixel. Runs the emulator's own script with
// the browser bits stubbed out, sets the snapshot, draws one view.
//
//   node tools/gv_render.js SNAP.json VIEW > frame.bin    (8192 bytes, left px = high nibble)
// Used by: tools/venv/bin/python tools/gv_pico.py ui VIEW
const fs = require('fs'), path = require('path'), vm = require('vm');
const [snapPath, view] = process.argv.slice(2);
const dir = __dirname;

const el = () => ({style: {}, textContent: '', children: [], hidden: false, width: 0, height: 0,
  addEventListener() {}, append() {}, classList: {add() {}},
  getContext: () => ({fillRect() {}, set fillStyle(v) {}})});
const ctx = vm.createContext({
  document: {getElementById: el, addEventListener() {}, body: el(), createElement: el, activeElement: null},
  localStorage: {}, location: {search: ''}, devicePixelRatio: 1, performance: {now: () => 0},
  fetch: () => new Promise(() => {}), setTimeout() {}, setInterval() {},
  EventSource: class { constructor() {} }, URLSearchParams, console,
});
for (const f of ['fonts/gv_fonts.js', 'gv_draw.js', 'gv_units.js'])
  vm.runInContext(fs.readFileSync(path.join(dir, f), 'utf8'), ctx, {filename: f});
const html = fs.readFileSync(path.join(dir, 'grainview_emulator.html'), 'utf8');
const script = html.slice(html.lastIndexOf('<script>') + 8, html.lastIndexOf('</script>'));
vm.runInContext(script + `
;globalThis.__gv = {set M(v) { M_ = v; }, st, fb, box, views: {WAVE: vWave, PARAM: vParm, MOD: vMod}};`,
  ctx, {filename: 'grainview_emulator.html'});

const G = ctx.__gv, snap = JSON.parse(fs.readFileSync(snapPath, 'utf8'));
G.M = snap;
if (snap.connected) { G.st.sound = snap.selected; G.st.scene = snap.edit_scene || 'A'; }
else if (snap._sound != null) G.st.sound = snap._sound;    // test: the last sound polled
G.st.view = view;
const b = G.fb();
if (!G.views[view]) throw new Error('view not ported: ' + view);
G.views[view](b);
if (!snap.connected) G.box(b, 'NO MODULE LINK');
const out = Buffer.alloc(b.p.length / 2);
for (let j = 0; j < out.length; j++) out[j] = (b.p[2 * j] << 4) | b.p[2 * j + 1];
process.stdout.write(out);
