# Live Sounds + Recorder — RE notes

_Offline RE 2026-10-21 (Ghidra headless + `mg_xref.py`, firmware 1.4.8.0). Nothing here is
hardware-tested yet._ Confidence: ✅ = matches a hardware-known address, **high** = several
independent code paths agree, **medium** = one path / inferred, **low** = guess.

Shorthand: `snd(n) = 0x24020B84 + n*0x9f0`; `R = 0x20000468` (recorder object);
`home = 0x24020B48` (Home page object); `st = 0x20008C5C` (global state, known).

---

## 1. Live Sounds (do this first)

**✅ Hardware-tested 2026-10-21** (`tools/mg_rec.py`, `pico/mgrec.py`; scratch Project27): the
recipe below works on empty and occupied sounds; mask + recorder mode follow; sample kept.

### State

| addr | type | meaning | conf. | evidence |
|---|---|---|---|---|
| `snd(n)+0x945` | u8 0/1 | **Live flag** (the value byte) | high | every panel path reads/writes +0x945; setter compares/stores it |
| `snd(n)+0x944` | u8 | default/previous copy of the flag | medium | UI-task assign copies +0x944 → +0x945 |
| `snd(n)+0x930` | ptr | record vptr = `0x0805C668` (vtable[0] = setter `0x0800C321`) | high | literal pool + vtable dump |
| `snd(n)+0x934..0x943` | std::function | change callback: storage +0x934 (bound arg = n), manager +0x93C, invoker +0x940 = `FUN_0800d7a4` | high | bound by `FUN_08012e34(n)` |
| `0x20008C9C` (`st+0x40`) | u32 | **live mask**, bit n = sound n is Live | high | callback sets/clears bit n; read by `FUN_08012984`, LED code |
| `0x20000454` | u8 | **effective recorder mode**: 0 sample-in, 1 resample, 2 looper | high | written only by the Live callback / Resampling setter / looper-size setter |
| `0x24025CC9` | u8 | Resampling setting (2 = looper always on) | high | (docs/SETTINGS.md) |
| `FUN_08012984()` | fn | "looper active" = `0x24025CC9==2 \|\| mask!=0` | high | used by every SAMPLE handler |

Record layout for this (sound) record: vptr +0x0, std::function +0x4..+0x13, value at **record+0x15**
(record = +0x930, so value = +0x945). Settings.mgs records keep the value at +0x11 — different class.

### What the panel does (both paths need the SOUND button physically held)

- Home: hold SOUND (focused) + click SAMPLE → `FUN_08033ab0(home, 0)` checks the held mask
  (`FUN_0802c844(cur)`, bit in `0x240441BC`) and toggles the **focused** sound.
- ALT page: hold SOUND + SAMPLE → `FUN_0803081c(alt=0x240451DC, 0)`, same toggle; with LATCH held it
  sets all 8 sounds to the new value.

Toggle logic (identical in both):

```
on  (0→1): if sound has no audio  → FUN_08012494(n, 1)   // apply DEFAULT LIVE SOUND record (Settings +0xBC4)
           setter(snd(n)+0x930, 1)
off (1→0): setter(snd(n)+0x930, 0)
           if sound has no audio  → FUN_08012494(n, 0)   // apply DEFAULT SOUND record (Settings +0x1D4)
"has audio" = u32 0x200004D8 + n*0x10 != 0   (FUN_0801286c / FUN_0801288c)
```

Occupied sound: only the flag changes — folder/filename/sample stay assigned (unused while Live,
back when Live is turned off). Empty sound: gets the default Live Sound params (scenes, links, …).
`FUN_08012494(n,b)` also sets +0x945 = b through the setter, so for an empty sound it does the whole job.

### The setter has the side effects → a plain RAM write is NOT enough

`0x0800C320(rec, v)`: `if rec[0x15]!=v { rec[0x15]=v; invoke callback(&n,&v) }`.
Callback `FUN_0800d7a4(&n, &v)`:
- v=1: `mask |= 1<<n`; if mode byte ≠ 2 → **switch recorder to looper**: ring = live-memory slot 8
  (`*(0x20000550)+*(0x2000055C)*4`), size = looper size `0x20000458`, clears R+0x2C..+0x5F (pending
  take, positions), hold 48000, fade 4800, mode=2, state=1. (If coming from resample mode it also
  zeroes the loop buffer.)
- v=0: `mask &= ~(1<<n)`; if mask==0 and setting ≠ 2 → back to mode = setting (0/1): ring size
  0x177000, clears positions, state=1.
- always: `st+0x11 = st+0x08` (project changed → autosave within ~10 s).
- n>7 → `bitset::set` abort (never returns = module hangs). Only reachable with a bad pointer.

A raw poke of +0x945 would leave the mask, the recorder mode and autosave stale → **must call the setter**.

### Call recipe — toggle Live on sound n (0..7), panel-equivalent

1. Read `v = 1 - rd8(snd(n)+0x945)`, `empty = rd32(0x200004D8+n*0x10)==0`.
2. Check `rd32(snd(n)+0x930) == 0x0805C668` (else call `*(*(snd+0x930))` instead — panel does the same).
3. `call 0x0800C320 (r0 = snd(n)+0x930, r1 = v)`.
4. If `empty`: `call FUN_08012494 (r0 = n, r1 = v)`.

Two halts (both short, no SD). Works on any n, not just the focused sound. Show state from
+0x945 per sound, mask `0x20008C9C`, mode `0x20000454` (2 = looper, magenta SAMPLE LED).

Live caveats:
- Turning the **first** Live Sound on (or the last off) re-points and clears the recorder → any
  pending sample-recorder take / Always-Listening audio is lost (same as the panel).
- `FUN_0803e91c` (folder button, used by `mg_load.py --folder`) calls `FUN_0801b428(n)`, which clears
  the sound's folder/filenames **and its Live flag** before loading. Expected panel behaviour, but note it.
- Hardware check: toggle on an empty and an occupied sound; watch +0x945, mask, 0x20000454, SAMPLE LED
  goes magenta, autosave flag `0x20008C6D` set.

---

## 2. Recorder state

**✅ Hardware-tested 2026-10-22** (`tools/mg_rec.py` `rec_do`, `pico/mgrec.py`; Project27): state
enum, take / fill / size, and every §4 recipe (press, save, assign, discard, grab; looper freeze /
unfreeze / keep loop) behave as below; the save-blink guard is real (~1.2 s).

### Objects

| addr | type | meaning | conf. | evidence |
|---|---|---|---|---|
| `0x200002F8` | obj | audio engine (`this` of audio process `FUN_080181a4`); R = this+0x170 | high | call sites load `0x200002F8` |
| `0x20000468` = **R** | obj | recorder; `FUN_080129a8()` returns it | high | literal |
| R+0x00 `0x20000468` | ptr | ring buffer (stereo s16 words) | high | audio writes `*(R+0)+pos*4` |
| R+0x04 `0x2000046C` | i32 | ring size, frames: **0x177000 = 1 536 000 = 32 s @48k** (sampler) / looper size | high | mode setters |
| R+0x08 `0x20000470` | f32 | threshold, sample recorder (= Settings +0xCC ×0.08) | high | sampler arm compare; THRSH knob reads +0xCC when mode≠2 |
| R+0x0C `0x20000474` | f32 | threshold, looper (= Settings +0xF0 ×0.08) | high | looper auto-freeze compare |
| R+0x10 `0x20000478` | i32 | below-threshold hold before auto-freeze (48000 looper, 0 sampler) | high | |
| R+0x18 `0x20000480` | i32 | fade length (4800 looper, 48 sampler) | medium | |
| R+0x24..27 | u8×4 | input-above-threshold flags (THRSH LED) | low | |
| **R+0x28 `0x20000490`** | i32 | **state** (table below) | high | audio + 5 UI handlers + LED code agree |
| R+0x2C `0x20000494` | i32 | below-threshold counter | medium | |
| R+0x30 `0x20000498` | i32 | write position (frames) | high | |
| R+0x34 `0x2000049C` | i32 | fill = frames in memory (≤ ring size) = Always-Listening / loop content | high | |
| R+0x3C / +0x40 | i32 | trim start offset / trim length (Advanced page) | medium | |
| R+0x54 `0x200004BC` | i32 | take start (ring index) | high | |
| **R+0x58 `0x200004C0`** | i32 | **take length, frames**. Counts up live while recording (= elapsed); ≥ 4800 (0x12C0, 0.1 s) = a take exists | high | |
| R+0x5C | i32 | freeze position | medium | |
| R+0x60 | f32 | fade gain (1.0) | medium | |
| R+0x64 | f32 | normalize target | medium | used in the save normalize pass |
| `0x20000454` | u8 | mode 0/1/2 (see §1) | high | |
| `0x20000458` | i32 | looper size frames: 384000/768000/1152000/1536000 (8/16/24/32 s) | high | `FUN_0800c09c` |
| `0x200004D0 + n*0x10` | — | sample slot n (0-7 sounds, 8 live memory, 9 scratch for Recs-only saves): +0 base ptr, +8 length frames (≠0 = has audio), +0xC offset | high | save path copies take here |
| `0x20008C84` (`st+0x28`) | i32 | save target sound (-1 = Recs only) | high | `FUN_08010bb0` |
| `0x24020B44` | u32 | **save request word**: bit0 = basic save (take), bit1 = trimmed save (Advanced page) | high | set by `FUN_08010bb0`, consumed by UI task |
| `0x24020B5C` (`home+0x14`) | i32 | save-blink countdown (0x80 after a save; −1 per Home render). Must be 0 or SAMPLE/SOUND save is ignored | high | `FUN_08036ad0` |
| `0x20008C5C` (`st+0`) | i32 | engine mode: 0 play, 1 = paused (Advanced Sampling page) | medium | `FUN_08015ea4` |

### State enum (R+0x28)

| val | sample recorder (mode 0/1) | SAMPLE LED | looper (mode 2) | SAMPLE LED |
|---|---|---|---|---|
| 0 | stopped. take ≥4800 → **pending save/assign**; else idle (AL off) | rapid-fade blue / solid dim | **frozen** (take ≥4800 → pending) | solid cyan / rapid-fade blue |
| 1 | restart listening (→3 next sample) | slow fade (blue) | auto-frozen, waiting for threshold | fading magenta |
| 2 | (→3) | slow fade | fade-in to recording | lit magenta |
| 3 | **listening** (Always Listening, ring keeps filling) | slow fade blue | **recording** into loop | lit magenta |
| 4 | stopping (→0) | slow fade | fading out to freeze (→0) | slow fade magenta |
| 5 | **armed**, waiting for threshold (→6 when level ≥ thr; thr 0 = immediately) | fade red | — | — |
| 6 | **recording** (take len counts; →0 at ring size = 32 s auto-stop) | lit red | — | — |
| 7 | stop requested: keeps recording until ≥4800 frames, then →0 | lit red | — | — |

Pending = `state==0 && R+0x58 >= 4800`. Elapsed while recording = `R+0x58 / 48000` s, max `R+0x04`.
LED code: `FUN_08036ad0` (SAMPLE), `FUN_08036890` (SOUND buttons: empty sounds rapid-fade blue when
`take>=4800 && state in {0,6}`).

---

## 3. Panel handlers (callable)

UI pages are C++ objects; current page ptr `0x20008CC0`. Buttons dispatch through std::function
lambdas (`FUN_0802b780` setup) to page vtable slots: **+0x28 press-down, +0x2C click (short release),
+0x30 long press (666 ms for SAMPLE), +0x34 very long (4 s), +0x38 release**; SOUND buttons: +0x14
down, +0x1C click, +0x20 long, +0x24 very long (medium-high: inferred from what each handler does).
Button index (high/medium): 0 SAMPLE, 1 LOAD, 2 SAVE, 3 ?, 4 SCENE A, 5 SCENE B, 6 ALT/EXIT, 7 CLEAR,
8 RAND, 9 X, 10 Y, 11 Z, 12 THRU, 13 LATCH, 14-21 SOUND 1-8.

| fn | page / slot | what it does for recording | conf. |
|---|---|---|---|
| `FUN_08033ab0(home, 0)` | Home +0x2C, SAMPLE click | sampler: pending → save to Recs (`req(0,-1)`, home+0x14=0x80, only if home+0x14==0); state 0/1/3/4 → 5 (arm/start); 5 → 3 (disarm); 6 → 7 (stop). Looper: pending → save; else freeze toggle 0→1, 1/5/6/7→0, 3→4 (+0x5C=pos). Focused SOUND held → Live toggle instead | high |
| `FUN_080331ac(home, 0)` | Home +0x30, SAMPLE long | sampler state 1/3: **Always-Listening grab** (3→4/1→0, take start = pos+R+0x18, take len = fill) → pending. Otherwise (pending/recording, or looper pending) → **enters Advanced Sampling page** (pauses engine). Looper not pending: freeze + grab loop | high |
| `FUN_08034a70(home, n)` | Home +0x14, SOUND n down | if `state in {0,6}` && sound n has no audio && take ≥4800: 6→7, then `req(0, n)` (save + assign) if home+0x14==0. Otherwise normal sound-button behaviour (select / copy / play) | high |
| `FUN_0803240c(clr=0x240451EC, 0)` | Clear page +0x2C, SAMPLE | 1st call arms (clr+8 = 0), 2nd call **discards**: memset R+0x28..+0x63, R+0x60=1.0; if the focused sound is Live also freezes and zeroes the loop buffer | high |
| `FUN_080314a0()` | Clear page leave | if fill < 4800: state 0→1 (restart listening), 1..7→3 | high |
| `FUN_08010bb0(bit, sound)` | helper | `st+0x28 = sound; 0x24020B44 \|= 1<<bit` (IRQ-safe) | high |
| `FUN_0803c7c8(adv=0x24045268, b)` / `FUN_0803c554(adv, n)` | Advanced page click / SOUND | trimmed save `req(1,-1)` / assign `req(1,n)` (2nd press to overwrite an occupied sound), 1 RESAMP, 2 NORM, 3 DIR, 12 THRU, 6 EXIT | high |

### The save itself runs later in the UI task (`FUN_08012fb4`, main loop)

UI task reads+clears `0x24020B44` each tick. bit0: freeze/stop (0/1/5→0, 2/3→4, 6→7), copy
`min(take, fill)` frames from the ring (start R+0x54) into slot `target` (or scratch slot 9),
optional normalize (Settings +0x99), then **`FUN_0801fce8(buf, frames)` writes the WAV synchronously**
(f_open CREATE_NEW, 0x40-byte header 48 kHz stereo s16, data rounded down to 32 B, f_close, f_utime).
On success: for every sound not on /Recs, Recs cursor := newest; for `target` ≥0: folder (+0x59C)=2,
filename (+0x5A0) = `RecNNNNN.wav` via setters, slot length set, default params applied
(`FUN_08012494(n,0)`, or the active Live Sound's params if a Live Sound is focused). Then
take len = 0 and state 0→1 / 1..7→3 (listening again, AL memory restarts).
On failure with SD error state 3: the target's slot length is still set (audio in RAM, no file,
no filename). Other failures: nothing assigned. (The bit1/Advanced path also applies default params
to the target on failure.)

### Rec numbering + list refresh (`FUN_0801fce8`)

- SD state `0x20008CCC`: 3 → return 1 (no save); sets 1 (busy) during; 0 ok, 3 disk error, 2 = list full.
- count = `0x240272DC` (Recs count), ids = `0x30010800` (i32, sorted, negative = abs).
- count == 0x400 (1024) → error 0x12, no save. count 0 → `Rec00001.wav`; else `ids[count-1]+1`
  (cap 99999). `ids[count] = n`, **count++ only on success** — no rescan; the RAM list is updated in place.
- Opens with FA_CREATE_NEW → never overwrites an existing file (if a Rec with that number exists, the
  save fails instead).
- Logs `SD: Saving %s...`, `Done. // rec_ids[%d]=%d`.

---

## 4. Call recipes (GRAINVIEW)

Inject from the idle loop as for `FUN_0803e710`. Before any call: Home page current
(`*0x20008CC0 == 0x24020B48`), SD state `0x20008CCC` ∉ {1, 3}, request word `0x24020B44 == 0`.

| action | guard (read first) | call |
|---|---|---|
| start recording / arm | mode≠2, state ∈ {1,3,4} or (0 and take<4800) | `FUN_08033ab0(0x24020B48, 0)` |
| stop | state 6 | same call |
| cancel arm | state 5 | same call |
| save pending → /Recs | state 0, take ≥4800, `home+0x14 == 0` | same call |
| save + assign to empty sound n | state 0 (or 6), take ≥4800, slot n length == 0, `home+0x14 == 0` | `FUN_08034a70(0x24020B48, n)` |
| Always-Listening grab | mode≠2, **state ∈ {1,3}** (else it opens the Advanced page) | `FUN_080331ac(0x24020B48, 0)` |
| looper freeze/unfreeze | mode==2, not pending | `FUN_08033ab0(0x24020B48, 0)` |
| looper → pending (save loop) | mode==2, not pending | `FUN_080331ac(0x24020B48, 0)` |
| discard pending | pending, focused sound not Live | `FUN_0803240c(0x240451EC, 0)` twice, then `FUN_080314a0()` |

Halt-free alternative (medium; mirrors the handlers' plain stores, same race profile as the
firmware's own UI-vs-audio writes): start = write state 5, stop = write 7, disarm = write 3, looper
freeze = write R+0x5C = R+0x30 then state 4, unfreeze = state 1. Save = write `0x20008C84` (target or
-1) then `0x24020B44 = 1` while it is 0 (+ `home+0x14 = 0x80` for the blink).

Poll for completion: request word back to 0, SD state back to 0, take len 0, Recs count +1.

---

## 5. Risks

- **SD writes:** `FUN_0801fce8` (Rec WAV, CREATE_NEW — cannot overwrite), autosave `FUN_08021bf8`
  (any assign / Live toggle sets the project-changed flag), preset save. Recording never touches
  project/preset files directly.
- **Wrong button index = different action.** Hard-code the argument:
  `FUN_080331ac(home, 1)` loads a preset, `(home, 2)` **saves a preset** (.mgp write);
  `FUN_0803240c(clr, 1)` **loads the Init preset (blank sounds → autosave → project wiped, cf. the
  Preset11 incident)**, 4/5 reset scenes, 8-11 clear mods, 12 clears the quantizer;
  `FUN_08033ab0(home, 12/13)` toggles THRU/LATCH; Home +0x34 handler `FUN_0803298c` with 7/13 does a
  **system reset**. Never call other slots.
- `FUN_080331ac(home,0)` outside the guarded states enters the Advanced Sampling page and **pauses
  playback** (engine mode 1) until EXIT (`FUN_0803c7c8(adv, 6)` or the panel).
- `FUN_08034a70(home,n)` outside the guard runs the normal SOUND-press logic (select / copy-sound if
  another SOUND is held / play).
- If the user is physically holding the focused SOUND button, `FUN_08033ab0(home,0)` toggles Live
  instead of recording.
- **Blocking:** the WAV write runs inside the UI task on the main thread — up to ~6 MB for 32 s. The
  main loop (UI, LEDs, our idle-loop injection point) stalls for the write; audio ISR keeps running.
  Don't halt/inject until SD state returns to 0.
- `home+0x14` save-blink countdown: a second save within ~128 render frames is silently ignored
  (state changes still happen).
- Discard with a Live focused sound wipes the live loop buffer.

## 6. Open questions

- Exact button-slot semantics (+0x2C = click on release?) — inferred, not traced through the button FSM.
- Button 3's panel name.
- Render frame rate (how long home+0x14 = 0x80 lasts).
- Whether Advanced-page saves (bit1) are worth exposing (needs trim UI).

## 7. Hardware checks to do (scratch project)

1. Read R (`0x20000468`, 0x68 bytes) + `0x20000454` at idle: expect state 3, fill growing to 1536000.
2. Panel SAMPLE press/press, long-press, CLEAR+SAMPLE×2+EXIT: watch state 6→7→0 (pending), 4→0, 0→1/3;
   R+0x58 counting while recording; with THRSH set, state 5.
3. RESAMP = looper: states 3 (magenta) / 0 (cyan) / 1 (fading).
4. Live: toggle via §1 recipe on an empty and an occupied sound; check +0x945, mask `0x20008C9C`,
   mode byte, LED magenta, autosave.
5. Calls: start/stop via `FUN_08033ab0(home,0)`; save → `/Multigrain/Recs/RecNNNNN.wav` appears,
   `0x240272DC` +1, `0x30010800[count-1]` = N; assign to an empty sound; discard.
6. Time the main-loop stall during a 32 s save (`mg_pcsample.py`).
