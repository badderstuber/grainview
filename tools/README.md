# Multigrain MIDI tools

Black-box MIDI tools for exploring the Intellijel Multigrain (STM32H753, firmware
1.4.8.0) over its class-compliant USB-C MIDI interface. The module's USB MIDI is
undocumented (the manual mentions MIDI only for SYNC clock), so these help
discover what it sends and responds to, en route to a companion "screen" app.

## Setup (already done)

A venv lives in `tools/venv` with `mido` + `python-rtmidi` (CoreMIDI backend).
To recreate it:

    python3 -m venv tools/venv
    tools/venv/bin/pip install --only-binary=:all: mido python-rtmidi

## Use

Plug the Multigrain into the Mac via USB-C and power it on. Then:

    # See everything the module sends — move knobs/faders/buttons, press SYNC:
    tools/venv/bin/python tools/mg_monitor.py
    tools/venv/bin/python tools/mg_monitor.py --no-clock   # hide clock spam

    # In a second terminal, probe what it responds to while watching its LEDs:
    tools/venv/bin/python tools/mg_probe.py --list         # show ports
    tools/venv/bin/python tools/mg_probe.py --cc-sweep     # which CCs do anything?
    tools/venv/bin/python tools/mg_probe.py --channels     # which MIDI channel?
    tools/venv/bin/python tools/mg_probe.py --cc 10 --ramp # ramp one CC
    tools/venv/bin/python tools/mg_probe.py --notes        # play notes 0..127
    tools/venv/bin/python tools/mg_probe.py --clock 120    # does SYNC lock?

`mg_monitor.py` decodes + tallies all incoming MIDI (prints a summary on Ctrl-C).
`mg_probe.py` sends stimulus so you can map stimulus -> response.

## Live state mirror over SWD (the "screen")

The Multigrain has **no USB-MIDI to a computer** (USB-C is firmware-update/DFU
only) and no MIDI parameter input - confirmed via hardware, firmware strings and
the manual. The viable path to a live on-screen mirror is reading the module's
RAM over its **SWD debug port** (the `JTRACE` CoreSight-20 header on the H7
Backpack), with an ST-Link. The Cortex-M7 reads memory in the background, so the
core never halts and audio keeps playing. No firmware modification; fully
reversible. See ../FIRMWARE_MOD_PLAN.md for why this beats patching firmware.

    # discover where a parameter lives in RAM (move ONE knob when prompted):
    tools/venv/bin/python tools/mg_peek.py --scan 0x24000000 0x8000
    tools/venv/bin/python tools/mg_peek.py 0x5C001000        # DBGMCU IDCODE (which H7)
    tools/venv/bin/python tools/mg_peek.py 0x24000100 --float --watch 0.1

Record each discovered address in `tools/mg_addrs.json`, then run the mirror:

    tools/venv/bin/python tools/mg_mirror.py --mock   # test UI now, no hardware
    tools/venv/bin/python tools/mg_mirror.py          # live, ST-Link attached
    # open http://localhost:8744/

`mg_peek.py` reads/watches/scans live RAM over SWD without halting (pyOCD +
ST-Link; `--probes` to list). `mg_mirror.py` polls the `mg_addrs.json` address
map and serves a live web dashboard (`/state` + `/meta` JSON). `--mock`
synthesizes moving values so the whole pipeline is verifiable without the probe.
Hardware chain: ST-Link/V2 -> Olimex ARM-JTAG-20-10 adapter -> 1.27mm 10-pin
cable -> 2x5 header soldered into JTRACE pins 1-10. Pinout is in mg_peek.py.

## SD card browser (works without the module)

Scans a Multigrain microSD, parses every WAV, renders waveform envelopes, and
writes one self-contained HTML file. Pure stdlib — no deps.

    # When the real card is mounted:
    tools/venv/bin/python tools/sd_browser.py /Volumes/MULTIGRAIN -o card.html

    # Develop/test without a card, against a generated mock:
    tools/venv/bin/python tools/make_mock_card.py /tmp/mock_sd
    tools/venv/bin/python tools/sd_browser.py /tmp/mock_sd -o demo_card.html

`tools/demo_card.html` is a prebuilt demo from the mock card. The browser reads
/Wavs, /Recs and /ProjectNN (incl. nested Wavs). Preset files are recognized by
their version byte (0x11 = v17); see PRESET_FORMAT.md for the cracked container.
(Any stdlib python3 works; the venv is just convenient.)

## Preset diff / labeling (finish the format map)

The preset byte layout is a packed stream whose per-field offsets we label by
comparing two presets that differ by ONE change. On the module:

1. Save a preset.
2. Change exactly one knob/parameter, save again (to a different slot/name).
3. Diff them:

       tools/venv/bin/python tools/sd_browser.py --diff presetA.mgp presetB.mgp

   It prints each changed offset decoded as u8 / u16 / u32 / float32 (old->new).
4. Record what you changed — when exactly one region differs, --label writes it
   to tools/preset_labels.json, and future diffs annotate that offset:

       tools/venv/bin/python tools/sd_browser.py --diff a.mgp b.mgp --label START

Repeat per parameter (START, WRAP, SCAN, SHAPE, LEVEL, TONE, RATE, SIZE, PITCH,
BLUR, REVERSE, RAND/X/Y/Z attenuverters) to build the full offset->name map.
`--merge-gap N` controls how far apart changed bytes are still grouped (default 2).

## UI mockup

`tools/demo_app.html` — a self-contained, clickable mockup of the companion-app
main screen (open it in any browser). Grounded in the firmware-RE parameter
model: 8 Sounds, Scene A/B with a working MORPH fader that interpolates every
parameter (and shows A/B probability for discrete ones like SHAPE/REVERSE), the
RAND/X/Y/Z modulation matrix (editable), and the waveform with a live
START/WRAP/SCAN overlay. Values are representative placeholders — this is a
layout/interaction prototype to react to, not wired to hardware.

## Goal

Capture the stimulus/response map, then build it into a local app that mirrors
the module's state (Sounds, Scenes/Morph, granular params) and lets you drive it
without squinting at LEDs. See ../NOTES or ask Claude for the current plan.
