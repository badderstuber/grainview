// gv_render.js - render one emulator frame headless (Node), for checking the Pico UI
// (pico/gv_ui.py) against the spec pixel for pixel. Runs the emulator's own script with
// the browser bits stubbed out, sets the snapshot, draws one view.
//
//   node tools/gv_render.js SNAP.json VIEW > frame.bin    (8192 bytes, left px = high nibble)
// A snapshot with "_steps" (clock values, ms) + "_rand" (random numbers) renders once per
// step with those (grain dots), the last frame is the output - as pico/gv_ui.py does.
// "_touch": [knob, mod source or null], "_dived", "_setCur": that UI state for the test;
// "_setup": [group or null, group cursor, row] opens SETUP (view "SETUP": the groups), "_edit":
// the cursor row's value being edited, "_gv": {selPlays, touchOn} (else the defaults);
// "_prev": earlier snapshots fed through detectTouch first (as the poll does).
// "_file": {folder ("ROOT" | a folder), files (a WAV folder's names), cur, ok, counts,
// menu: [cur, armed]} opens FILE there (view "FILE" alone: the root); "_flash": [msg, label].
// Used by: tools/venv/bin/python tools/gv_pico.py ui VIEW
const fs = require('fs'), path = require('path'), vm = require('vm');
const [snapPath, view] = process.argv.slice(2);
const dir = __dirname;
let clock = 0;

const el = () => ({style: {}, textContent: '', children: [], hidden: false, width: 0, height: 0,
  addEventListener() {}, append() {}, classList: {add() {}},
  getContext: () => ({fillRect() {}, set fillStyle(v) {}})});
const ctx = vm.createContext({
  document: {getElementById: el, addEventListener() {}, body: el(), createElement: el, activeElement: null},
  localStorage: {}, location: {search: ''}, devicePixelRatio: 1, performance: {now: () => clock},
  fetch: () => new Promise(() => {}), setTimeout() {}, setInterval() {},
  EventSource: class { constructor() {} }, URLSearchParams, console,
});
for (const f of ['fonts/gv_fonts.js', 'gv_draw.js', 'gv_units.js'])
  vm.runInContext(fs.readFileSync(path.join(dir, f), 'utf8'), ctx, {filename: f});
const html = fs.readFileSync(path.join(dir, 'grainview_emulator.html'), 'utf8');
const script = html.slice(html.lastIndexOf('<script>') + 8, html.lastIndexOf('</script>'));
vm.runInContext(script + `
;globalThis.__gv = {set M(v) { M_ = v; }, set CAT(v) { CAT = v; }, st, fb, box, touchActive, vTouch, detectTouch, vSetup,
  SETUP_GROUPS, gItems, vFile, openMenu, isStore, FOLDERS,
  views: {WAVE: vWave, PARAM: vParm, MOD: vMod, SETTINGS: vSet}};`,
  ctx, {filename: 'grainview_emulator.html'});

const G = ctx.__gv, snap = JSON.parse(fs.readFileSync(snapPath, 'utf8'));
G.M = snap;
if (snap.connected) { G.st.sound = snap.selected; G.st.scene = snap.edit_scene || 'A'; }
else if (snap._sound != null) G.st.sound = snap._sound;    // test: the last sound polled
const setup = snap._setup || (view === 'SETUP' ? [null, 0, 0] : null);
const file = snap._file || (view === 'FILE' ? {folder: 'ROOT', cur: 0} : null);
G.st.view = setup || file ? 'WAVE' : view;
if (setup) {
  G.st.overlay = 'SETUP'; G.st.setup = {g: setup[0], gc: setup[1], cur: setup[2]};
}
const gv = snap._gv || {};
G.st.selPlays = !!gv.selPlays; G.st.touchOn = gv.touchOn !== 0;
G.CAT = JSON.parse(fs.readFileSync(path.join(dir, 'gv_settings.json'), 'utf8'));
if (snap._touch) G.st.touch = {k: snap._touch[0], src: snap._touch[1], t: Date.now()};
G.st.dived = !!snap._dived; G.st.setCur = snap._setCur || 0;
if (setup && setup[0] != null && '_edit' in snap) {
  const g = G.SETUP_GROUPS[setup[0]][1], e = G.gItems(g)[setup[2]];
  G.st.edit = {g, e, v: snap._edit, v0: null};
}
for (const p of snap._prev ? [...snap._prev, snap] : []) {
  G.M = p; G.st.sound = p.selected; G.st.scene = p.edit_scene || 'A'; G.detectTouch();
}
G.M = snap;
if (file) {
  const f = file.folder;
  G.st.overlay = 'FILE'; G.st.folder = f; G.st.menu = null;
  G.st.files = f === 'ROOT' ? G.FOLDERS.slice() : G.isStore(f) ? Array.from({length: 48}, (_, i) => i)
    : file.files || [];
  G.st.fileCur = file.cur == null ? 0 : file.cur; G.st.filesOk = file.ok !== false;
  G.st.rootCounts = file.counts || {};
  if (file.menu) { G.openMenu(); G.st.menu.cur = file.menu[0]; G.st.menu.armed = file.menu[1]; }
}
if (!setup && !file && !G.views[view]) throw new Error('view not ported: ' + view);
const rand = (snap._rand || []).slice();
vm.runInContext('Math.random = () => __next()', Object.assign(ctx, {__next: () => rand.shift()}));
let b;
for (const t of snap._steps || [0]) {          // as the emulator's render(): hero or view
  clock = t; b = G.fb(); (file ? G.vFile : setup ? G.vSetup : G.touchActive() ? G.vTouch : G.views[view])(b);
}
if (snap._flash) G.box(b, snap._flash[0], snap._flash[1]);
else if (!snap.connected) G.box(b, 'NO MODULE LINK');
const out = Buffer.alloc(b.p.length / 2);
for (let j = 0; j < out.length; j++) out[j] = (b.p[2 * j] << 4) | b.p[2 * j + 1];
process.stdout.write(out);
