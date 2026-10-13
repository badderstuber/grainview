# Multigrain companion app — progress & resumption guide

Personal project: build a computer "screen"/controller for my **Intellijel
Multigrain** (3U granular sampler) — it's hard to use without a screen and the
audio-file workflow is confusing. This file is the single place to pick the
project back up if I lose the chat session.

_Last updated: 2026-10-13._

---

## Update 2026-10-13 — WAVE view = live grain animation, style B chosen ✅ (mock only)

Worked without the module (`grainview_server.py --mock`). Leo's direction: WAVE shows
**no values** — the waveform fills the box and turning a knob changes the *picture*;
numbers live in PARM / the hero. Inspired by the Evil Pet + Tasty Chips GR-1 grain dots.

- **Grain dots = one dot per grain**, simulated from the knobs (not the engine's real
  grain voices — SWD polling is far too slow to animate those). Model from the manual's
  "anatomy of a grain" + SCAN text: RATE = grains/s (the density control; RATE-SIZE link
  + SYNC aware); SIZE = dot lifetime (floor 80 ms) and travel distance; PITCH = read
  speed (dot travels SIZE x pitch-ratio of the sample); SHAPE = brightness over life,
  scaled by LEVEL; launch point = the **scan playhead**: grains launch from START, SCAN
  steps each *successive grain's* start through START..START+WRAP (fwd/back, centred =
  static), reset to START on SOUND press. Dots sit above/below a thin wave band. Only
  the playing sound makes grains. Dot count = grains overlapping (RATE x SIZE).
- **Fixed:** the old dotted SCAN "position" line was wrong (SCAN is a per-grain step,
  not a position) — it's now the playhead.
- **Styles compared side by side** in new `tools/wave_compare.html` (4 embedded
  emulators + shared mock knobs): A pure / **B status readout** / C B+MORPH hairline /
  D B with static dots. **Leo picked B**: any knob on WAVE changes the picture and shows
  small in the status line (`SIZE 427ms`), no hero on WAVE. B is the default; A/C/D +
  compare page kept until judged on the real OLED, then strip the losers.
- **Placeholders:** `SCAN_STEP` (0.05 window/grain at full SCAN — map from the grain
  engine), sample length faked 2–10 s (`sampleSec`; real = WAV header, see preview spike),
  no REVERSE, `GRAIN_SPREAD` visual only, dot size / `WAVE_AMP` to judge on the OLED.
- **Links shown on PARM** (Leo: the panel's lit buttons show them, so not on WAVE; but PARM is
  where you read numbers). PARM grid reordered (`PARM_ORDER`) so RATE · SIZE · PITCH share a
  row (SIZE = hub of both links); a lit link = an 11x5 **chain icon** between the two labels
  (tried inverted labels + dotted lines first — didn't read clearly). Hero of a derived value
  (RATE under R›S, SYNC wins; SIZE under S›P) — tried chain + `LINKED` in the hero too,
  Leo: PARAM only. Linked RATE shows the
  **overlap** the knob sets (`x1.0`..`x8.0`, `gv_units.js`), not Hz. TONE text rounded to whole
  Hz / kHz (`HP 425`, `LP 7k`) so it fits its cell. MOD keeps its row order. Mock has the
  flags + `POST /mock_mode` (mock only) and R›S / S›P / SYNC buttons on the compare page.
- **Views renamed** PARM → **PARAM**, SET → **SETTINGS** (status line has room).
- **Also:** emulator `?wave=A..D`, `?embed=1`, SETTINGS › Wave style; `gv_draw.js` `?zoom=N`;
  mock knob sliders (emulator legend + compare page) drive `/param` like real knobs.

## Update 2026-10-12 (night, later) — WAV-preview spike ✅ (read file off SD → play on the laptop)

Idea (Leo): when browsing SD WAVs to load, hear a **raw, unprocessed preview** of the
file so you pick the right one — and play it **through the browser/phone, not the module**
(keeps the engine silent + the patch untouched; module playback would granular-process it).
**Spike PROVEN on hardware 2026-10-12** on throwaway Project05: read `/Wavs[3]`
(Cascadia loop) off the card over SWD, reconstructed, `afplay`'d on the Mac — Leo heard
the beat. Module never sounded, patch untouched.

- **Reader:** `FUN_0801fb94(folder, name, buf, max, &n)` — raw file read. Seeks past the WAV
  header, `f_read`s PCM into `buf`, `*n = bytes>>2`. folder 0/1/2 = project//Wavs//Recs;
  `name` = ptr to the RAM filename (/Wavs list `0x30008800` + idx*0x100). `max` is in
  4-byte units, so it reads ≤ `max*4` bytes. Returns 0 = OK.
- **5th arg (`&n`) is on the STACK** (AAPCS r0-r3 only hold 4). The existing call helpers
  (`mg_call`/`mg_load`) only set r0-r3, so the spike script pushes it: catch the idle loop,
  save full context, `sp-=16` + write `&n` at `[sp]`, set r0-r3 + LR=catch(`0x08000000` BP)
  + PC=reader, resume, catch the return, **restore the whole idle context**, resume. One
  idle-loop halt → tiny audio blip while browsing (inaudible on the Pico). Clean recovery
  on timeout. Tool: **`tools/spike_preview.py [idx] [max]`** (+ `tools/spike_recon.py`).
- **Scratch buffer = top of SDRAM `0xC3F00000`** (`&n` word at `0xC3FE0000`). SDRAM bank =
  `0xC0000000..0xC3FFFFFF` (**64 MB**); sounds hold **no raw SDRAM pointer** (allocator-
  managed), so buffers can't be found via the struct — the top is clear of them. `0xD0000000`
  unmapped. Verified the read overwrote scratch; nothing else disturbed.
- **Format: card WAVs are 16-bit PCM** (NOT 32-bit float — first guess wrong; `bytes>>2`
  is 4-byte *words* = 2 samples). Heard correct as **mono 48 k**; real build must read the
  44-byte header for exact rate/ch/bits instead of guessing.
- **TO FINISH (parked, Leo back later):** (1) read the WAV header over SWD for exact format;
  (2) add `GET /preview?folder=&index=` to `grainview_server.py` (header+PCM over SWD → .wav
  blob); (3) FILE overlay: scroll → **debounced** Web Audio preview (play-on-land / stop-on-
  move), cap ~1–2 s. Same architecture later on the Pico (SWD read → WiFi → phone).
- **State left:** module on **Project05** (throwaway), GRAINVIEW server **stopped**. Earlier
  this session the live app (`grainview_server.py`, port 8745) was re-confirmed reading the
  module end-to-end (`/state` clean, connected).

## Update 2026-10-12 (night) — two open hardware checks closed ✅

- **Empty-sound WAV load — HARDWARE-TESTED ✅.** All 17 projects were full, so created a
  throwaway **Project05 over SWD** with `FUN_08012c54(4, 0)` — the panel's exact pad call.
  It DOES create a missing project (the mkdir is inside the open-or-create wrapper
  `FUN_0805253c`/FatFS, reached via `FUN_08024598`; a mid-session doubt that it "doesn't
  create" was WRONG — confirmed the note). Loaded `/Wavs[3]` into empty Sound 1: firmware
  reset the sound + loaded file 0, then `mg_load.fix_cursor` injected a 2nd load → landed
  on index 3 (`intellijel-10-Cascadia-percussion-loop.wav`), not file 0. Note:
  `mg_preset.py` guards against switching to a non-existent project; for a throwaway,
  bypass it with a direct `FUN_08012c54(n, 0)` inject on a free slot.
- **Knob-hero ADC jitter — HARDWARE-TESTED ✅, no jitter.** 320 polls over 60 s on the
  selected sound's edited scene: all 10 params + 40 mod depths bit-identical (peak-to-peak
  0.00000), zero false heroes. Firmware only writes stored scene values on real knob
  motion, so TOUCH_EPS (0.004) has huge margin.
- **Sound `+0x4f4` "missing-file" flag — CONFIRMED by offline RE** (no hardware needed).
  It's a per-sound, persisted, reactive u8 (setter +0x4ec/+0x4f0; deserialized from the
  .mgp by `FUN_08022d38`, copied in copy-sound `FUN_08039c84`, cleared on sound-clear
  `FUN_0800927c`). The project/preset reload `FUN_08012a3c` sets it **1 when a sound has a
  stored filename but the WAV fails to load** (load ok → 0, empty/no name → 0); so
  non-zero = referenced file missing. (`FUN_080129b0` returns non-zero=success — verified
  via the audio-length-clear on the 0 path.) Only the reload sets it, not interactive
  browse-loads — which is why our just-loaded Sound 1 read 0, and why all sounds read 0
  (every file present). Empirical `1` would need a project pointing at a deleted file.
- SD/projects confirmed fully disposable (Leo: backed up, do anything). Module left on
  Project02 (session start); throwaway Project05 remains on the card.

## Update 2026-10-12 (evening) — any-folder WAV load, presets + projects

- **WAV from any folder:** `mg_load.py --folder project|wavs|recs [N]`; GRAINVIEW FILE
  opens on the sound's folder; `..` / BACK = up to a root list (PROJECT, WAVS, RECS,
  PRESETS, PROJECTS + counts, CUR = sound's folder); FILE again = quick jump to the next
  folder (Leo: the FILE-cycle alone felt too "magic"). HW-tested.
- **Presets / projects:** `mg_preset.py` save / lock / load / switch project / autosave,
  all HW-tested. In GRAINVIEW (decided with Leo: "FILE hub"): PRESETS / PROJECTS pages list
  the 48 slots (CUR / LCK tags, empty dim); push a slot → LOAD / SAVE|OVERWRITE / LOCK, or
  OPEN / SAVE NOW. Overwrite needs a 2nd push; locked can't be saved over. Server:
  `POST /preset {action,n}`, `POST /project {action,n}`, `/state.store`.
- Addresses + functions: ROADMAP Phase 1.

## Update 2026-10-12 (later) — module back: Phase 1 finished, app live on hardware

- `mg_slots.py` verified; live GRAINVIEW backend verified end to end (see ROADMAP Phase 2).
  Run live: `tools/venv/bin/python tools/grainview_server.py [--port N]`.
- ST-Link "Write verification error" on 1-byte writes = firmware changing the byte
  between write and read-back; `mg_load.write8()` handles it (use it for all u8 writes).
- **Unit conversions done** (`tools/gv_units.js`), engine fs 48076 Hz. Engine object
  0x20000570 = live param block base (START at +0x8c = 0x5fc). Settings flags per sound:
  +0x53d RATE-SIZE link, +0x525 SIZE-PITCH link, +0x8f1 pitch quantizer mode, u16
  +0x554 note mask, +0x90c pitch offset; global: 0x24025dc5 SIZE max mode, 0x24025bc1
  sync enable (hardware-confirmed: 1 once SYNC is enabled), f32 0x24020834 clock period (s). Full RE notes: ROADMAP Phase 1.

## Update 2026-10-12 — Phase 2 started (module away)

- **Phase 2 = the GRAINVIEW emulator, live.** The old dashboard (`demo_app.html`)
  concept is dropped.
- New **`tools/grainview_server.py`**: serves `grainview_emulator.html` + JSON API.
  `--mock` (fake module) tested end to end; live SWD backend written on top of the
  mg_param/mg_load helpers but **not yet hardware-tested**. Port 8745.
- Emulator now polls `/state` (no more hard-coded mock data); SOUND‹› selects on
  the module, FILE lists the real folder and loads, SET has "Sel plays".
- Parked Phase 1 items (need module / offline RE): `tools/mg_slots.py` (written,
  untested) and unit conversions. See ROADMAP.md.

---

## Update 2026-10-11 — interactive control proven + module direction set

- **Function-calls over SWD WORK** (`tools/mg_call.py`): halt → set registers →
  run a firmware function → catch return → restore → resume. Tested the SD
  dir-scan `FUN_0801f0d4()` live: returned cleanly, module kept running. This
  unlocks *driving* the module with its own code — no firmware mod.
- **Ghidra located the file/sound functions** (overnight job → `GHIDRA_FINDINGS.md`,
  callers → `GHIDRA_CALLERS.md`):
  - ~~WAV loader~~ **CORRECTED 2026-10-11: PRESET loader.** `FUN_08012b24(n)` →
    `FUN_08026754(n, target)` opens **`Preset%02d.mgp` with n+1** in the current
    project (format string @`0x0805c7d8`), reads 4-byte checksum + ≤0x8000 body
    (matches .mgp sizes 16388/32772), deserializes via `FUN_08023aec`.
    "SD: Loading %s" is the PRESET log, not WAV. Real WAV loader still unknown.
  - Dir scan: `FUN_0801f0d4()`. File list in RAM: names at **`0x30008800`**
    (0x100 each), count at **`0x240272d8`** → `tools/mg_sd.py` reads it.
  - Sounds array at struct base `+0x58c`, `0x9f0` stride.
- **`mg_sd.py` WORKS on hardware (2026-10-11):** read 11 filenames from
  `/Multigrain/Wavs` (index 0–10, last = `leo-bangla-stabs.wav`) — list order
  is alphabetical, index = position.
- **First load test (2026-10-11): `mg_call.py 0x08012b24 10`** → returned in
  0.02 s (r0=0x20008c5c), then module went dark: all LEDs off except **Sound 1
  blinking green**, SD LED on, no audio. CPU still alive: PC sampled (DWT_PCSR
  `0xE000101C`) = `0x0800ba9e` = **main idle loop** in `FUN_0800ba80`:
  `while(!*(u32*)0x24020b30); FUN_08012fb4(); *0x24020b30=0;` — i.e. main waits
  on a tick flag then runs the UI/control task. Our call was injected at that
  idle point (clean spot). **Cause:** arg 10 = load `Preset11.mgp`, which
  doesn't exist → project state cleared to empty, then autosaved → that
  project's `Autosave.mgp` now blank (all sound buttons grey, selected one
  blinking green). Power-cycle doesn't fix (it's on the card); module boots fine
  without the card / in other projects. `tools/mg_pcsample.py` (new: DWT_PCSR
  histogram, no halt) confirmed CPU healthy (~81% main idle loop). **Fixed** by
  reloading one of that project's saved presets from the front panel (confirmed). SD backup on Leo's
  Desktop was taken AFTER the incident (contains blank autosave).
  Lessons: switch to a throwaway project before load experiments; verify a
  function's format strings/args in the .bin before calling it.
- **Preset load WORKS (2026-10-11):** new `tools/mg_preset.py N` (one-halt,
  return-to-idle call of `FUN_08012b24(N-1)`). Project01 Preset02 then Preset01:
  ~13 ms halt, SD done in ~1.1-1.4 s, all 16 scene rows changed; Preset01
  matched the session's first scene dump exactly. File must exist!
- (old note) we now have a working-ish **"load preset N" call** — call
  `FUN_08012b24(n)` with n = existing preset number − 1 (test on a scratch project).
- **Real WAV loader found (offline, 2026-10-11)** with new `tools/mg_xref.py`
  (BL/literal xrefs straight from the .bin):
  - `FUN_0801fb94(folder, name, buf, max, *n)` = raw WAV read (folder 0=project,
    1=/Wavs, 2=/Recs). `FUN_080129b0(folder, name, sound)` = load into sound N.
    `FUN_08012a3c(N)` = reload sound N from its struct. `FUN_08012edc(a,b)` = copy sound.
  - **`FUN_0803e710(ui, delta)` = front-panel browse+load** into the *current*
    sound: cursor += delta (clamped), load, set filename param via setter on
    success. UI calls it with ui=`0x240452c8` after checking SD ready.
  - Current sound u8 `0x24025b30`; sound struct `0x24020b84 + N*0x9f0`
    (source u8 +0x59c, /Wavs filename +0x6c8, "missing" flag +0x4f4);
    browse cursor i32 `0x24033344 + (folder*8+sound)*4`; counts
    `0x240272d4 + folder*4`; lists 0x30000800 / 0x30008800 / Rec ints 0x30010800;
    SD state `0x20008ccc` (1 busy, 3 error).
  - **`tools/mg_load.py`** wraps it: status (read-only) / `INDEX --dry-run` /
    `INDEX`; only injects while CPU is in main idle loop (thread mode).
    **HARDWARE-TESTED 2026-10-11 ✅:** Sound 4 <- [10] leo-bangla-stabs.wav,
    r0=1 in 0.08 s, sound plays it, cursor 10, module fine. Current-sound byte
    confirmed against front panel.
- **Sound focus vs playback (2026-10-11):** `FUN_08011980(n)` = set *edit
  focus* (reactive setter on `0x24025b30`) — tested: knobs/bright LED move, old
  sound keeps playing. Real button = `FUN_08030e4c`: focus + (if loaded)
  `FUN_0801b4fc(n)` (immediate if input #7 held / repeat, else queued via
  page+8 = n+0xe, presumably for release). **`FUN_0801b4fc` is NOT "play"**:
  loaded → `FUN_08012494(n, b)` copies a block of params into sound n from a
  2nd table @ `0x24025c60` indexed by b (= sound+0x945, 0/1 — scene?); empty →
  opens browser. A `--play` built on it did nothing audible; removed.
  `mg_load.py --sound N` = focus only.
- **Playing sound found (2026-10-11)** via `mg_peek --find` (RAM diff while
  pressing real buttons) + new **`tools/mg_watch.py`** (DWT write-watchpoint →
  prints the writing code): playing sound = u32 **`0x20008c70`** (engine state
  `0x20008c5c` +0x14, mirror +0x1c). Written by engine tick `FUN_0801a49c`:
  `if (events & (1<<3)) playing = selected` (+ has-audio checks). Events word
  `0x240441b8`, posted by `FUN_0802a25c(n)` (atomic |= 1<<n), fetched+cleared
  each tick by `FUN_0802a2c4`. Audio voices hold sound-struct ptrs at
  `0x200003b8` / `0x200006a0` (2 voices — crossfade?). `mg_load.py --play` =
  post event 3 after select — **HARDWARE-TESTED ✅** (playback + LED follow).
- **Halts glitch audio** (any halt > audio buffer period; even lean 8-reg
  batched save/restore is audible). So: **prefer plain RAM writes while
  running.** Halt-free select = write u8 `0x24025b30` (+ notify's side step
  state+0x11 = state+0x08); skipped the UI page's vtable+0x40 "sound changed"
  call — tested: LEDs move instantly, knobs edit the new sound, nothing odd.
  Halt-free play = set bit 3 of events `0x240441b8` (only when word is 0).
  Now `mg_load.py` default; `--halt-select` = old setter call. Select notify =
  std::function @ `0x24024b84+0xf9c` (invoker `0x0800bde0`).
  **WAV load still needs a call (halt → glitch).** Panel loads (ALT → folder,
  ‹prev/next›) are clean; panel buttons are raw GPIO reads (`FUN_0802c818`) so
  can't be injected. Shrunk to **one halt**: catch idle loop, set r0/r1, LR =
  idle-loop top (`0x0800ba9a`), PC = `FUN_0803e710`, resume — function returns
  straight into main's loop (AAPCS keeps r4/r5; loop holds nothing in r0-r3),
  completion confirmed by RAM polling. Measured **~16 ms** halted (ST-Link USB
  round-trips) → still a small blip. **On the Pico (direct SWD, no USB) the same
  halt is ~tens of µs → expected inaudible.** Accepted for dev; verify on Pico.
  (Fully halt-free option parked: RAM VTOR copy + DebugMon via FPB breakpoint on
  the idle loop + RAM trampoline — fiddly, SD-corruption risk if wrong.)
  `--halt-load` = old two-halt path.
- **Scene A/B mapped + write-back WORKS (2026-10-11, hardware-verified):**
  Sound n struct `0x24020b84 + n*0x9f0`: **Scene A** floats at +0x48 START,
  +0x4c SCAN, +0x50 WRAP, +0x54 SIZE, +0x58 RATE, +0x5c PITCH, +0x60 LEVEL,
  +0x64 TONE, +0x68 SHAPE, +0x80 BLUR (same layout as live block @0x200005fc);
  **Scene B = A + 0x264**. MORPH at B → live == B (LEVEL/TONE differ = modulation
  on top). Knobs write straight into the stored scene values. **Plain RAM write
  of a stored value = engine follows within a tick, not overwritten unless a
  knob moves; no halt, no glitch** — Leo heard SIZE 0↔0.5 toggling.
  New **`tools/mg_param.py`** (table / one sound / set / `--wiggle` A-B test).
  **Knob takeover = JUMP** (touching a knob snaps the param to the knob's
  position; app values last until a knob moves).
  **Autosave:** project switch saves the outgoing project (our writes survive),
  but the background autosave only runs when the **project-changed flag**
  `0x20008c6d` (state+0x11) is set — plain writes don't set it (power-cycle
  lost them). UI task (`FUN_08012fb4`, r4=state) checks every ~10 s (state+0x0c
  ≈1 kHz tick counter, threshold ~10000): settings flag +0x10 → Settings.mgs,
  else +0x11 → Autosave.mgp (`FUN_08021bf8`), clear on success. **Fix: after a
  write set +0x11 = +0x08 (autosave-enabled)** → module saved within 4 s,
  value survived power-cycle ✅. `mg_param.py` does this by default (`--no-save`).
  Current project index u32 `0x20008cc4` (Project%02d = n+1), path `0x240332fc`.
  Boot quirk: physical knob positions get applied to the edited scene at boot.
  Open:
  other per-scene params (mod matrix etc.) beyond these 10.
- **Mod matrix mapped + writable (2026-10-11, hardware-verified):** 4 sources
  **RAND, X, Y, Z** (RAND = click RAND then turn a knob; X/Y/Z = CV ins), depth
  per scene. In each scene block: source k block at +0x9c + k*0x48 =
  [u32 flag = any non-zero depth][depth floats, same layout as params: START
  +0x00 … SIZE +0x0c, PITCH +0x14, TONE +0x1c, BLUR +0x38]; i.e.
  depth = scene + 0xa0 + k*0x48 + (param_off − 0x48). Bipolar −1..1. Panel
  clears the flag when a source has no depths left. `mg_param.py --sound N`
  shows the matrix; `--mod SRC PARAM V` writes it (keeps flag, marks dirty) —
  RAND→SIZE 1.0 audibly randomized, 0 settled ✅.
- **Panel LED sync (2026-10-11, hardware-verified):** the panel draws knob
  LEDs from per-knob **virtual values** (u32 floats 0..1, bipolar v as (v+1)/2)
  at `0x240436b0` START, b4 WRAP, b8 SCAN, bc SHAPE, c0 BLUR, c4 LEVEL, c8 RATE,
  cc SIZE, d0 PITCH, d4 TONE — loaded on mode entry, moved by knobs, NOT
  re-read from the stored values (so our writes didn't show until mode re-entry).
  Writing the virtual value updates the LED live and does NOT change the param.
  UI page ptr `0x20008cc0`: `0x24020b48` = normal, `0x24045210` = mod mode
  (RAND/X/Y/Z; source u32 @ page+0x10, 0-3). **Edited scene** u8 `0x24025b48`
  (1 = B) — separate from MORPH (what you hear)! Mod modes time out back to
  normal; depths unaffected. Mod knob handler `FUN_0803779c` (vtable slot of the
  mod page) memcpys a 0x48 source block, callback only marks dirty.
  `mg_param.py` now syncs the LED when the panel shows the written value
  (same sound + edited scene + mode/source) — yellow↔purple confirmed ✅.
  UX note: app/GRAINVIEW must show *edited* scene and *heard* (MORPH) separately.
- **Endgame direction chosen (Leo's idea):** a dedicated **"GRAINVIEW" screen
  eurorack module** — RP2040 + **128×128 greyscale OLED (SSD1327)** + push-encoder
  + 4 buttons, **8 HP**, bus-powered, 4-wire SWD ribbon to JTRACE. The Pico is the
  SWD master running our read+call logic; Multigrain unmodified. Dev path:
  breadboard Pico first, then KiCad PCB. Pico W can also serve the web app over
  WiFi as an optional big-screen view. See ROADMAP.md Phase 3.
- **Mockups built (no hardware):** `tools/screen_mock.html` (OLED options
  compared), `tools/panel_mock.html` (8 HP panel to scale with live screen),
  `tools/grainview_emulator.html` (interactive module emulator = firmware spec).
- **GRAINVIEW spec LOCKED (2026-10-11):** 128×128 greyscale OLED (SSD1327), 8 HP×3U;
  push-encoder + 6 buttons (BACK, VIEW, FILE, SOUND‹, SOUND›, A/B) + 2 same-colour
  A/B scene LEDs; 4 views WAVE·PARM·MOD·SET (VIEW btn + encoder cycle); turn=page/
  navigate, push=dive/select, BACK=up, SOUND/SCENE global, FILE=overlay, no chords.
  Full spec in ROADMAP.md Phase 3. Web app = faithful emulator of this module (one
  UX, later ported to LVGL).
- **Day-job framework (`.claude/`):** bootstrap **deferred** — it's TDD/web-shaped
  and this phase is exploratory RE/hardware. Revisit when building the firmware/web
  app. Context clear/restore handled by memory + this file + `/clear` (no framework
  needed).

---

## TL;DR status

- **Original idea (control over USB MIDI) is dead** — proven. The Multigrain has
  no USB-device mode (USB-C is firmware-update/DFU only) and **no MIDI parameter
  input at all**. Confirmed three ways (live hardware, firmware strings, official
  manual). External control is **analog CV only**.
- **The viable path to the live "screen" I actually want: read the module's RAM
  over its SWD debug port** with an ST-Link, while it runs. The Cortex-M7 reads
  memory in the background, so audio never stops. No firmware modification, fully
  reversible, no brick risk.
- **The debug port exists and is accessible**: an unpopulated `JTRACE` 20-pin
  1.27 mm CoreSight header on the H7 Backpack daughterboard.
- **Software is built and tested** (in `--mock`, no hardware): `mg_peek.py`
  (live RAM read/scan) and `mg_mirror.py` (live web dashboard). pyOCD installed.
- **Blocked only on one cheap part + a bit of soldering** (a 2×5 1.27 mm pin
  header), then: scan addresses → fill `mg_addrs.json` → live mirror.

---

## Hardware facts

- Module: **Intellijel Multigrain 3U rev001.03**. CPU is on a daughterboard:
  **"intellijel H7 II Backpack rev003.01"** (STM32H7 + Alliance SDRAM).
- MCU: **STM32H7** — STM32H753 (earlier photo / my read) vs possibly H7B52
  (blurry close-up). **Doesn't matter for read-only SWD**; confirm on first
  connect by reading DBGMCU_IDCODE at `0x5C001000` (low 12 bits: `0x450`=H75x,
  `0x480`=H7A/B, `0x483`=H72x/H73x).
- USB-C = **DFU/firmware only** (ST bootloader `0483:df11`; enter via power-on
  while holding **Boot**). In normal boot NOTHING enumerates on USB.
- External control surface = **CV only**: 3 assignable CV ins (X/Y/Z → any
  granular param), MORPH CV in (+attenuverter, blends Scene A↔B), Sound-select
  CV, SYNC clock in.

## Firmware RE (done earlier, still valid)

- `Multigrain.1.4.8.0.bin` (634672 bytes), C++/GCC10+newlib, Cortex-M7, flash
  @`0x08000000`. Ghidra 11.1.2 at `~/ghidra_11.1.2_PUBLIC` (scripts in session
  scratchpad are ephemeral — re-import from the .bin if gone; ARM:LE:32:Cortex).
- **Preset format cracked** (packed LE stream, version byte `0x11`, 8 Sound
  records + trailer; reactive param model w/ per-field setter callbacks). Full
  notes: `tools/PRESET_FORMAT.md`. The setter callbacks are the ideal tap point
  for live state.

## The debug-port path (current plan)

- `JTRACE` = **2×10, 1.27 mm (0.05") ARM CoreSight-20** header, unpopulated, on
  the Backpack next to the BOOT button. Measured ~13 mm long → 1.27 mm pitch.
- CoreSight-20 pinout: 1=VTREF, 2=SWDIO, 3=GND, 4=SWCLK, 5=GND, 6=SWO,
  9=GNDDetect, 10=nRESET, 12=TRACECLK, 14/16/18/20=TRACEDATA0-3, other odd=GND.
  The SWD subset (pins 1–10) includes SWDIO/SWCLK/GND/VTREF/SWO/nRESET — all we
  need (SWO too, for ITM later). Only parallel trace (11–20) is dropped.
- **Hardware in hand:** genuine ST-Link/V2 (CN3 = 20-pin 2.54 mm JTAG, + its
  20-pin ribbon), **Olimex ARM-JTAG-20-10** adapter, and its 1.27 mm 10-pin grey
  ribbon cable.
- **Still to buy:** a **2×5 (10-pin) 1.27 mm male pin header** to solder into
  JTRACE **pins 1–10** (the half nearest pin 1). That's the only missing part.
- Connection chain: ST-Link CN3 → 20-pin ribbon → Olimex 2.54 side; Olimex
  1.27 side → grey cable → soldered 2×5 header on JTRACE pins 1–10.
- Module stays on **rack power**. Do NOT power from the ST-Link; VTREF is sensed
  through the chain. Multimeter-check first: pin 1 ≈ 3.3 V, odd pins = GND.

---

## Tools (all in `tools/`, run with `tools/venv/bin/python`)

| File | What |
|---|---|
| `mg_peek.py` | Read/watch/scan **live RAM over SWD without halting** (pyOCD + ST-Link). `--probes`, `--scan ADDR LEN`, `--watch SEC`, `--float`. |
| `mg_mirror.py` | Polls `mg_addrs.json` → serves live web dashboard at `http://localhost:8744/` (`/state`, `/meta` JSON). `--mock` = fake moving values, no hardware. |
| `mg_addrs.json` | Address map (name→addr→type). Auto-created with **placeholder** addresses; replace with real ones from `--scan`. |
| `sd_browser.py` | Scans a Multigrain microSD, renders WAV waveforms → HTML. Also `--diff`/`--label` to map the preset byte format. Works offline. |
| `make_mock_card.py` | Generates a mock SD tree for offline dev. |
| `demo_app.html` | Clickable UI mockup of the companion app (Sounds/Scenes/MORPH/mod-matrix/waveform). To be wired to live data. |
| `demo_card.html` | Prebuilt SD-browser demo output. |
| `mg_monitor.py`, `mg_probe.py` | USB-MIDI tools — now **moot** for this module (no USB MIDI). Kept for reference. |

Other docs: `FIRMWARE_MOD_PLAN.md` (full feasibility of patching firmware for
2-way USB — 3–9 months, not recommended; SWD read-only is the shortcut in its
§7), `tools/README.md` (how to run everything), `tools/PRESET_FORMAT.md`.

Env notes: Xcode CLT is broken (no source builds) → prebuilt wheels / Homebrew
bottles only. pyOCD 0.45.1 is installed in `tools/venv` and bundles its own
libusb (`libusb-package`), so no Homebrew needed for the ST-Link.

---

## NEXT STEPS (day-of, once the 2×5 header is soldered)

1. Solder the 2×5 1.27 mm header into **JTRACE pins 1–10**. Multimeter-check
   (pin 1 ≈ 3.3 V, odd pins = GND). Wire the chain above.
2. Prove the link + identify the chip:
   ```
   tools/venv/bin/python tools/mg_peek.py --probes
   tools/venv/bin/python tools/mg_peek.py 0x5C001000        # which H7
   tools/venv/bin/python tools/mg_peek.py 0x24000000 -n 64  # peek AXI-SRAM
   ```
   (Audio should keep playing — reads don't halt the core.)
3. Find each parameter's live address:
   ```
   tools/venv/bin/python tools/mg_peek.py --scan 0x24000000 0x8000
   # move exactly ONE knob when prompted → note the changed offset
   ```
   Scan other RAM regions too if needed: `0x20000000` DTCM, `0x24000000`
   AXI-SRAM, `0x30000000` SRAM1-3, `0x38000000` SRAM4, external SDRAM (FMC).
4. Add each discovered address to `tools/mg_addrs.json`
   (`{"name","addr","type":"f32",...}`), repeat per knob.
5. Run the live mirror:
   ```
   tools/venv/bin/python tools/mg_mirror.py      # open http://localhost:8744/
   ```
6. Later: wire `demo_app.html` to `/state`, and (optional) add write-back /
   inbound control via a USB-MIDI bridge into the module's host port, or the
   fuller firmware mod in FIRMWARE_MOD_PLAN.md.

## Overnight job (started 2026-10-10 night)

Running Ghidra headless to locate the **SD/file/sound functions** for the live
write-back path (#2: call firmware functions over SWD). Anchor strings in the
firmware pin them: `SD: Loading %s (%d bytes)...` (WAV loader), `SD: Scan
/Wavs...` / `SD: /Wavs has %d wav(s).` (dir scan/list), `SD: Collect Sound %d:`
(slot assignment). Output -> `GHIDRA_FINDINGS.md` (decompiled functions +
callees). Scripts in `ghidra_proj/` (gitignored): `mg_setup.py` (H7 memory map +
vector seeding), `mg_find_sd.py` (anchor search + decompile). Log:
`ghidra_proj/analyze.log`.

### RESULTS (job done, exit 0 — full decompile in GHIDRA_FINDINGS.md, 194 KB)

Target functions located (STM32H753, base 0x08000000, Thumb — OR the entry
address with 1 when calling):

| Function | Role | Args (from decompile) |
|---|---|---|
| **FUN_0801f0d4** | **Directory scan of /Multigrain/Wavs -> builds file list** | none (uses globals). `f_opendir` via FUN_080522b8. |
| **FUN_08026754** | ~~Load WAV~~ **Load preset `Preset%02d.mgp` (index+1)** — corrected 2026-10-11 | `(uint index, int target)` — builds filename from index+1, logs "Loading %s". |
| FUN_08024414 | Load serialized state/preset into target | `(char* filename, void* target)` — f_open + reader FUN_08023aec. |
| FUN_080277ac | Load project/preset | `(void* target)` — different log fmt. |
| FUN_0801e104 | "Collect Sound" = project-SAVE gather (copies sound WAVs) | `(int struct_base, char* outbuf)`. Confirms **sounds array at base+0x58c**. |

FatFs helpers identified: FUN_080510f0 = f_open(fil,path,mode); FUN_080513f8 =
f_read; FUN_08051884 = f_write; FUN_08051d88 = f_close; FUN_080522b8 = f_opendir;
FUN_08023aec = deserialize/reader; FUN_0804cb68 = printf-style logger.
Global struct base ~0x20000000; sounds at +0x58c (matches our live RAM — the
0x200005fc param array is sound 0's current block).

**Morning next steps (needs hardware + you):**
1. Confirm arg semantics by reading the CALL SITES of FUN_0801f0d4 /
   FUN_08026754 (Ghidra xrefs — can re-run headless with an xref script, or just
   inspect what regs are set before the call).
2. Build an **SWD function-call helper** (pyocd: halt, set r0..r3 = args,
   LR = a return-catch breakpoint addr, PC = entry|1 (Thumb), resume, wait for
   halt at LR, read r0 = return, restore context + resume). Brief audio pause
   during the call is fine for load actions.
3. **Safest first test: call FUN_0801f0d4() (dir scan, NO args)** — lowest risk,
   validates the whole function-call mechanism; verify by reading the refreshed
   file list from RAM. THEN try FUN_08026754(index, target) to load a WAV.
4. Wire into the web UI. Card stays in the module throughout.

Risks: wrong ABI/args can hang the firmware (recover with Boot-button reset /
power cycle — no brick risk). Start with the no-arg dir scan.

## State of live read (DONE)

Full live mirror works: `tools/mg_mirror.py` + `tools/mg_addrs.json` (11 knobs
mapped, verified). `tools/mg_peek.py` has read/--watch/--scan/--find/--map/--set.
Writing current-value slots gets clobbered (knobs are authoritative) - see memory
note; that's why write-back goes via firmware function-calls, not memory pokes.

## Repo / session

- Git repo: **github.com/badderstuber/multigrain**, pushed over SSH via host
  alias `github.com-badderstuber` (key `~/.ssh/id_rsa_github`). I use Bitbucket
  for work; this is personal.
- There's also a Claude auto-memory entry (`multigrain-companion-app`) with the
  same state — but this file is the human-readable source of truth.
