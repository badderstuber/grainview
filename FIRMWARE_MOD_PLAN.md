# Multigrain two-way USB — firmware modification feasibility plan

**Goal:** make the Multigrain send its live parameter/engine state *out* to a
computer (and accept changes back), so a companion app can act as a real screen
that mirrors the module in real time.

**Why this document exists:** two-way feedback is the one thing CV, host-MIDI
controllers, and the SD card cannot provide. The only ways to get it are (a)
modify the firmware so the module transmits its state, or (b) tap an existing
data egress the firmware already produces. This is an honest scoping of both so
you can judge the effort before committing.

> TL;DR verdict: the full firmware-device-stack mod is a **3–9 month project for
> an experienced embedded-RE engineer**, with permanent maintenance cost and a
> real chance it never becomes reliable. There is a **much cheaper read-only
> path (SWD/ITM trace tap)** that could deliver live feedback in days-to-weeks
> *if* the module exposes debug pads and emits useful trace — that should be
> tested first. See §7.

---

## 1. What's in our favour, and what's against

**In favour (genuinely encouraging):**
- **USB-device hardware is proven to work.** DFU enumerates as `0483:df11`
  ("DFU in FS Mode"), so the STM32H753's USB OTG peripheral *and* the USB-C
  wiring physically support device mode. We are not fighting dead silicon — the
  app firmware simply doesn't bring USB up as a device.
- **The parameter model is reactive.** From the Ghidra work, loading/changing a
  parameter fires per-field **setter/notify callbacks**. That is the *ideal*
  tap point: to stream state out, you hook where the module already announces
  "this value changed." You don't have to poll or understand every consumer.
- **Dual-bank flash (2×1 MB).** You can keep stock firmware in bank 1 and run a
  modified image from bank 2, giving an A/B safety net.
- **Recovery is guaranteed.** The Boot button forces the STM32 ROM bootloader
  regardless of what's in flash, so a bad flash is always re-flashable with
  stock firmware. Bricking risk is low.

**Against (the hard parts):**
- **Closed, stripped C++ binary**, ~634 KB, GCC 10 + newlib. Partial symbol
  recovery only. No source, no linker map.
- **USB role switch.** The app appears to use the OTG core as a *host* (for
  controllers plugged into it). Reusing the same port as a *device* means
  reconfiguring the OTG core, PHY, clocks and interrupt handling at runtime —
  one of the fiddliest corners of STM32 work even *with* source.
- **No free-standing SDK.** Injected code must either call the firmware's
  existing HAL/USB functions (whose addresses and ABIs you must recover) or ship
  its own driver into a code cave — both painful.
- **Maintenance treadmill.** Every official firmware update shifts addresses and
  breaks the patch; you re-do a chunk of the RE each time.
- **Real-time constraints.** The granular engine is latency-sensitive; your
  injected TX code must not starve the audio ISR.

---

## 2. Prerequisites / tooling

- Ghidra 11.1.2 (installed) with the STM32H7 memory map + vector-table seeding
  scripts already written (`ghidra_scripts/`).
- **An SWD debug probe** (ST-Link v3, ~$25, or a J-Link). This is the single
  most important addition — static RE alone will not get you there.
- OpenOCD or STM32CubeProgrammer + arm-none-eabi-gdb for live debugging.
- The STM32H753 reference manual (RM0433) and the OTG_HS/FS chapters.
- A bench setup where the module is powered and patchable without disturbing a
  live rack; ideally a spare microSD and a known-good stock firmware image saved
  locally for instant restore.
- **Physical access to SWD pads** on the PCB (SWDIO/SWCLK/GND, ideally SWO).
  Unknown until you look — this gates Phases 2 and the §7 shortcut.

---

## 3. Phase plan (full firmware mod)

Each phase ends with a **GO/NO-GO gate** — a cheap question that, if it fails,
kills the project before the expensive next phase.

### Phase 0 — Safety harness & recovery (0.5–1 wk)
- Dump stock flash over DFU/SWD; checksum and archive it. Verify you can restore
  it and the module boots. (Do this *before* any modification.)
- Script the flash/restore loop so iteration is fast and safe.
- **Gate:** can you reliably dump and restore stock firmware? If not, stop.

### Phase 1 — Static RE: map the terrain (3–6 wk)
- Finish the function map around the parameter model (setters, the reactive
  notify dispatch, the Sound/Scene structures — partially done).
- Locate the **main loop / scheduler** and a safe periodic hook point.
- Identify **USB code**: does the app link ST's USB OTG HAL? Find `HAL_PCD_*` /
  `USBH_*` / `USBD_*` equivalents, the OTG register base usage (`0x40040000`
  OTG_HS / `0x50000000`… per RM0433), and the IRQ handlers in the vector table.
- Identify the **clock tree setup** (PLL/HSE) so you know the USB 48 MHz source.
- Find **free flash** (padding/erased regions) for a code cave, and spare RAM.
- **Gate:** can you point at (a) the setter/notify callback you'd hook for TX,
  (b) a main-loop hook, and (c) the OTG register usage? If USB is *host-only HAL*
  with no device code present, the effort jumps (you must bring a whole device
  driver) — reassess here.

### Phase 2 — Dynamic analysis (2–4 wk, **needs SWD pads**)
- Attach ST-Link; halt, single-step, set breakpoints on the suspected setter
  callbacks while you turn knobs — *confirm* the static guesses against reality.
- Dump live parameter structures; verify the Sound (stride 0x9f0) / Scene
  (0x264) layouts and the float param array from actual RAM.
- Watch the OTG registers to learn exactly how the app configures the core.
- **Gate:** can you observe a knob move land in a known RAM address via a known
  callback? That confirmed tap point is the foundation of everything after.

### Phase 3 — Injection design (1–2 wk)
- Decide architecture: **reuse firmware HAL** (call its functions by address) vs
  **ship your own** minimal USB-device driver into the code cave. Reuse is less
  code but couples you to their ABI; BYO is more code but self-contained.
- Define hook mechanism: overwrite a branch at the main-loop/init site to jump
  into the cave, do your work, then execute the displaced instructions and
  return (classic trampoline). Mind Thumb-2 encoding and the FPU/caller-saved
  registers.
- Plan cache coherency (Cortex-M7 has I/D cache — injected code and DMA buffers
  need correct MPU/cache handling or USB DMA will corrupt).

### Phase 4 — USB device bring-up (3–8 wk, highest-risk)
- Reconfigure the OTG core to **device mode** (or claim the second OTG instance
  if the port is wired to one that's free — check the schematic/pin muxing).
- Set up PHY, 48 MHz clock, endpoints, interrupts; get the module to **enumerate
  on the Mac as a device at all** (even a bare vendor device with one bulk IN).
- This is where projects stall. Role-switching a shared OTG port at runtime,
  without disturbing the audio engine or the host-MIDI feature, is genuinely
  hard.
- **Gate:** does `system_profiler SPUSBDataType` show your device in *normal*
  operation (not DFU)? If you can't enumerate, the rest is moot.

### Phase 5 — Class + protocol (1–2 wk)
- Implement a **USB-MIDI class** (easiest: class-compliant, no driver) or a
  **CDC/vendor** bulk pipe (higher bandwidth, cleaner for a full-state protocol).
- Define the wire protocol: an initial **full state dump** on connect, then
  **deltas** on change, plus an inbound write channel. Rate-limit so you never
  flood the engine.

### Phase 6 — Wire to the parameter model (1–3 wk)
- **TX (the feedback you need):** hook the reactive setter/notify callback from
  Phase 2 to push `(param_id, value)` into a ring buffer that the USB IN
  endpoint drains. Because the model already fires on change, this is the
  cleanest part of the whole project *once* the plumbing exists.
- **RX:** map inbound messages to the same setters so the app can write back.
- Guard against feedback loops (don't re-emit a value you just received) and
  against writes during audio-critical sections.

### Phase 7 — Companion app (2–4 wk, mostly done)
- Point `demo_app.html`'s model at the live protocol. The UI (Sounds, Scene A/B,
  MORPH, mod matrix, waveform) already exists as a mockup — this becomes the
  real screen. This phase is the easy, fun one.

### Phase 8 — Hardening & maintenance (ongoing)
- Soak-test: does audio ever glitch under USB load? Does host-MIDI still work?
- Re-port the patch to each stock firmware release (budget days per release).

---

## 4. Effort & skills summary

| | |
|---|---|
| **Calendar effort** | ~3–9 months, experienced embedded-RE engineer, part-time-to-full |
| **Hobbyist reality** | 6–12+ months, meaningful chance it never becomes reliable |
| **Skills required** | ARM Thumb-2 asm, Cortex-M7 internals (cache/MPU/NVIC), STM32 USB OTG, binary patching, USB protocol, Ghidra, SWD/GDB debugging, C++ RE |
| **Hard dependency** | Exposed SWD pads on the PCB (Phase 2) |
| **Ongoing cost** | Re-port on every official firmware update, forever |
| **Risk of failure** | High, concentrated in Phase 4 (device bring-up) |
| **Bricking risk** | Low — Boot-button ROM bootloader always restores stock |

---

## 5. Decision gates (where to bail cheaply)

1. **No exposed SWD pads** → full mod becomes near-infeasible (static-only RE of
   a USB role switch is brutal). Pivot to §7 or offline app.
2. **Phase 1 shows host-only USB with no device HAL present** → you must author a
   whole device stack in a code cave; effort ~doubles.
3. **Phase 4 can't enumerate** → stop; the feedback goal is unreachable this way.

---

## 6. Risks beyond effort

- A buggy patch that passes bench tests could still corrupt audio or the SD
  filesystem in the field.
- You're maintaining a private fork of someone else's product forever.
- Legit to do on your own hardware, but it voids any expectation of support and
  each stock update is an adversary, not a gift.

---

## 7. The pragmatic alternative: read-only feedback via SWD/ITM (test this FIRST)

You said the screen/feedback is the whole point — but **feedback doesn't require
a USB-device stack.** The Cortex-M7 has an **ITM/SWO trace** unit and an SWD
debug port. Two low-effort possibilities:

**(a) SWD live-memory polling (no firmware change at all).** With an ST-Link
attached to SWD pads, a host-side tool (OpenOCD/pyOCD) can **read the module's
RAM live** while it runs. If Phase 2 nails down the addresses of the current
parameter struct, the companion app can poll those addresses at, say, 30 Hz and
mirror the state — a real screen, **zero firmware modification**, fully
reversible, no bricking risk. This is the single highest-value experiment.

**(b) ITM/SWO trace tap.** The firmware already has a logger (`FUN_0804cb68`). If
it emits over ITM/SWO (or a UART), you can read that stream read-only with the
same probe. Less certain to carry the data you want, but free to check.

Effort for (a): **days to ~2 weeks**, gated only on (i) accessible SWD pads and
(ii) finding the live param-struct address (Phase 1/2 work you'd do anyway).
Limitation: it's read-only (perfect for a *screen*; for write-back you'd still
need the inbound MIDI-bridge from the earlier discussion, or the full mod).

**Hybrid that meets your stated need:** SWD live-read for the on-screen mirror +
(optional) a small USB-MIDI bridge into the module's host port for sending
changes. That gets you the screen you actually want without the Phase 4
nightmare.

---

## 8. Recommendation

1. **Open the module and look for SWD pads** (SWDIO/SWCLK/GND, ideally SWO).
   This one observation decides everything.
2. If pads exist: buy a ~$25 ST-Link, do Phase 0–2, and try **§7(a) live-memory
   polling** — you may have your screen in a couple of weekends, reversibly.
3. Only if that proves insufficient *and* you still want write-back: escalate to
   the full §3 firmware mod, eyes open about the multi-month cost.
4. In parallel, the offline **SD sample + preset app** remains the zero-risk win
   for the file-workflow pain and loses nothing if the firmware route stalls.
