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
    tools/venv/bin/python tools/mg_param.py --sound 1 --scene B --mod X SIZE 0.5
                         # mod depth X -> SIZE (-1..1); sources RAND X Y Z
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
# Mod matrix (per scene): 4 source blocks of 0x48 from scene +0x9c:
# [u32 flag: source has a routing][depth floats, same layout as the params]
MOD_SRC = {"RAND": 0, "X": 1, "Y": 2, "Z": 3}
MOD_FLAG = 0x9C
MOD_VALS = 0xA0
MOD_STRIDE = 0x48
# Panel UI state - lets us keep the knob LEDs in sync with our writes.
# The panel shows LEDs from per-knob "virtual" values (0..1; bipolar v as
# (v+1)/2), loaded on mode entry and moved by the knob; it does not re-read
# the stored values, so we update the virtual value when it's on screen.
UI_PAGE = 0x20008CC0          # u32 current UI page object
PAGE_NORMAL = 0x24020B48
PAGE_MOD = 0x24045210         # RAND/X/Y/Z mode; source (0-3) u32 @ +0x10
EDIT_SCENE = 0x24025B48       # u8 1 = scene B is being edited
VKNOB = {"START": 0x240436B0, "WRAP": 0x240436B4, "SCAN": 0x240436B8,
         "SHAPE": 0x240436BC, "BLUR": 0x240436C0, "LEVEL": 0x240436C4,
         "RATE": 0x240436C8, "SIZE": 0x240436CC, "PITCH": 0x240436D0,
         "TONE": 0x240436D4}
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


def mod_addr(snd, scene, src, name):
    return (SOUND_BASE + snd * SOUND_STRIDE + (SCENE_B if scene == "B" else 0)
            + MOD_VALS + MOD_SRC[src] * MOD_STRIDE + PARAMS[name][0] - PARAMS["START"][0])


def mod_flag_addr(snd, scene, src):
    return (SOUND_BASE + snd * SOUND_STRIDE + (SCENE_B if scene == "B" else 0)
            + MOD_FLAG + MOD_SRC[src] * MOD_STRIDE)


def read_mod(t, snd, scene, src, name):
    return f32(t.read_memory(mod_addr(snd, scene, src, name)))


def write_mod(t, snd, scene, src, name, value):
    t.write_memory(mod_addr(snd, scene, src, name), u32(value))
    # flag = "source has any non-zero depth" (panel sets/clears it the same way)
    flag = mod_flag_addr(snd, scene, src)
    depths = t.read_memory_block32(flag + 4, (MOD_STRIDE - 4) // 4)
    t.write_memory(flag, int(any(d & 0x7FFFFFFF for d in depths)))


def sync_panel(t, snd, scene, name, value, src=None):
    """If the panel currently displays this value, update its virtual knob so
    the LED follows (mode timeouts etc. are fine - we only write when shown)."""
    sel, edit = t.read_memory(CUR_SOUND, 8), t.read_memory(EDIT_SCENE, 8)
    page, psrc = t.read_memory(UI_PAGE), t.read_memory(PAGE_MOD + 0x10)
    shown = ("mod " + list(MOD_SRC)[psrc] if page == PAGE_MOD and psrc < 4 else
             "normal" if page == PAGE_NORMAL else f"page 0x{page:08x}")
    why = (f"  (panel: Sound {sel + 1}, editing scene {'B' if edit else 'A'}, {shown} mode"
           " - not showing this value, LED left alone)")
    if sel != snd or edit != (1 if scene == "B" else 0):
        print(why)
        return False
    if src is None:
        if page != PAGE_NORMAL:
            print(why)
            return False
        bipolar = PARAMS[name][1] < 0
    else:
        if page != PAGE_MOD or psrc != MOD_SRC[src]:
            print(why)
            return False
        bipolar = True
    t.write_memory(VKNOB[name], u32((value + 1) / 2 if bipolar else value))
    return True


def mark_dirty(t):
    """Tell the firmware the project changed so its own autosave persists our
    plain writes (what the knob/select setters do: dirty = autosave-enabled)."""
    from mg_load import write8                       # firmware clears it too
    write8(t, DIRTY, t.read_memory(AUTOSAVE_ON, 8), volatile=True)


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
    for sc in "AB":
        print(f"\nMod depths, scene {sc}:   " + " ".join(f"{n:>6}" for n in PARAMS))
        for src in MOD_SRC:
            vals = [read_mod(t, snd, sc, src, n) for n in PARAMS]
            row = " ".join("     ." if v == 0 else f"{v:+6.2f}" for v in vals)
            print(f"  {src:4} (flag {t.read_memory(mod_flag_addr(snd, sc, src))})  {row}")


def main():
    ap = argparse.ArgumentParser(description="Read/write Scene A/B params (no halt).")
    ap.add_argument("param", nargs="?", type=str.upper, choices=list(PARAMS))
    ap.add_argument("value", nargs="?", type=float)
    ap.add_argument("--sound", type=int, choices=range(1, 9), metavar="1-8")
    ap.add_argument("--scene", type=str.upper, choices=["A", "B"], default="A")
    ap.add_argument("--mod", type=str.upper, choices=list(MOD_SRC),
                    help="write a mod DEPTH (-1..1) for this source instead of the param")
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
        if a.mod:
            old = read_mod(t, snd, a.scene, a.mod, a.param)
            v = min(max(a.value, -1.0), 1.0)
            write_mod(t, snd, a.scene, a.mod, a.param, v)
            print(f"Sound {a.sound} {a.scene} {a.mod}->{a.param}: {old:+.3f} -> "
                  f"{read_mod(t, snd, a.scene, a.mod, a.param):+.3f}")
            if sync_panel(t, snd, a.scene, a.param, v, src=a.mod):
                print(f"  panel is in {a.mod} mode on this sound/scene - LED updated")
            if not a.no_save:
                mark_dirty(t)
                print("  marked project changed - module will autosave it")
            return
        _, lo, hi = PARAMS[a.param]
        clamp = lambda v: min(max(v, lo), hi)  # noqa: E731
        old = read(t, snd, a.scene, a.param)
        if a.wiggle is None:
            write(t, snd, a.scene, a.param, clamp(a.value))
            print(f"Sound {a.sound} {a.scene}.{a.param}: {old:+.3f} -> "
                  f"{read(t, snd, a.scene, a.param):+.3f}")
            if sync_panel(t, snd, a.scene, a.param, clamp(a.value)):
                print("  panel shows this sound/scene - knob LED updated")
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
