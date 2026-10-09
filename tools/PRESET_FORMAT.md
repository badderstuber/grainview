# Multigrain preset/project format — reverse-engineering notes

Derived from static analysis of `Multigrain.1.4.8.0.bin` (STM32H753, Cortex-M7)
in Ghidra. Confidence levels are marked. The remaining gaps are best closed by
**diffing real preset files** with single-parameter changes (needs the SD card).

## Method / where this came from

Ghidra headless import (ARM:LE:32:Cortex @ 0x08000000, STM32H7 memory map).
Located the serialization code via strings, then read the decompiled writer /
reader pair:

| Function | Role |
|---|---|
| `FUN_0802120c` | Preset **writer** (serialize to stream) |
| `FUN_08023aec` | Preset **reader** (deserialize; fires param setters on change) |
| `FUN_080207e8` | per-**Sound** writer (called 8×) |
| `FUN_08022d38` | per-Sound reader |
| `FUN_080205a4` | per-**Scene** writer |
| `FUN_080200ec`, `FUN_08020578` | Scene sub-object writers (sizes TBD) |
| `FUN_08007160` | memcpy (optimized) |
| `FUN_0804cb68` | **debug logger** ("Preset version %d") — NOT file content |
| `FUN_08024b00` | project/preset/autosave orchestration (`/Multigrain/Project%02d`) |

## Container (HIGH confidence)

The preset file is a **packed, little-endian serialized byte stream** (not a raw
struct dump). Structure:

```
offset 0:  u8   version = 0x11  (= 17; the "%d" in "Preset version %d")
           Sound[8]             (8 sounds, serialized in order)
           <preset-level trailer fields>   (see below)
```

- No magic bytes and no trailing CRC in the core serializer. The stream begins
  directly with the version byte.
- The in-memory stride of a Sound is `0x9f0` (2544) bytes and a Scene is `0x264`
  (612) bytes, but the FILE is smaller/packed — only the fields each serializer
  actually writes appear on disk, in write order.

### Preset-level trailer (after the 8 sounds)

Fields written (byte unless noted), in order:
`u8@0x4f94, u8@0x4fc4, u8@0x4fac, u16@0x4fd8, u8@0x4ff5, u8@0x500d, u8@0x5024,
u8@0x503d, u8@0x5055, u8@0x506d, u32@0x5080, ...`
(offsets are the in-memory globals; these are global/preset-level settings —
exact meanings TBD by diffing.)

## Sound record (MEDIUM confidence)

Each Sound (`FUN_080207e8`) writes, in order:
```
u8    @+0x14     sound type / flags (sample vs live vs empty — TBD)
Scene @+0x18     Scene A   (via FUN_080205a4)
Scene @+0x27c    Scene B   (via FUN_080205a4)   (0x27c-0x18 = 0x264 apart)
u8    @+0x4f4    ...
<more sound-level fields up to the next sound>
```

## Scene record (MEDIUM confidence — field order known, labels TBD)

Each Scene (`FUN_080205a4`) writes, in order:
```
u8        @+0x14
block     @+0x2c   0x48 (72) bytes, memcpy'd verbatim into the stream
<sub-obj> @+0x2c   via FUN_080200ec   (size TBD)
<sub-obj> @+0x74   via FUN_08020578   (size TBD)
u8        @+0x1b8
u8        @+0x1d0
u8        @+0x1e8
u8        @+0x200
u32/float @+0x218
u32/float @+0x230
u32/float @+0x248
u32/float @+0x260
```
The offsets `0x1b8,0x1d0,0x1e8,0x200,0x218,0x230,0x248,0x260` are a regular
**0x18 (24-byte) stride** → an array of ~8 parameter records. The reader treats
the 4-byte fields as **float**. This is almost certainly the granular parameter
set (START/WRAP/SCAN/SHAPE/LEVEL/TONE/RATE/SIZE/PITCH/BLUR + REVERSE) with per-
parameter modulation, but the offset→name mapping is not yet pinned.

### Reactive parameter model

On load, the reader compares each incoming value to the current one and, if
changed, calls a per-field **setter callback** stored next to the value
(layout ~ `{object*, changed_flag, setter_fn, value}` in consecutive words).
This is how loading a preset re-drives the engine.

## What's left (finish by diffing real files)

1. Exact serialized size of a Scene (resolve `FUN_080200ec` / `FUN_08020578`).
2. offset → parameter-name mapping (START, WRAP, SCAN, SHAPE, LEVEL, TONE,
   RATE, SIZE, PITCH, BLUR, REVERSE, + RAND/X/Y/Z attenuverters).
3. Real preset filename / extension / per-project layout on the card.

**Plan:** on the hardware, save a preset; save a 2nd identical except ONE knob;
binary-diff. The changed byte offset + value delta labels that field directly.
Repeat per parameter. This also validates the container above end-to-end.
