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
- [ ] **Load preset N** via `FUN_08012b24(N-1)` — verify on a scratch project with an existing preset.
- [x] **Select sound** (focus, `FUN_08011980`) + **switch playback** (engine event 3) — `mg_load.py --sound N [--play]`, hardware-tested 2026-10-11.
- [x] Map **Scene A / Scene B raw arrays** — sound struct +0x48.. (A), +0x264 (B); `tools/mg_param.py` (2026-10-11).
- [x] **Patch write-back** — plain RAM write to the stored scene value; engine follows, no halt (2026-10-11). Knobs JUMP on touch (no pickup). Still to check: autosave persistence.
- [ ] Nice-to-haves: trigger record, save/load project, read slot→file assignments (Sound structs @ base+0x58c, 0x9f0 stride).
- [ ] Real **unit conversions**: RATE→Hz, SIZE→ms/s, PITCH→semitones, TONE→%, SHAPE→name.

### Phase 2 — The app UI (responsive web: desktop + phone)
- [ ] One responsive web app (works in desktop + phone browsers) served locally,
      later by the bridge. Evolve `demo_app.html` into the real thing.
- [ ] Views: **live mirror** (8 sounds, Scene A/B + MORPH, granular params, mod
      matrix, waveform) + **SD browser** (file list, load-into-slot) + patch
      management.
- [ ] Backend API (`/state`, `/meta`, `/sd`, `/load`, `/call`) decoupled from
      transport so it works over USB now and WiFi later.

### Phase 3 — Dedicated "Screen" eurorack module (clutter-free endgame) ⭐
A standalone RP2040-powered module with its own TFT + encoder/buttons that sits
next to the Multigrain and connects via a 4-wire SWD ribbon to JTRACE. Gives the
Multigrain the screen it lacks, no phone/laptop. (Pico W can ALSO serve the
web app over WiFi as an optional big-screen view.)
- [ ] **Breadboard prototype (no PCB):** Pico + ST7789 TFT + push-encoder, jumpers
      to the Multigrain JTRACE pins (same as ST-Link). Prove it end to end first.
- [ ] Port SWD **read** (background mem read) + **function-call** (halt/set-regs/
      run/catch/restore) logic to RP2040 C/C++ (PIO SWD master).
- [ ] Hardcode the mapped addresses + function entry points (firmware-version
      aware — Multigrain 1.4.8.0; plan for version detection via DBGMCU / a known
      signature so a stock update doesn't silently break it).
- [ ] On-screen UI (LVGL): live mirror + SD browser + load-to-slot + patch mgmt.
- [ ] **Then** hardware: eurorack PCB + panel (KiCad), ~8 HP, bus power → 3.3 V,
      VTREF sense only (no back-power), SWD header to ribbon.
- [ ] Optional Pico W: serve the Phase-2 web app/API over WiFi too.

### GRAINVIEW spec — LOCKED 2026-10-11
- **Display:** 128×128 **greyscale** OLED (SSD1327, 1.5"). Elektron-style mono look.
- **Size:** 8 HP × 3U (4.03 cm × 12.85 cm).
- **Brain:** RP2040 (Pico / Pico W), SWD master via PIO; LVGL UI.
- **Controls:** push-encoder + **6 buttons** — BACK, VIEW, FILE, SOUND‹, SOUND›,
  A/B — plus **2 A/B scene LEDs** (same colour; lit=active scene) beside the A/B btn.
- **Panel layout** (top→bottom): screen · [BACK | encoder] · [VIEW | FILE] ·
  [SOUND‹ | SOUND›] · [A/B btn | A/B LEDs].
- **4 views** (VIEW button cycles + encoder pages, tab strip top): WAVE · PARM · MOD · SET.
- **Interaction model:** encoder turn = page views / navigate; push = dive-in /
  select; BACK = up a level; SOUND‹› & SCENE A/B are global (apply across views);
  FILE opens the SD browser overlay. No long-press / chords (keep it obvious).
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
