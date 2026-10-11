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
- [ ] **Read SD file list** through the module (`mg_sd.py`) — names + indices. *(built, needs hardware test)*
- [ ] **Load a WAV into a slot** via `FUN_08012b24(index)` — test safely on a scratch sound; confirm which slot it targets + how to choose the slot.
- [ ] Find **"select active sound"** function/state so loads can target a chosen slot.
- [ ] Map **Scene A / Scene B raw arrays** (we currently read the morphed "current" values) for per-scene display/edit.
- [ ] Figure out **patch write-back** (write inactive scene, or call setter fns) — the clean way to send values without fighting the knobs.
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

Components (draft): RP2040 (Pico/Pico W) · ST7789 240x320 IPS SPI TFT · 1 push
rotary encoder + 2-4 buttons · eurorack power (+12V->3V3 buck/LDO) · 2x5 1.27mm
or 4-pin header + ribbon to Multigrain JTRACE.

### Phase 4 — OPTIONAL stretch: module firmware mod
- [ ] Only if ever wanting zero extra hardware. Use `FIRMWARE_MOD_PLAN.md`.
      Not a dependency for anything above.

---

## Immediate next tasks (resume when power supply is back)
1. `mg_sd.py` → confirm real WAV list reads out.
2. Test `FUN_08012b24(index)` load into a scratch sound (with go-ahead).
3. Find "select active sound" so we can target a specific slot.

## Open questions
- Phone app: responsive **web app served by the bridge** (recommended) vs native?
- Which slot does `FUN_08012b24` load into, and how is the active sound chosen?
- Write-back strategy: inactive-scene write vs setter-function calls.
