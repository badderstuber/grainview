# Multigrain project — the simple plan

_A 30-second re-orientation. For detail see `ROADMAP.md`; for current state see `PROGRESS.md`._

## The goal
Give my Intellijel Multigrain the screen + control it's missing — eventually as a
little **eurorack "screen" module** (GRAINVIEW) sitting next to it.

## The big realisation
Can't talk to it over USB/MIDI (dead end). **But its SWD debug port lets us read
everything live and even call its own functions** — no firmware hacking, fully
reversible. That's the whole foundation.

## Where I am now ✅
- Live **reading** works: a labelled on-screen mirror of all the knobs. ✅
- **Driving** it works: we can call the module's own firmware functions over SWD
  (proved with the SD directory scan). ✅
- Found the functions for listing SD files + loading a WAV into a slot. ✅
- Decided the endgame: an **8 HP screen module** (RP2040 + 128×128 greyscale OLED).
  Mockups done. ✅

## The four phases
1. **Explore + prove** (SWD read/call, map everything) ........ ▶ nearly done
2. **Finish the SWD features** (browse SD, load file→slot, scenes, write-back) .. ⬜ next
3. **The app UI** (responsive web app: desktop + phone) ....... ⬜
4. **GRAINVIEW module** (Pico bridge → own screen; web app over WiFi optional) .. ⬜ endgame

## When I come back, do this next (needs module + power supply)
1. Plug in, run `tools/mg_sd.py` → see the real WAV list on the computer.
2. Carefully test loading a WAV into a *scratch* slot via `FUN_08012b24(index)`.
3. Find "select active sound" so loads can target a chosen slot.

_(No hardware? → keep designing the GRAINVIEW screen UI flow — all doable offline.)_

## The toolbox (all in `tools/`, run with `tools/venv/bin/python`)
- `mg_mirror.py` — live screen of the params (web dashboard)
- `mg_peek.py` — read/scan/map/write RAM over SWD
- `mg_call.py` — call firmware functions over SWD
- `mg_sd.py` — read the SD file list through the module
- `screen_mock.html` / `panel_mock.html` — module display + panel mockups

## How to pick back up
Memory loads automatically. Just say **"catch up on the multigrain project"** and
I'll read `PROGRESS.md` + `ROADMAP.md`. Use `/clear` when the chat gets long.
