#!/usr/bin/env python3
"""Generate a mock Multigrain microSD card tree for developing/testing the
browser without the real hardware. Structure mirrors what the firmware expects:

    <root>/Multigrain/
        Wavs/            user samples
        Recs/            Rec%05d.wav recordings
        Project01/ ...   per-project folders (with their own Wavs + a preset blob)

Audio is synthesized with the stdlib `wave` module (16-bit PCM) so each file has
a visually distinct waveform. Usage:

    python make_mock_card.py /path/to/output_root
"""
import math, os, struct, sys, wave


def write_wav(path, framerate, channels, seconds, gen):
    """gen(t, ch) -> float in [-1, 1]."""
    n = int(framerate * seconds)
    frames = bytearray()
    for i in range(n):
        t = i / framerate
        for ch in range(channels):
            v = max(-1.0, min(1.0, gen(t, ch)))
            frames += struct.pack("<h", int(v * 32767))
    with wave.open(path, "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(framerate)
        w.writeframes(bytes(frames))


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "mock_sd"
    base = os.path.join(root, "Multigrain")
    wavs = os.path.join(base, "Wavs")
    recs = os.path.join(base, "Recs")
    proj = os.path.join(base, "Project01")
    pwavs = os.path.join(proj, "Wavs")
    for d in (wavs, recs, pwavs):
        os.makedirs(d, exist_ok=True)

    # --- /Wavs : varied content, rates, channel counts ---
    write_wav(os.path.join(wavs, "vox.wav"), 44100, 1, 3.2,
              lambda t, c: math.sin(2 * math.pi * 180 * t) * (0.3 + 0.7 * abs(math.sin(2 * math.pi * 1.5 * t))))
    write_wav(os.path.join(wavs, "drum_loop.wav"), 44100, 2, 2.0,
              lambda t, c: (1.0 if (t % 0.5) < 0.02 else 0.0) * math.exp(-((t % 0.5)) * 40) * (1 if c == 0 else 0.6))
    write_wav(os.path.join(wavs, "pad.wav"), 48000, 2, 4.0,
              lambda t, c: 0.5 * (math.sin(2 * math.pi * 110 * t) + math.sin(2 * math.pi * 165 * t + c)) / 2)
    write_wav(os.path.join(wavs, "field.wav"), 22050, 1, 5.0,
              lambda t, c: 0.4 * math.sin(2 * math.pi * (200 + 120 * t) * t))  # chirp

    # --- /Recs : Rec%05d.wav ---
    write_wav(os.path.join(recs, "Rec00001.wav"), 44100, 2, 1.5,
              lambda t, c: 0.6 * math.sin(2 * math.pi * 440 * t) * math.exp(-t * 1.5))
    write_wav(os.path.join(recs, "Rec00002.wav"), 44100, 2, 2.5,
              lambda t, c: 0.5 * (2 * ((t * 220) % 1) - 1))  # sawtooth

    # --- /Project01 : its own sample + an opaque preset blob + a lock file ---
    write_wav(os.path.join(pwavs, "bass.wav"), 44100, 1, 1.0,
              lambda t, c: 0.7 * math.sin(2 * math.pi * 55 * t))
    # Preset stream: from firmware RE the real format starts with version byte
    # 0x11 (=17), then 8 sounds, then trailer. We don't have the exact packed
    # field layout yet (pending diffing a real card), so the body is filler —
    # but the version byte makes the browser recognize the container.
    with open(os.path.join(proj, "preset01.mgp"), "wb") as f:
        f.write(bytes([0x11]) + os.urandom(2048))
    with open(os.path.join(proj, "autosave.mgp"), "wb") as f:
        f.write(bytes([0x11]) + os.urandom(2048))
    with open(os.path.join(proj, ".lock"), "w") as f:
        f.write("A lock file, delete to unlock.\n")

    print(f"Mock card created at: {os.path.abspath(base)}")
    for dirpath, _, files in os.walk(base):
        for fn in sorted(files):
            p = os.path.join(dirpath, fn)
            print(f"  {os.path.relpath(p, root)}  ({os.path.getsize(p)} bytes)")


if __name__ == "__main__":
    main()
