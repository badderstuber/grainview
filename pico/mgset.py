# Settings writes on the Pico, over SWD (swd.py) - a port of tools/mg_set.py's write (spec
# docs/SETTINGS.md): the record's setter done in its two steps - store the value, then call
# its change callback's invoker (checked against mg_map.SETTINGS first) with (&functor,
# &value); no callback (Choke / Gate) = mark the project changed. Type = mgrec.set_live.
#
#   write(s, key, v, n)    v = the catalogue's value (enum index, number, {notes, root});
#                          n = the sound (0-7) for sound settings. ValueError = nothing written
import struct

import mg_map as M
from mgfile import inject, u8
from mgpoll import base

ROWS = {r[1]: r for r in M.SETTINGS}


def addr(row, n):
    if row[3] is not None:
        return row[3]
    if n is None or not 0 <= n < 8:
        raise ValueError("sound must be 1..8")
    return base(n) + row[4]


def encode(row, v):                           # mg_set.encode
    t, nopt, lo, hi = row[2], row[7], row[8], row[9]
    if t in ("bool", "enum"):
        if not isinstance(v, int) or not 0 <= v < nopt:
            raise ValueError("%s must be 0..%d" % (row[1], nopt - 1))
        return bytes((v,))
    if t == "u8":
        v = int(round(float(v)))
        if not lo <= v <= hi:
            raise ValueError("%s must be %s..%s" % (row[1], lo, hi))
        return bytes((v,))
    if t == "f32":
        v = min(max(float(v), lo), hi) / row[12]
        if row[13] is not None:
            v = row[13] / v
        return struct.pack("<f", v)
    if t == "quant":
        notes, root = v.get("notes"), v.get("root")
        if not (isinstance(notes, list) and len(notes) == 12) or root not in range(12):
            raise ValueError("quantizer: 12 notes + root 0..11")
        m = root << 12
        for i in range(12):
            if notes[i]:
                m |= 1 << i
        return struct.pack("<H", m)
    raise ValueError("%s can't be written" % row[1])


def record_ok(s, fn, inv):                    # mg_set.record_ok
    mgr, got = s.read32(fn + 8), s.read32(fn + 0xC)
    if inv:
        return mgr != 0 and got == inv
    return mgr == 0 and got == 0 and M.VTABLES[0] <= s.read32(fn - 4) < M.VTABLES[1]


def write(s, key, v, n=None):
    if key == "type":
        import mgrec
        return mgrec.set_live(s, n, bool(v))
    row = ROWS.get(key)
    if row is None or row[5] is None:
        raise ValueError("%s can't be written" % key)
    a, raw = addr(row, n), encode(row, v)
    fn, inv = a + row[5], row[6]
    if not record_ok(s, fn, inv):
        raise ValueError("%s: record not as expected" % key)
    if row[2] == "f32":                       # the record's own range (value +4 / +8)
        lo, hi = struct.unpack("<ff", s.read_block8(a + 4, 8))
        if not lo <= hi:
            raise ValueError("%s: record range unreadable" % key)
        raw = struct.pack("<f", min(max(struct.unpack("<f", raw)[0], lo), hi))
    if bytes(s.read_block8(a, len(raw))) == raw:
        return                                # (the setter does nothing either)
    sd = s.read32(M.SD_STATE)
    if sd != 0:
        raise ValueError("SD busy" if sd == 1 else "SD error / no card")
    if len(raw) == 4:
        s.write32(a, struct.unpack("<I", raw)[0])
    else:
        for i in range(len(raw)):
            s.write8(a + i, raw[i])
    if inv:
        inject(s, inv, (fn, a))
    else:
        s.write8(M.PROJECT_DIRTY, u8(s, M.STATE + 8))
