# Multigrain companion app — roadmap & tasks

_Last updated: 2026-10-11._

## Vision

A companion "screen"/controller for the Intellijel Multigrain that mirrors its
state live and lets you drive it (browse SD samples, load files into slots,
tweak + recall patches) — eventually from a **phone or desktop over WiFi**, with
nothing but a tiny hidden board wired to the module inside the rack.

## How it works (proven)

The module has no USB-MIDI/parameter input; its USB-C is firmware-update only.
BUT its **SWD debug port** (the `JTRACE` header) lets us, with nothing modified
on the module and fully reversibly:
- **Read** live RAM in the background without halting → mirror every parameter.
- **Call the firmware's own functions** (briefly halt, set registers, run, catch
  return, restore) → drive actions like dir-scan / load-WAV using the module's
  own code.

## Key architecture decision: how to get rid of the laptop + ST-Link

| Option | Clutter-free? | Module firmware risk | Effort | Verdict |
|---|---|---|---|---|
| ST-Link + laptop (now) | no | none | done | dev setup only |
| **RP2040 / Pico W permanent SWD bridge** | **yes** | **none** | medium | **chosen endgame** |
| Mod module firmware to use its USB-C | yes | high + maintenance treadmill | months | optional stretch only |

The **Pico-W bridge** wins: 4 wires from JTRACE → hidden ~£4 board → WiFi/BT/USB →
phone/desktop app. It does the SWD talking; the module is never modified.

---

## Phases

### Phase 0 — Foundations ✅ DONE
- [x] Confirm USB/MIDI dead-ends; choose SWD path.
- [x] Solder JTRACE 2x5 header; ST-Link chain working; chip = STM32H753.
- [x] Live read mirror (`mg_mirror.py` + `mg_addrs.json`, 11 params mapped).
- [x] Prove we can call firmware functions over SWD (`mg_call.py`, dir-scan OK).
- [x] Ghidra RE: located load-WAV / dir-scan / sound functions + args.

### Phase 1 — Complete the SWD feature set (ST-Link + Mac, dev)
- [x] **Read SD file list** through the module (`mg_sd.py`) — names + indices. *(hardware-tested 2026-10-11: 11 files, indices 0–10)*
- [x] **Load a WAV into the selected sound** — `tools/mg_load.py` via front-panel routine `FUN_0803e710` (hardware-tested 2026-10-11). (`FUN_08012b24` = *load Preset(n+1).mgp*.)
- [x] **Load preset N** — `tools/mg_preset.py N` (`FUN_08012b24(N-1)`), verified on Project01 Preset01/02 (2026-10-11). File must exist.
- [x] **Select sound** (focus, `FUN_08011980`) + **switch playback** (engine event 3) — `mg_load.py --sound N [--play]`, hardware-tested 2026-10-11.
- [x] Map **Scene A / Scene B raw arrays** — sound struct +0x48.. (A), +0x264 (B); `tools/mg_param.py` (2026-10-11).
- [x] **Patch write-back** — plain RAM write to the stored scene value; engine follows, no halt (2026-10-11). Knobs JUMP on touch (no pickup). Persisted by setting the project-changed flag (state+0x11) → module autosaves; survives power-cycle ✅.
- [x] **Mod matrix** (RAND/X/Y/Z → params, per scene) — read + write via `mg_param.py --mod` (2026-10-11).
- [x] **Load a WAV from any folder** (project / Wavs / Recs) — `mg_load.py --folder wavs|recs|project N`
      via the panel's folder-button routine `FUN_0803e91c(ui, F)` (sets the sound's folder
      +0x59c with notify, then loads at cursor[F]). **Hardware-tested 2026-10-12** (Sound 5:
      project → Wavs → project). **Empty-sound path hardware-tested 2026-10-12** (created a
      throwaway Project05 over SWD, loaded /Wavs[3] into empty Sound 1: firmware reset +
      loaded file 0, our 2nd load landed on index 3 ✅). Recs (card had none) still untested.
      Recs names = `Rec%05d.wav` of the
      int list. Firmware bug: a Rec load copies the name to 0x30000000+cursor*0x100, so Rec
      index ≥ 8 overwrites project-list names in RAM (panel does the same) - re-read lists.
- [x] **Presets + projects** — `tools/mg_preset.py` (status / N / `--save` / `--lock` /
      `--project` / `--autosave`), all **hardware-tested 2026-10-12** on Project01/02:
      save `FUN_08011450(n)` (autosave + write; refuses locked), lock toggle `FUN_0801e924(n)`
      (Preset%02d.lck), project switch `FUN_08012c54(n, 1)` (saves outgoing first), autosave
      now = state+0x11 = 1 + tick state+0x0c = 10000 (no halt). 48 slots each. Bitmaps
      u32[2]: preset exists 0x240312e0, locked 0x240312e8, project exists 0x240312f4; current
      preset u8 0x24025b18 (>47 none), project u8 0x24025c74 (UI) / u32 0x20008cc4 (SD).
      Guards: load/lock need the exists-bit (missing preset = blank sounds; missing project
      = new empty one), UI and SD project must match. Not done: delete `FUN_0801e834(n)`,
      Collect (`FUN_0801140c(n)`; firmware bug when n ≠ current leaves SD on project n).
- [ ] Nice-to-haves: trigger record. (slot→file ✅ below)
      ✅ slot→file: `tools/mg_slots.py` **hardware-verified 2026-10-12** (matched the
      file loaded the day before). +0x4f4 "missing" byte **CONFIRMED by offline RE
      2026-10-12**: the project/preset reload (`FUN_08012a3c`) sets it to 1 when a sound has a
      stored filename but the file fails to load (loaded OK → 0, truly empty → 0), so
      non-zero = the referenced WAV is missing. Only the reload path sets it (not interactive
      browse-loads); always 0 here because every file is present. Reactive u8 (setter
      +0x4ec/+0x4f0), persisted in the .mgp (deserialized by `FUN_08022d38`).
- [x] **Unit conversions** (2026-10-12) — `tools/gv_units.js`, from the grain engine
      `FUN_08016278` (fs = **48076 Hz**): RATE = v²·130.813 Hz (min 0.25); SIZE = 960 +
      v²·191040 samples (20 ms–4 s); PITCH = v·48−24 st; SHAPE idx thresholds 0.03/0.97
      (names from manual); TONE ± = HP/LP (≈312 Hz…7 kHz, approx); rest linear %. Mode
      flags **hardware-confirmed**: RATE-SIZE link u8 sound+0x53d, SIZE-PITCH link u8
      sound+0x525, clock period f32 0x24020834 (s, smoothed). Applied: linked RATE =
      (1+7v)/grain length; SP link divides grain length by pitch ratio; sync → x1/16..x16.
      Sync enable u8 0x24025bc1 **hardware-confirmed** (it's a setting that must be
      enabled; patching a clock alone leaves it 0).
      Open: SIZE modes 2/3 (8 s / buffer) not handled; TONE Hz approximate.

### Phase 2 — The app = live GRAINVIEW emulator (decided 2026-10-12)
The big responsive dashboard (`demo_app.html`) is an **old concept — dropped**.
Phase 2 grows `tools/grainview_emulator.html` into the real app: the same
128×128 screen + 6 buttons + encoder, driven by live module data. One UX,
designed once here, then ported to LVGL on the Pico (Phase 3).
- [x] Backend `tools/grainview_server.py` (2026-10-12): serves the emulator at `/` +
      JSON API `GET /state /files`, `POST /select /play /param /mod /load`.
      `--mock` = in-memory fake module (tested end-to-end, headless Chrome).
      Live SWD backend reuses mg_param/mg_load helpers — **written, NOT yet run on hardware**.
- [x] Emulator wired to the API: header (file, ▸ playing), WAVE markers + MORPH, PARM, MOD
      grid, SET ("Sel plays" toggle), FILE list → load. Values normalized for now.
- [x] **Live backend hardware-tested 2026-10-12** ✅ — full state read 120 ms (5 Hz poll);
      module→app sound/scene/knob/MORPH follow; app SOUND‹› + SCENE (panel A/B + knob LEDs
      follow) + FILE→load all work; hero view fires on knobs, no idle jitter seen.
      Fixed on hardware: (1) UI flicker after app writes — server now patches its cached
      snapshot under the poll lock; (2) `ProbeError: Write verification error` (~10% of
      scene writes) — ST-Link read-back races the firmware on flag bytes it also writes;
      `mg_load.write8()` tolerates that for volatile flags, verifies + retries real values.
- [x] **Decided 2026-10-12: no per-param editing in GRAINVIEW.** Knobs on the module
      are faster + playable, and GRAINVIEW shows the value while you turn. App-set
      values would also be lost on knob touch (JUMP takeover). PARM + MOD are views.
      `/param` + `/mod` stay in the API (no UI); `mg_param.py` covers CLI writes.
- [ ] Maybe later (one-press actions, not editing): MOD push on a cell = clear routing
      (exact 0 is fiddly on a bipolar knob); copy scene A→B / sound→sound
      (`FUN_08012edc`), reset scene.
- [x] **Decided 2026-10-12: A/B is synced with the module both ways** (= the panel's
      edited scene, u8 `0x24025b48`; NOT MORPH). Setter found offline: `FUN_080114e4`
      (store + notify + state+0x30 = 0). `POST /scene` does the stores without the
      notify (like select). **Hardware-verified 2026-10-12:** panel A/B + knob LEDs follow.
- [x] Font comparison page `tools/font_compare.html` (2026-10-12): 31 u8g2 BDF candidates
      in 3 tiers (tiny labels / medium must-read / large values), pixel-exact 4-bit
      framebuffer, zoom + calibrated actual size, Metropolix-style sample screens.
      Also served at `/font_compare.html` (shares calibration). Fonts: `tools/fonts/`.
- [ ] ⏸ PARKED 2026-10-12 (Leo deciding, ideally on the real OLED): pick fonts.
      **Fonts will be a SET setting** — 3–4 curated *font sets* (tiny/medium/large
      combos, each verified to fit every screen), not free per-tier picks. Layouts
      must derive positions from font metrics (cap/line height, text width), as
      font_compare.html does. Cheap on the Pico (few KB flash per font).
- [x] Emulator on the bitmap renderer (2026-10-12): shared core `tools/gv_draw.js`
      (4-bit fb, BDF text, pixel ellipsis, crisp zoom/calibrated actual size, redraw
      only on change). **Working font set = Spleen** (5x8 / 6x12 / 8x16); SET > Font
      switches sets (Spleen, Classic) and every view reflows from font metrics.
      Metropolix-style chrome: header `S# ▸ file … [A]`, tiny status line
      `page-dots VIEW ······ hint` (tab strip dropped), two-line flash box.
- [x] **Knob-touched hero view** (2026-10-12): turning a Multigrain knob shows that
      param big (Spleen 16x32 hero tier) for 1.5 s + position bar (bipolar from
      centre) + the other scene's value; status line keeps the view you return to.
      Trigger = stored scene value of selected sound/edited scene moving (knobs write
      these; CV doesn't), or a mod depth. MORPH excluded (often CV). Sound/scene
      switch and bulk changes (≥3 values: preset load) are silent. Suppressed in
      FILE / SET-edit. SET › Knob view ON/OFF. **Hardware-tested 2026-10-12: no jitter** —
      320 polls over 60 s on the selected sound, stored scene values bit-identical (p2p
      0.00000 across all params + mod depths), zero false heroes. Firmware only writes the
      stored values on real knob motion, so TOUCH_EPS (0.004) has huge margin.
- [x] **Settings menu** (2026-10-13, mock): SETTINGS view = focused sound's settings; SETUP
      overlay = MODULE / PRESET / SAMPLE (soon) / GRAINVIEW. Catalogue `tools/gv_settings.json`
      (from the manual), spec `docs/SETTINGS.md`, `POST /setting` (mock only).
      TODO: map each setting's RAM + persistence (Settings.mgs reader / preset trailer) for
      live read + write; SAMPLE group with sampling. (Quantizer keyboard page ✅ same day.)
- [ ] Hardware to buy (list agreed 2026-10-12): Pico 2 WH, SSD1327 (SPI), 2× half breadboards,
      jumpers, EC11 push encoder module, 6 tactile buttons. First use: Pico as a
      **dumb USB screen** mirroring the emulator framebuffer (no UI port needed).
- [ ] Real waveform for WAVE (needs sample data location in RAM, or read the WAV off SD).
- [x] **WAVE = grain animation** (2026-10-13, mock): no values on WAVE, waveform fills the
      box, one dot per simulated grain (RATE/SIZE/PITCH/SHAPE/LEVEL + scan playhead), touched
      knob shows in the status line (**style B, chosen**). `tools/wave_compare.html` compares
      styles. TODO: real `SCAN_STEP`, real sample length (WAV header), REVERSE,
      judge dot size + band on the real OLED, then strip styles A/C/D.
- [ ] **Raw SD file preview (play on the device, not the module)** — audition a WAV while
      browsing, unprocessed, so you pick the right one before loading. **Spike PROVEN on
      hardware 2026-10-12** (`tools/spike_preview.py`): `FUN_0801fb94` reads raw PCM off SD
      over SWD into top-of-SDRAM scratch, reconstructed + played on the Mac, module silent.
      Card WAVs = 16-bit PCM. TO FINISH: read the WAV header for exact format, add
      `GET /preview?folder&index` to the server (→ .wav blob), FILE overlay scroll →
      debounced Web Audio preview. See PROGRESS.md 2026-10-12 (night, later) for the recipe.

### Phase 3 — Dedicated "Screen" eurorack module (clutter-free endgame) ⭐
A standalone RP2040-powered module with its own TFT + encoder/buttons that sits
next to the Multigrain and connects via a 4-wire SWD ribbon to JTRACE. Gives the
Multigrain the screen it lacks, no phone/laptop. (Pico W can ALSO serve the
web app over WiFi as an optional big-screen view.)
- [x] **Breadboard prototype (no PCB):** Pico + SSD1327 + push-encoder (2026-10-13);
      v1.0 module board built + SWD through J3 → JTRACE proven 2026-10-20.
- [x] Port SWD **read** + **function-call** (halt/set-regs/run/catch) to the Pico — done in
      MicroPython (PIO + viper, `pico/swd.py`), not C. The Mac drives it over USB
      (`gv_pico.PicoTarget`, `grainview_server.py --swd pico`); WAV load hardware-tested
      2026-10-20. Still Mac-driven: the logic itself moves onto the Pico with the on-screen UI.
- [ ] Hardcode the mapped addresses + function entry points (firmware-version
      aware — Multigrain 1.4.8.0; plan for version detection via DBGMCU / a known
      signature so a stock update doesn't silently break it).
- [ ] On-screen UI: live mirror + SD browser + load-to-slot + patch mgmt. **Started 2026-10-20**
      in MicroPython framebuf (not LVGL): `pico/gv_ui.py` = a pixel-exact port of the
      emulator; WAVE (static) / PARAM / MOD + SOUND‹› done, checked by `gv_pico.py ui`.
- [ ] **Then** hardware: eurorack PCB + panel (KiCad), ~8 HP, bus power → 3.3 V,
      VTREF sense only (no back-power), SWD header to ribbon.
- [ ] Optional Pico W: serve the Phase-2 web app/API over WiFi too.

### GRAINVIEW spec — LOCKED 2026-10-11
- **Display:** 128×128 **greyscale** OLED (SSD1327, 1.5"). Elektron-style mono look.
  Active area 26.7 mm square (1.5" = diagonal), ~0.21 mm pixels.
  **Readability confirmed 2026-10-12:** Intellijel Metropolix uses a ~1.3" 128×64 OLED
  (~0.23 mm pixels, ~5 px status text) and Leo found it easy to read in use → same
  pitch, twice the rows. Browser preview at actual size looks worse than the real
  panel (blurry system font). Text plan: bitmap fonts; **6×12 for must-read** (file
  names, values), 5×7 for secondary; big shapes for glance info (Metropolix style).
- **Size:** 8 HP × 3U (4.03 cm × 12.85 cm).
- **Brain:** RP2040 (Pico / Pico W), SWD master via PIO; LVGL UI.
- **Controls:** push-encoder + **7 buttons** — BACK, VIEW, FILE, SOUND‹, SOUND›,
  A/B, SETUP. (A/B scene LEDs dropped 2026-10-13 for SETUP — revisit tiny LEDs in the
  A/B legend when the panel is finalised.)
- **Panel layout** (top→bottom): screen · [BACK | encoder] · [VIEW | FILE] ·
  [SOUND‹ | SOUND›] · [A/B | SETUP].
- **4 views** (VIEW button cycles + encoder pages): WAVE · PARAM · MOD · SETTINGS
  (renamed from PARM / SET 2026-10-13 — the status line has room). **All 4 views are per
  sound**; SETTINGS = the focused sound's settings. **SETUP** = overlay for MODULE / PRESET /
  SAMPLE / GRAINVIEW settings. Spec: `docs/SETTINGS.md`.
  Where-am-I = **status line at the bottom** (page dots + view name, Metropolix
  style) — the top tab strip was dropped 2026-10-12 to give content the space
  (Leo: keep for now; fallback idea = tabs shown briefly on VIEW/turn).
- **Interaction model:** encoder turn = page views / navigate; push = dive-in /
  select; BACK = up a level; SOUND‹› & SCENE A/B are global (apply across views);
  FILE opens the SD browser overlay. No long-press / chords (keep it obvious).
- **Role (decided 2026-10-12):** display + file/sound/preset browser. GRAINVIEW
  never edits single params — the module's knobs do that; PARAM/MOD are views.
- **Focus vs playback (decided 2026-10-11):** SOUND‹› moves *edit focus* only
  (`FUN_08011980`) — playing sound keeps going, so you can browse/load/tweak
  another sound silently. SET option **"Select also plays"** (default OFF) adds
  the button-press action (`FUN_0801b4fc`). Firmware separates the two too:
  bright-green LED = focus, fading LED = playing.
- **Power:** rack bus +12 V → 3.3 V; VTREF sensed from Multigrain; shared GND.
- **Link:** 4-wire SWD ribbon (SWDIO/SWCLK/GND/VTREF) to Multigrain JTRACE, on the back.
- **Mockups / spec:** `tools/grainview_emulator.html` (interactive UX = firmware
  spec), `tools/panel_mock.html` (panel to scale), `tools/screen_mock.html` (OLED compare).

Components to buy (when app works, Phase 3): RP2040 Pico W · SSD1327 128×128 OLED ·
push rotary encoder · 6 tactile buttons · 2 LEDs · eurorack power (+12V→3V3) ·
1.27mm header + ribbon to JTRACE.

### Phase 4 — OPTIONAL stretch: module firmware mod
- [ ] Only if ever wanting zero extra hardware. Use `FIRMWARE_MOD_PLAN.md`.
      Not a dependency for anything above.

---

## Immediate next tasks (resume when power supply is back)
1. ~~`mg_sd.py` → confirm real WAV list reads out.~~ ✅
2. ~~Restore the project blanked by the bad preset-load test.~~ ✅ (reloaded its preset)
3. ~~Find the real WAV-into-sound loader.~~ ✅ `mg_load.py`
4. ~~Select sound / switch playback.~~ ✅ `mg_load.py --sound N --play`

## Open questions
- Phone app: responsive **web app served by the bridge** (recommended) vs native?
- Where is the WAV→sound load, and how is the active sound chosen?
- Write-back strategy: inactive-scene write vs setter-function calls.
