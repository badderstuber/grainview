# GRAINVIEW settings — spec

_Decided 2026-10-13 (Leo + Claude), from the Multigrain manual v1.4 (pages cited as p.N)._
The machine-readable catalogue is **`tools/gv_settings.json`** (labels, value types, options,
defaults, panel shortcut) — shared by the server's mock and the emulator. This doc is the why.

## Structure

- **All four views are per sound.** The **SETTINGS view** = the *focused* sound's settings;
  SOUND‹› flips between sounds as in every other view.
- **SETUP button** (new; takes the A/B LEDs' place on the panel — LEDs dropped for now, maybe
  tiny LEDs in the A/B legend at panel finalisation) opens an overlay with everything else:
  `MODULE` · `PRESET` · `SAMPLE` (later, with sampling) · `GRAINVIEW` (the app's own).
  Name "SETUP" is provisional — may change once it beds in.

## Interaction

- SETTINGS view: push = dive in (cursor), turn = move, push a row = **edit** (value inverts),
  turn = change, push = keep, BACK = cancel. BACK again leaves the list.
- SETUP: opens on the group list (push = open group), then the same list/edit as above.
  BACK = up a level; SETUP again (or VIEW) = close.
- Status line: where you are (`SETTINGS`, `SETUP>MODULE`) + the highlighted row's **panel
  shortcut** (e.g. `SYS>THRU` = System Settings page, THRU button) — so GRAINVIEW teaches the
  module. `SYS` = System Settings page (ALT, hold PROJECT 4 s, p.50).
- Any other button cancels an edit. Read-only rows (`info`) refuse edits; a value not yet mapped
  on a live module shows `-` and refuses edits.

## Groups

**MODULE** — global, `Settings.mgs` (System Settings page p.50–52 + boot options p.53):
Rand mod (UNI/BI) · NEXT input (NEXT/RESET) · Autocollect · Gate delay 0–10 ms · SELECT range
0.67–5 V · Grain max (4s / 4s or sample / 8s or sample / full; p.51) · Size scale (Grain Size
Scaling) · Idle return (30 s) · Knob mode (JUMP/CATCH) · Pitch out 1.000–1.100× · Theme
(read-only: only set by holding a button at boot).

**PRESET** — in the `.mgp` (p.54, p.29, p.22): Mod out A / B (9 modes, p.29) · Thru · Latch.

**SOUND** (SETTINGS view) — per sound, in the `.mgp`: Type (SAMPLE/LIVE, p.30) · Sync (p.29) ·
Rate-Size / Size-Pitch links · Ping-pong (p.20) · Fine tune ±7 st (p.29) · Quantizer (12 notes +
root, p.33 — its own keyboard page, below) · Quant on (ALL = knob+mod / MOD only) · Choke · Gate
(p.30).

### Quantizer page (SETTINGS › Quantizer)

One octave keyboard across the screen (lit notes filled, root brightest with a dot; unlit white
keys dark, unlit black keys dark grey), the scale name under it, and two fields: ROOT and QUANT
ON. Turn walks C → B, then ROOT, then QUANT ON (caret under the keyboard marks the note).
- Push a note = toggle it, applied at once (as on the module).
- ROOT / QUANT ON = push, turn, push (BACK cancels). Turning ROOT **transposes the scale** —
  the other notes keep their interval to the root, as the module's long-press does (p.33).
  No long press on GRAINVIEW, so this replaces it.
- Scale names are recognised relative to the root (major, minor, modes, harmonic/melodic
  minor, pentatonics, blues, whole tone, triads, fifths, chromatic); the SETTINGS row shows
  the short form (`C MAJ`, `D# PMIN`) or the note count. Root note switched off → just the
  count.
- Not done: the module's copy-to-other-sounds / apply-to-all (p.33) — could be SETUP actions.

**GRAINVIEW** — local (browser now, Pico flash later): Sel plays · Knob view · Wave style ·
Font · Link (info) · Firmware (info).

**SAMPLE** — later, with sampling (the most complex area): input gain (0.5–8.5×, p.49),
threshold (per recorder mode), resampling / looping recorder, normalize, looper size, freeze
modulation assignments (p.27 "toggle is applied per Preset"), Thru blur bypass / lock (p.22).

## Left out on purpose

- **State, not settings:** Latest Project, Session Count, Preset Number, Latest Scene / Sound.
- **Shown elsewhere:** sample folder + filename (header, FILE); scene / panel / mod values
  (PARAM, MOD).
- **Actions, not values:** Default Sounds save / reset (p.11) — maybe an actions menu later.
- **Blur for empty sounds:** listed as global (p.54) but p.22 says it's saved with the preset —
  it's the BLUR knob on an empty sound, so PARAM covers it.

## Open questions (resolve in the firmware)

- **Sync** is per sound on the panel (ALT › SYNC "for current Sound", p.28) and the manual lists
  both *Sync Enabled* (preset) and *Sync Mode* (sound, undocumented). The only mapped flag is the
  global u8 `0x24025bc1` — does it follow the focused sound? Shown under SOUND for now.
- **Grain max** order: settled offline (2026-10-13) — raw 0..3 = manual order 4s / 4s-or-sample
  / 8s-or-sample / full (the loader's migration treats 0 as the old v1.2 "4 s fixed"). See below.

## Live status

**Reads (built 2026-10-13, untested on hardware):** every catalogued setting with a `ram`
entry in `tools/gv_settings.json` is read from the live module, once a second (settings rarely
change; 20 small block reads). Values are decoded strictly — an out-of-range enum or an
implausible float shows `-` instead of a wrong value. Not read yet: **Gate delay** and
**SELECT range** (storage format unknown). Tested against a fake target
(`read_settings` in `grainview_server.py`).

**Writes:** still refused on a live module (UI: "read-only (live)"). After the hardware
checklist below: preset + sound settings = RAM write + the autosave flag; module settings =
call the record's setter over SWD.

## Settings.mgs map (offline Ghidra, 2026-10-13 — hardware check pending)

**Code:** load `FUN_080277ac` (reads u32 checksum + ≤ 8 KB, checks it, then deserialises with
`FUN_0802695c`; missing file → `FUN_08009bcc` defaults), save `FUN_080225a4` (serialiser
`FUN_08021d58`, checksum `FUN_0803fbb0`), reset-to-defaults `FUN_08009738`. Settings object =
RAM **`0x24025C60`** (anchored by two known addresses: +0x14 = the project u8 `0x24025c74`,
+0x165 = the size-mode u8 `0x24025dc5`). File = `u32 checksum` + `u8 version (0x11)` + fields in
the order below; fields added in later firmware are gated by version.

**Reactive records** (same model as presets): each setting is a record with a `std::function`
setter at record+0x8/+0xc; the value byte sits at record+0x11 (u8) / the float at record+0x14,
the default/pending copy one slot below. Most setters only mark settings dirty (save pending);
a few also apply side effects (Theme palette, recorder thresholds / looper size). **Live writes
must go through the setter** (an SWD function call, like our other firmware calls), not a raw
RAM poke, or the side effect and the autosave won't happen.

| +off | abs addr | type | setting | conf. | evidence |
|---|---|---|---|---|---|
| 0x14 | 0x24025C74 | u8 | Latest project | ✅ | = known project byte |
| 0x2c | 0x24025C8C | 32-bit | Session count | high | bumped at every boot |
| 0x48 | 0x24025CA8 | f32 | Input trim (GAIN) | high | fed to the recorder / engine with its range |
| 0x69 | 0x24025CC9 | u8 | Resampling mode (2 = looping recorder) | high | setter reconfigures the recorder 0/1/2 |
| 0x81 | 0x24025CE1 | u8 | **?** (v1.0-era; Thru-related?) | — | plain setter, no reader found yet |
| 0x99 | 0x24025CF9 | u8 | Normalize | high | gates an extra pass when a recording is saved |
| 0xb1 | 0x24025D11 | u8 | Theme 0–3 | ✅ | set from the button held at boot; setter swaps palette |
| 0xcc | 0x24025D2C | f32 | Threshold, recorder A | high | scaled into recorder +0x310 |
| 0xf0 | 0x24025D50 | f32 | Threshold, recorder B | high | scaled into recorder +0x314 (which is sampler vs looper: TBD) |
| 0x114 | 0x24025D74 | f32 | Looper size (8/16/24/32 s) | high | setter maps 0..3 to 4 buffer lengths |
| 0x135 | 0x24025D95 | u8 | NEXT input: 0 NEXT / 1 RESET | high | NEXT pulse steps sound+1 only when 0 |
| 0x14d | 0x24025DAD | u8 | Rand polarity (1 = bipolar?) | med-high | engine flag; v1.2 pair with 0x135 |
| 0x165 | 0x24025DC5 | u8 | Grain max 0–3 | ✅ | clamped ≤ 3; = known size-mode byte |
| 0x17d | 0x24025DDD | u8 | Idle return | medium | main loop: if 1 and idle → go home |
| 0x198 | 0x24025DF8 | f32 | Pitch out scale | med-high | float, v1.3-gated, fed to the A/B output path |
| 0x1b9 | 0x24025E19 | u8 | Knob mode (JUMP/CATCH) | medium | setter pushes to panel globals; by elimination |
| 0x1d1 | 0x24025E31 | u8 | Auto-collect | high | read in the preset-save routine |
| 0x1d4 / 0xbc4 | — | Sound | Default Sound / default Live Sound | high | two full Sound records |
| 0x15c9 | 0x24027229 | u8 | bounded int (min +0x15ca, max +0x15cb) — Gate delay ms? | low | v1.4-gated |
| 0x15e1 | 0x24027241 | u8 | Grain size scaling | high | fed to the engine with Grain max |
| 0x15f8 / 0x1610 / 0x1628 | 0x24027258 / 70 / 88 | u8 | **?** three v1.4 flags, default off | — | reset to 0 by defaults |
| 0x1644 | 0x240272A4 | f32 | SELECT range | high | multiplies CV input 3 (SELECT) |

Not in Settings.mgs as far as the serialiser shows: Gate delay as a float, Blur-for-empty —
so Gate delay is probably the bounded int at 0x15c9, and Blur-for-empty lives in the preset.

**Hardware checklist (next module session, scratch project):**
1. Read the struct; check values against the panel (Theme, Knob mode, Idle return, NEXT mode…).
2. Flip each System Settings toggle on the panel, watch which byte moves — settles 0x81,
   0x14d polarity, 0x17d, 0x1b9, 0x15c9 (turn START), the three v1.4 flags, threshold A/B.
3. Write test: call one record's setter over SWD (e.g. Idle return), confirm the panel LED
   follows and the value survives a power-cycle (Settings.mgs saved).

## Preset map (offline Ghidra, 2026-10-13 — hardware check pending)

Preset serialiser `FUN_0802120c` (deserialiser `FUN_08023aec`): version 0x11, the 8 Sound
records, then the preset fields below. **The preset object starts at the sound array
`0x24020B84`** (8 × 0x9f0), so preset field +off = absolute `0x24020B84 + off`; three known
addresses land exactly (preset, edited scene, sync). The preset setters only raise the
"project changed" flag (autosave) — **a live write = RAM write + that flag**, like our param
writes (no setter call needed).

| +off | abs addr | type | setting | conf. | evidence |
|---|---|---|---|---|---|
| 0x4f94 | 0x24025B18 | u8 | Preset number | ✅ | = known current-preset byte |
| 0x4fc4 | 0x24025B48 | u8 | Latest (edited) scene | ✅ | = known edit-scene byte |
| 0x4fac | 0x24025B30 | u8 | Latest sound | ✅ | = known current-sound byte |
| 0x4fd8 | 0x24025B5C | u8[2] | Mod out A, B | high | 2-element record, indexed setter; engine reads both |
| 0x4ff5 | 0x24025B79 | u8 | Thru | high | engine reads it with the blur-bypass byte |
| 0x500d | 0x24025B91 | u8 | Latch | high | engine: latched-gate logic |
| 0x5024 | 0x24025BA8 | u8 | **?** (UI-only; Thru lock?) | — | no engine reader |
| 0x503d | 0x24025BC1 | u8 | **Sync** | ✅ | = known sync byte (hardware-confirmed) |
| 0x5055 | 0x24025BD9 | u8 | **?** (UI-only) | — | no engine reader |
| 0x506d | 0x24025BF1 | u8 | Thru blur send / bypass | high | packed with Thru into the input config |
| 0x5080 | 0x24025C04 | u8[4] | Freeze mod assigns (RAND/X/Y/Z)? | medium | 4-element record; 4 flags into the input/looper config |
| 0x50a0 | 0x24025C24 | 32-bit | Blur for empty sounds? | low | into the input config with trim |
| 0x50c0, 0x50d8 | 0x24025C44 / 5C | 32-bit | **?** | — | |

## Sound map (per sound; offline Ghidra, 2026-10-13)

Sound serialiser `FUN_080207e8` / deserialiser `FUN_08022d38`. Sound n = `0x24020B84 + n×0x9f0`
(same base our tools use; +0x525 / +0x53d / +0x59c / +0x4f4 already known). Write order:

| +off | type | setting | conf. | evidence |
|---|---|---|---|---|
| 0x14 | u8 | **?** (record header / type) | — | first byte |
| 0x18, 0x27c | Scene | Scene A, B (panel values, mod, REVERSE) | ✅ | known |
| 0x4f4 | u8 | file-missing flag | ✅ | known |
| 0x50d | u8 | Sync mode (manual: listed, undocumented) | medium | manual order: just before the links |
| 0x525 | u8 | Size-Pitch link | ✅ | known |
| 0x53d | u8 | Rate-Size link | ✅ | known |
| 0x554 | u16 | Quantizer notes (12-bit mask) | high | 16-bit, engine reads it as the scale |
| 0x56c, 0x584 | 32-bit | Quantizer root / enable? | medium | follow the notes |
| 0x59c | u8 | Sample folder | ✅ | known |
| (string) | | Sample filename | ✅ | memcpy after the folder |
| 0x8f1 | u8 | Quant mode (ALL / MOD) | high | manual order; engine reads it |
| 0x90c | f32 | Fine tune (±7 st) | high | float, engine reads it |
| 0x92d | u8 | Ping-pong | high | manual order; engine reads it |
| 0x945 | u8 | **Live** sound | high | bool; pre-v1.4 |
| 0x95d | u8 | **Choke** | high | v1.4: loader forces 0 for older files |
| 0x975 | u8 | **Gate** | high | v1.4: same |
| 0x98c / 0x9a4 / 0x9bc, 0x9d4 / 0x9ec | u8 ×3, 32-bit ×2 | **?** (sampling / trim?) | — | later block |

**Sync — answer + new question.** The sync byte `0x24025BC1` is a *preset* field, so Sync is
one setting per preset, not per sound — but each sound also has a "Sync mode" byte (+0x50d).
The ALT page says SYNC toggles "for current Sound" (p.28): on hardware, toggle ALT › SYNC on
two different sounds and watch both bytes. Until then the UI keeps Sync under SOUND.

**Hardware checklist additions:** toggle THRU / LATCH / ALT›A / ALT›B / blur bypass (LATCH+THRU)
/ THRU lock (hold LATCH+THRU) and watch the preset bytes (settles +0x5024, +0x5055, +0x506d);
toggle a sound's Live / Choke / Gate / Ping-pong / Quant mode and turn Fine tune (ALT›PITCH),
watch the sound bytes; set a quantizer scale and read +0x554 / +0x56c / +0x584.

Ghidra scripts (headless, `ghidra_proj/`): `mg_settings.py` (anchor strings → functions +
callees), `mg_refs.py` (who loads pointers into a RAM struct), `mg_ptrs.py` (follow callback
pointers), `mg_decomp.py` (decompile given functions).
