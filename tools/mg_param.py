#!/usr/bin/env python3
"""mg_param.py - read/write the Multigrain's per-sound Scene A/B parameters over
SWD, while it runs (plain RAM access - no halt, no audio glitch).

RE (1.4.8.0, verified live 2026-10-11): each Sound struct (0x24020b84 + n*0x9f0)
holds two scene blocks, A at +0x48.. and B = A + 0x264, same float layout as the
engine's live (morphed) block at 0x200005fc. Writing a stored value is picked up
by the engine within one tick and is not overwritten unless a knob moves.

Usage:
    tools/venv/bin/python tools/mg_param.py                          # all sounds, A/B table
    tools/venv/bin/python tools/mg_param.py --sound 3                # one sound + live values
    tools/venv/bin/python tools/mg_param.py --sound 3 --scene B SIZE 0.75
                         # (also marks the project changed so the module autosaves it;
                         #  --no-save to skip)
    tools/venv/bin/python tools/mg_param.py --sound 3 --scene B SIZE 0.75 --wiggle 0.28
                         # alternate 0.75 / 0.28 every 2 s (listening test), then restore
"""
import argparse
import json
import os
import struct
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from mg_peek import connect  # noqa: E402

SOUND_BASE = 0x24020B84
SOUND_STRIDE = 0x9F0
SCENE_B = 0x264
CUR_SOUND = 0x24025B30
STATE = 0x20008C5C            # engine/UI state block
AUTOSAVE_ON = STATE + 0x08    # u8 autosave enabled
DIRTY = STATE + 0x11          # u8 project-changed flag; UI task saves Autosave.mgp
                              # (FUN_08021bf8) on its next periodic check, then clears it
PLAYING = 0x20008C70
# name: (offset in sound struct for scene A, min, max)
PARAMS = {
    "START": (0x48, 0, 1), "SCAN": (0x4C, -1, 1), "WRAP": (0x50, 0, 1),
    "SIZE": (0x54, 0, 1), "RATE": (0x58, 0, 1), "PITCH": (0x5C, 0, 1),
    "LEVEL": (0x60, 0, 1), "TONE": (0x64, -1, 1), "SHAPE": (0x68, 0, 1),
    "BLUR": (0x80, 0, 1),
}
LIVE = {p["name"]: int(p["addr"], 16) for p in json.load(
    open(os.path.join(os.path.dirname(__file__), "mg_addrs.json")))}


def f32(u):
    return struct.unpack("<f", struct.pack("<I", u))[0]


def u32(x):
    return struct.unpack("<I", struct.pack("<f", x))[0]


def addr(snd, scene, name):
    return (SOUND_BASE + snd * SOUND_STRIDE + PARAMS[name][0]
            + (SCENE_B if scene == "B" else 0))


def read(t, snd, scene, name):
    return f32(t.read_memory(addr(snd, scene, name)))


def write(t, snd, scene, name, value):
    t.write_memory(addr(snd, scene, name), u32(value))


def mark_dirty(t):
    """Tell the firmware the project changed so its own autosave persists our
    plain writes (what the knob/select setters do: dirty = autosave-enabled)."""
    t.write_memory(DIRTY, t.read_memory(AUTOSAVE_ON, 8), 8)


def table(t):
    print("      " + " ".join(f"{n:>6}" for n in PARAMS))
    for snd in range(8):
        for sc in "AB":
            vals = " ".join(f"{read(t, snd, sc, n):+6.2f}" for n in PARAMS)
            print(f"S{snd + 1} {sc}  {vals}")


def one(t, snd):
    sel, play = t.read_memory(CUR_SOUND, 8), t.read_memory(PLAYING)
    print(f"Sound {snd + 1}  (selected {sel + 1}, playing {play + 1}; "
          f"'live' = engine's morphed values for the playing sound)")
    print(f"{'':6} {'A':>7} {'B':>7} {'live':>7}")
    for n in PARAMS:
        print(f"{n:6} {read(t, snd, 'A', n):+7.3f} {read(t, snd, 'B', n):+7.3f} "
              f"{f32(t.read_memory(LIVE[n])):+7.3f}")
    print(f"MORPH {'':15} {f32(t.read_memory(LIVE['MORPH'])):+7.3f}")


def main():
    ap = argparse.ArgumentParser(description="Read/write Scene A/B params (no halt).")
    ap.add_argument("param", nargs="?", type=str.upper, choices=list(PARAMS))
    ap.add_argument("value", nargs="?", type=float)
    ap.add_argument("--sound", type=int, choices=range(1, 9), metavar="1-8")
    ap.add_argument("--scene", type=str.upper, choices=["A", "B"], default="A")
    ap.add_argument("--wiggle", type=float, metavar="OTHER",
                    help="alternate VALUE/OTHER every --period s, then restore")
    ap.add_argument("--period", type=float, default=2.0)
    ap.add_argument("--times", type=int, default=10)
    ap.add_argument("--no-save", action="store_true",
                    help="don't mark the project changed (value lost on power-off)")
    ap.add_argument("--freq", type=int, default=4_000_000)
    a = ap.parse_args()
    if a.value is not None and (a.param is None or a.sound is None):
        ap.error("writing needs --sound N PARAM VALUE")

    session = connect(a.freq)
    try:
        t = session.target
        if a.sound is None:
            table(t)
            return
        snd = a.sound - 1
        if a.value is None:
            one(t, snd)
            return
        _, lo, hi = PARAMS[a.param]
        clamp = lambda v: min(max(v, lo), hi)  # noqa: E731
        old = read(t, snd, a.scene, a.param)
        if a.wiggle is None:
            write(t, snd, a.scene, a.param, clamp(a.value))
            print(f"Sound {a.sound} {a.scene}.{a.param}: {old:+.3f} -> "
                  f"{read(t, snd, a.scene, a.param):+.3f}")
            if not a.no_save:
                mark_dirty(t)
                print("  marked project changed - module will autosave it")
            return
        try:
            for i in range(a.times):
                v = clamp(a.value if i % 2 == 0 else a.wiggle)
                write(t, snd, a.scene, a.param, v)
                print(f"  {i * a.period:5.1f}s  {a.param} = {v:+.3f}", flush=True)
                time.sleep(a.period)
        finally:
            write(t, snd, a.scene, a.param, old)
            print(f"restored {a.param} = {old:+.3f}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
