#!/usr/bin/env python3
"""mg_set.py - read / write the module's settings over SWD. Spec: docs/SETTINGS.md.

Every setting is a reactive record: the value (u8 / u16 / f32) plus a std::function change
callback. Its setter (the record's vtable[0], or inlined by the panel code) is always:
    if value != new { value = new; if callback: invoker(&functor, &new) }
and the callbacks only mark Settings.mgs / the project changed (+ Knob mode / Gate delay /
Theme push the value to the panel). The float setter takes its value in s0, which our call
helper doesn't set, so we do the setter's two steps ourselves for every type: store the
value, then call the invoker (checked against the catalogue first) with (&functor, &value).
Choke / Gate have no callback (the panel only stores them): we mark the project changed.
Type (Live Sound) has its own write: mg_rec.set_live. One short halt per write, no SD.

The catalogue (gv_settings.json "ram"): addr / off = the value, t = its type, fn = the
functor relative to the value, inv = the invoker, scale / recip = how the value is shown.

Usage:
    tools/venv/bin/python tools/mg_set.py                        # every setting (read-only)
    tools/venv/bin/python tools/mg_set.py knob_mode 1            # module / preset setting
    tools/venv/bin/python tools/mg_set.py fine_tune -2.5 --sound 3
    tools/venv/bin/python tools/mg_set.py quantizer C,E,G@C --sound 1   # notes @ root
    ... --swd pico                                               # through GRAINVIEW
"""
import argparse
import json
import os
import struct
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mg_load as L  # noqa: E402
import mg_param as P  # noqa: E402

with open(os.path.join(HERE, "gv_settings.json")) as _f:
    CAT = {g: v for g, v in json.load(_f).items() if not g.startswith("_")}
SIZE = {"bool": 1, "enum": 1, "u8": 1, "f32": 4, "quant": 2}
NOTE = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
VTABLES = (0x0805C5C0, 0x0805C740)   # the reactive record classes' vtables (12-byte stride)


def entry(key):
    """-> (group, catalogue entry)."""
    for g, es in CAT.items():
        for e in es:
            if e["key"] == key:
                return g, e
    raise ValueError("unknown setting %r" % key)


def addr(e, sound=None):
    r = e["ram"]
    if "addr" in r:                     # absolute (module / preset; sound Sync is a preset byte)
        return int(r["addr"], 16)
    if sound is None or not 0 <= sound < 8:
        raise ValueError("%s is per sound: sound 0..7" % e["key"])
    return L.SOUND_BASE + sound * L.SOUND_STRIDE + int(r["off"], 16)


def decode(e, raw):
    """Raw bytes -> the catalogue's value; None (UI shows -) if it isn't one we understand."""
    t, r = e["ram"]["t"], e["ram"]
    if t == "bool":
        return 1 if raw[0] else 0
    if t == "enum":
        return raw[0] if raw[0] < len(e["options"]) else None
    if t == "u8":
        v = raw[0]
        return v if e["min"] <= v <= e["max"] else None
    if t == "f32":
        v = struct.unpack("<f", raw[:4])[0]
        if "recip" in r:
            v = r["recip"] / v if v > 0 else float("nan")
        v *= r.get("scale", 1)
        if not e["min"] - e["step"] <= v <= e["max"] + e["step"]:   # (also NaN)
            return None
        return round(min(max(v, e["min"]), e["max"]), e.get("dp", 3))
    if t == "quant":
        m = int.from_bytes(raw[:2], "little")
        root = m >> 12
        return {"notes": [bool(m >> i & 1) for i in range(12)], "root": root if root < 12 else 0}
    return None


def encode(e, v):
    """The catalogue's value (validated) -> raw bytes. Floats: the record's own range is
    applied at write time."""
    t, r = e["ram"]["t"], e["ram"]
    if t in ("bool", "enum"):
        n = len(e["options"])
        if not isinstance(v, int) or not 0 <= v < n:
            raise ValueError("%s must be 0..%d" % (e["key"], n - 1))
        return bytes((v,))
    if t == "u8":
        v = int(round(float(v)))
        if not e["min"] <= v <= e["max"]:
            raise ValueError("%s must be %s..%s" % (e["key"], e["min"], e["max"]))
        return bytes((v,))
    if t == "f32":
        v = min(max(float(v), e["min"]), e["max"]) / r.get("scale", 1)
        if "recip" in r:
            v = r["recip"] / v
        return struct.pack("<f", v)
    if t == "quant":
        notes = v.get("notes") if isinstance(v, dict) else None
        root = v.get("root") if isinstance(v, dict) else None
        if not (isinstance(notes, list) and len(notes) == 12) or root not in range(12):
            raise ValueError("quantizer must be {notes: [12 bools], root: 0..11}")
        m = sum(1 << i for i, x in enumerate(notes) if x) | root << 12
        return struct.pack("<H", m)
    raise ValueError("%s can't be written" % e["key"])


def read(t, key, sound=None):
    _, e = entry(key)
    return decode(e, bytes(t.read_memory_block8(addr(e, sound), SIZE[e["ram"]["t"]])))


def write(t, key, v, sound=None):
    """Set one setting as the panel's setter does. Raises ValueError (nothing written) if the
    value or the record isn't what we expect."""
    g, e = entry(key)
    if key == "type":
        import mg_rec
        return mg_rec.set_live(t, sound, bool(v))
    r = e.get("ram")
    if e["type"] == "info" or not r or "fn" not in r:
        raise ValueError("%s can't be written" % key)
    a, raw = addr(e, sound), encode(e, v)
    fn = a + r["fn"]
    inv = int(r["inv"], 16) if r["inv"] else 0
    if not record_ok(t, fn, inv):
        raise ValueError("%s: record not as expected - nothing written" % key)
    if r["t"] == "f32":                 # the record's own range (+0x1c / +0x20 = value +4 / +8)
        lo, hi = struct.unpack("<ff", bytes(t.read_memory_block8(a + 4, 8)))
        if not lo <= hi:
            raise ValueError("%s: record range unreadable - nothing written" % key)
        raw = struct.pack("<f", min(max(struct.unpack("<f", raw)[0], lo), hi))
    if bytes(t.read_memory_block8(a, len(raw))) == raw:
        return                          # (the setter does nothing either)
    sd = L.u32(t, L.SD_STATE)
    if sd != 0:
        raise ValueError("SD busy" if sd == 1 else "SD error / no card")
    if len(raw) == 1:
        L.write8(t, a, raw[0])
    else:
        t.write_memory_block8(a, list(raw))
    if inv:
        call(t, inv, (fn, a))
    else:
        P.mark_dirty(t)


def record_ok(t, fn, inv):
    """The std::function at fn: manager +8, invoker +0xc. With a callback, the invoker must
    be the catalogue's; without one (inv 0) both are 0 and the record's vtable (fn - 4)
    must be one of the firmware's record classes."""
    mgr, got = L.u32(t, fn + 8), L.u32(t, fn + 0xC)
    if inv:
        return mgr != 0 and got == inv
    return mgr == 0 and got == 0 and VTABLES[0] <= L.u32(t, fn - 4) < VTABLES[1]


def call(t, func, args):
    xpsr = L.wait_idle_and_halt(t)
    if not xpsr:
        raise RuntimeError("couldn't catch the CPU in the idle loop - nothing called")
    L.call_returning_to_idle(t, xpsr, func, args)


def parse(e, s):
    if e["type"] == "quant":                  # C,E,G@C  (or OFF)
        notes, _, root = s.upper().partition("@")
        on = [] if notes in ("", "OFF") else [NOTE.index(n) for n in notes.split(",")]
        return {"notes": [i in on for i in range(12)], "root": NOTE.index(root) if root else 0}
    if e["type"] == "enum":
        o = [x.upper() for x in e["options"]]
        return o.index(s.upper()) if s.upper() in o else int(s)
    return float(s)


def show(e, v):
    if v is None:
        return "-"
    if e["type"] == "enum":
        return e["options"][v]
    if e["type"] == "quant":
        on = [NOTE[i] for i in range(12) if v["notes"][i]]
        return (",".join(on) or "OFF") + " @" + NOTE[v["root"]]
    return e["fmt"].replace("{v}", str(v))


def main():
    ap = argparse.ArgumentParser(description="Module / preset / sound settings over SWD.")
    ap.add_argument("key", nargs="?", help="setting key (gv_settings.json); omit = list all")
    ap.add_argument("value", nargs="?", help="option name / index, number, or C,E,G@C")
    ap.add_argument("--sound", type=int, choices=range(1, 9), metavar="1-8")
    ap.add_argument("--swd", choices=("stlink", "pico"), default="stlink")
    a = ap.parse_args()
    if a.swd == "pico":
        import gv_pico
        link = gv_pico.PicoLink(None, log=lambda *x: None)
        for _ in range(50):
            if link.ser is not None:
                break
            time.sleep(0.1)
        t, session = gv_pico.PicoTarget(link), None
        t.connect()
    else:
        session = L.connect(4_000_000)
        t = session.target
    try:
        if session is not None and not L.fw_ok(t):
            raise SystemExit("not Multigrain %s firmware - hands off" % L.FW_VERSION)
        n = a.sound - 1 if a.sound else None
        if a.key and a.value is not None:
            g, e = entry(a.key)
            if g == "sound" and n is None:
                n = L.u8(t, L.CUR_SOUND)
            write(t, a.key, parse(e, a.value), n)
            time.sleep(0.05)
        for g, es in CAT.items():
            for e in es:
                if a.key and e["key"] != a.key or "ram" not in e:
                    continue
                if g == "sound":
                    for s in [n] if n is not None else range(8):
                        print("%-7s %-12s S%d %s" % (g, e["key"], s + 1, show(e, read(t, e["key"], s))))
                else:
                    print("%-7s %-12s    %s" % (g, e["key"], show(e, read(t, e["key"]))))
    finally:
        if session is not None:
            session.close()


if __name__ == "__main__":
    main()
