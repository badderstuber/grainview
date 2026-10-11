# Multigrain companion app — progress & resumption guide

Personal project: build a computer "screen"/controller for my **Intellijel
Multigrain** (3U granular sampler) — it's hard to use without a screen and the
audio-file workflow is confusing. This file is the single place to pick the
project back up if I lose the chat session.

_Last updated: 2026-10-11._

---

## Update 2026-10-11 — interactive control proven + module direction set

- **Function-calls over SWD WORK** (`tools/mg_call.py`): halt → set registers →
  run a firmware function → catch return → restore → resume. Tested the SD
  dir-scan `FUN_0801f0d4()` live: returned cleanly, module kept running. This
  unlocks *driving* the module with its own code — no firmware mod.
- **Ghidra located the file/sound functions** (overnight job → `GHIDRA_FINDINGS.md`,
  callers → `GHIDRA_CALLERS.md`):
  - WAV loader entry: **`FUN_08012b24(wav_index)`** (calls `FUN_08026754(index,
    target)`; target buffer = `0x24020b84`).
  - Dir scan: `FUN_0801f0d4()`. File list in RAM: names at **`0x30008800`**
    (0x100 each), count at **`0x240272d8`** → `tools/mg_sd.py` reads it.
  - Sounds array at struct base `+0x58c`, `0x9f0` stride.
- **NOT yet done (needs hardware; Leo's power supply was missing):** run
  `mg_sd.py`, test `FUN_08012b24` load into a scratch slot, find "select active
  sound", map Scene A/B raw arrays, write-back strategy.
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
| **FUN_08026754** | **Load WAV by index into a sound** (best "load into slot" candidate) | `(uint index, int target)` — builds filename from index+1, logs "Loading %s". |
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
