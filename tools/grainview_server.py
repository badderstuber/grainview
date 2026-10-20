#!/usr/bin/env python3
"""grainview_server.py - backend for the GRAINVIEW emulator (Phase 2 app).

Serves tools/grainview_emulator.html at / plus a small JSON API. Two backends
with the same API, so the UI can't tell them apart:
    --mock   in-memory fake module (no hardware) - for UI work
    default  live module over SWD (ST-Link), built on the hardware-tested
             helpers in mg_param.py / mg_load.py. No halts except WAV load.
    --swd pico   the same, through the GRAINVIEW Pico (J3 -> JTRACE) instead of the
             ST-Link: the Pico polls the module itself (pico/mgpoll.py), /state is its
             snapshot; actions drive its SWD master via gv_pico.PicoTarget

API (all JSON):
    GET  /state                 module snapshot (see Backend.snapshot); "firmware" = the
                                module's (checked at connect, mg_load.fw_ok), else not
                                connected with "fw": "checking"|"unknown" (hands off)
    GET  /files[?folder=F]      file list of folder F (project|Wavs|Recs), default
                                the SELECTED sound's folder
    POST /select  {"sound":0-7}               edit focus (no halt)
    POST /scene   {"scene":"A"|"B"}           edited scene, as the panel's A/B (no halt)
    POST /play    {}                          playback -> selected sound
    POST /param   {"sound","scene","name","value"}
    POST /mod     {"sound","scene","src","name","value"}
    POST /preset  {"action":"load"|"save"|"lock","n":0-47}   (one halt; guarded:
                                              load/lock need the file, save not if locked)
    POST /project {"action":"load"|"save","n":0-47}   load = switch (saves the old one
                                              first, one halt); save = Autosave.mgp now (no halt)
    POST /load    {"index"[,"folder"]}        WAV -> selected sound (one halt; another
                                              folder = the sound switches folder, as ALT+folder)

Pico USB screen (breadboard GRAINVIEW, pico/main.py; see gv_pico.py):
    POST /frame   8192 raw bytes, 128x128 4-bit, 2 px/byte (left = high nibble) -> Pico
    GET  /events  server-sent events: {"t":"enc","d":±n} / {"t":"btn","n":"BACK","down":true}
    /state carries "pico": {"connected","port","frames"}. --pico off disables it.

Usage:
    tools/venv/bin/python tools/grainview_server.py --mock
    tools/venv/bin/python tools/grainview_server.py          # live
    tools/venv/bin/python tools/grainview_server.py --swd pico   # live, no ST-Link
Then open http://localhost:8745/
"""
import argparse
import json
import os
import queue
import random
import sys
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mg_load as L  # noqa: E402
import mg_param as P  # noqa: E402
import mg_preset as PR  # noqa: E402

# Edited scene setter FUN_080114e4(scene) (offline RE 2026-10-12, mirrors the
# sound setter FUN_08011980): if changed { u8 0x24025b48 = scene; notify via
# std::function @ 0x24024b84+0xfb4 (invoker ptr +0xfc0, set at runtime) }; then
# always u8 state+0x30 = 0. set_scene() does the stores without the notify, like
# select_nohalt(). UNTESTED on hardware: check the panel's A/B LEDs + knob LEDs
# follow; if not, read the invoker ptr @ 0x24025b44 and see what it does.
SCENE_FLAG = L.STATE + 0x30
# Engine mode flags (offline RE 2026-10-12, FUN_0801a49c fills the engine's
# settings from these each tick). Per-sound = offset in the sound struct.
FLAG_LINK_RS = 0x53D          # u8 per sound: RATE-SIZE link (1 = on)
FLAG_LINK_SP = 0x525          # u8 per sound: SIZE-PITCH link (1 = on)
G_SIZE_MODE = 0x24025DC5      # u8 global: SIZE max-length mode (0 = 4 s default)
G_SYNC = 0x24025BC1           # u8 global: RATE sync to clock (1 = on, if a clock is present)
G_CLOCK_PERIOD = 0x24020834   # f32 global: smoothed clock period, s (clamped 0.05..2)

NAMES = list(P.PARAMS)            # START SCAN WRAP SIZE RATE PITCH LEVEL TONE SHAPE BLUR
SRCS = list(P.MOD_SRC)            # RAND X Y Z
FOLDER_NAMES = {0: "project", 1: "Wavs", 2: "Recs"}
# Settings catalogue (docs/SETTINGS.md): module / preset / sound groups, shared with the emulator.
with open(os.path.join(HERE, "gv_settings.json")) as _f:
    SETTINGS_CAT = {g: v for g, v in json.load(_f).items() if not g.startswith("_")}
FLAG_KEYS = ("link_rs", "link_sp")     # sound settings that are also top-level sound fields
FOLDER_IDX = {v: k for k, v in FOLDER_NAMES.items()}


def slot_arg(n):
    if not isinstance(n, int) or not 0 <= n < PR.SLOTS:
        raise ApiError(f"n must be 0..{PR.SLOTS - 1}")
    return n


def folder_arg(f):
    if f is None or f == "":
        return None
    if f not in FOLDER_IDX:
        raise ApiError(f"folder must be one of {', '.join(FOLDER_IDX)}")
    return FOLDER_IDX[f]


class ApiError(Exception):
    pass


class FirmwareError(RuntimeError):
    """The module runs another firmware than the addresses are for (mg_load.FW_*)."""


def check_args(sound=None, scene=None, name=None, src=None):
    if sound is not None and sound not in range(8):
        raise ApiError("sound must be 0-7")
    if scene is not None and scene not in ("A", "B"):
        raise ApiError("scene must be A or B")
    if name is not None and name not in P.PARAMS:
        raise ApiError(f"unknown param {name!r}")
    if src is not None and src not in P.MOD_SRC:
        raise ApiError(f"unknown mod source {src!r}")


def setting_value(scope, key, value):
    """Validate + normalise a settings write against the catalogue."""
    if scope not in SETTINGS_CAT:
        raise ApiError("scope must be module, preset or sound")
    e = next((e for e in SETTINGS_CAT[scope] if e["key"] == key), None)
    if e is None:
        raise ApiError(f"unknown {scope} setting {key!r}")
    if e["type"] == "info":
        raise ApiError(f"{key} is read-only")
    if e["type"] == "enum":
        if not isinstance(value, int) or not 0 <= value < len(e["options"]):
            raise ApiError(f"{key} must be 0..{len(e['options']) - 1}")
        return value
    if e["type"] == "num":
        v = min(max(float(value), e["min"]), e["max"])
        return round(e["min"] + round((v - e["min"]) / e["step"]) * e["step"], e.get("dp", 3))
    if e["type"] == "quant":
        notes = value.get("notes") if isinstance(value, dict) else None
        if not (isinstance(notes, list) and len(notes) == 12) or value.get("root") not in range(12):
            raise ApiError("quantizer must be {notes: [12 bools], root: 0..11}")
        return {"notes": [bool(n) for n in notes], "root": value["root"]}
    raise ApiError(f"{key}: unsupported type")


# ---- live settings: read-only, from the catalogue's "ram" locations (docs/SETTINGS.md) ----
SETTINGS_EVERY = 1.0                   # s between live settings reads (they rarely change)
RAM_SIZE = {"bool": 1, "enum": 1, "f32": 4, "quant": 2}


def ram_entries():
    return [(g, e) for g in ("module", "preset", "sound") for e in SETTINGS_CAT[g] if "ram" in e]


def ram_addr(e, sound=None, key="off"):
    r = e["ram"]
    if "addr" in r:                     # absolute (module / preset; sound Sync is a preset byte)
        return int(r["addr"], 16)
    return L.SOUND_BASE + sound * L.SOUND_STRIDE + int(r[key], 16)


def ram_decode(e, get, sound=None):
    """Raw RAM -> the catalogue's value; None (UI shows -) if it isn't a value we understand."""
    t, a = e["ram"]["t"], ram_addr(e, sound)
    if t == "bool":
        return 1 if get(a, 1)[0] else 0
    if t == "enum":
        v = get(a, 1)[0]
        return v if v < len(e["options"]) else None
    if t == "f32":
        v = P.f32(int.from_bytes(get(a, 4), "little"))
        if not e["min"] - e["step"] <= v <= e["max"] + e["step"]:
            return None
        return round(min(max(v, e["min"]), e["max"]), e.get("dp", 3))
    if t == "quant":
        mask = int.from_bytes(get(a, 2), "little")
        root = int.from_bytes(get(ram_addr(e, sound, "root"), 4), "little")
        return {"notes": [bool(mask >> i & 1) for i in range(12)], "root": root if root < 12 else 0}
    return None


class SpanReader:
    """Batch scattered small reads into a few block reads."""
    GAP = 48

    def __init__(self, t, wants):
        spans = []
        for a, n in sorted(set(wants)):
            if spans and a <= spans[-1][1] + self.GAP:
                spans[-1][1] = max(spans[-1][1], a + n)
            else:
                spans.append([a, a + n])
        self.blocks = [(lo, bytes(t.read_memory_block8(lo, hi - lo))) for lo, hi in spans]

    def get(self, a, n):
        for lo, b in self.blocks:
            if lo <= a and a + n <= lo + len(b):
                return b[a - lo:a - lo + n]
        raise KeyError(hex(a))


def read_settings(t):
    """{module: {...}, preset: {...}, sounds: [8 x {...}]} from live RAM."""
    want = []
    for g, e in ram_entries():
        for n in range(8) if g == "sound" else [None]:
            want.append((ram_addr(e, n), RAM_SIZE[e["ram"]["t"]]))
            if e["ram"]["t"] == "quant":
                want.append((ram_addr(e, n, "root"), 4))
    rd = SpanReader(t, want)
    out = {"module": {}, "preset": {}, "sounds": [{} for _ in range(8)]}
    for g, e in ram_entries():
        if g == "sound":
            for n in range(8):
                out["sounds"][n][e["key"]] = ram_decode(e, rd.get, n)
        else:
            out[g][e["key"]] = ram_decode(e, rd.get)
    return out


def mock_only(be):
    if be.mode != "mock":
        raise ApiError("mock only")
    return be


def clamp_param(name, v):
    _, lo, hi = P.PARAMS[name]
    return min(max(float(v), lo), hi)


# ---- mock backend -----------------------------------------------------------

class MockBackend:
    """A fake module that behaves like the real one: sounds with files and
    A/B scenes, MORPH at rest, SD loads that take a moment."""
    mode = "mock"

    def __init__(self):
        rnd = random.Random(7)
        self.lists = {0: ["01-kick-loop.wav", "02-pad.wav", "03-vox-chop.wav"],
                      1: ["vox.wav", "drum_loop.wav", "pad_long.wav", "field_rec.wav",
                          "bass_sub.wav", "glass_hit.wav", "choir_ah.wav", "noise_fl.wav",
                          "perc_01.wav", "strings.wav", "vinyl.wav", "leo-bangla-stabs.wav"],
                      2: ["Rec%05d.wav" % n for n in (1, 2, 5)]}
        self.files = self.lists[1]
        self.selected = 0
        self.playing = 0
        self.edit_scene = "A"
        self.sd_state = 0
        self.morph = 0.35               # fader at rest (a real module only moves if you do)
        self.sounds = []
        for n in range(8):
            cur = None if n in (3, 7) else (n * 5) % len(self.files)
            scenes = {}
            for sc in "AB":
                scenes[sc] = {k: round(rnd.uniform(lo, hi), 3)
                              for k, (_, lo, hi) in P.PARAMS.items()}
                scenes[sc]["LEVEL"] = 0.8
            mod = {sc: {s: {k: 0.0 for k in NAMES} for s in SRCS} for sc in "AB"}
            mod["A"]["RAND"]["SIZE"] = 0.4
            mod["B"]["X"]["PITCH"] = -0.25
            settings = {e["key"]: json.loads(json.dumps(e["default"])) for e in SETTINGS_CAT["sound"]
                        if e["key"] not in FLAG_KEYS + ("sync",)}
            self.sounds.append({"folder": 1, "cursors": {0: 0, 1: cur or 0, 2: 2}, "link_rs": 0, "link_sp": 0,
                                "settings": settings,
                                "file": None if cur is None else self.files[cur],
                                "scenes": scenes, "mod": mod})
        self.store = {"project": 0, "projects": [0, 1, 2, 3, 8], "presets": [0, 1, 4],
                      "locked": [1], "preset": 0}
        self.sync = 0
        self.clock_period = 0.5         # fake clock at the SYNC input: 120 BPM
        self.settings = {g: {e["key"]: e["default"] for e in SETTINGS_CAT[g]} for g in ("module", "preset")}
        self.sounds[0]["settings"]["quantizer"] = {     # S1: C major, so the row has something to show
            "notes": [n in (0, 2, 4, 5, 7, 9, 11) for n in range(12)], "root": 0}
        self.lock = threading.Lock()

    def snapshot(self):
        with self.lock:
            m = self.morph
            p = self.sounds[self.playing]["scenes"]
            live = {k: round(p["A"][k] + (p["B"][k] - p["A"][k]) * m, 3) for k in NAMES}
            return {
                "mode": self.mode, "connected": True, "error": None, "firmware": L.FW_VERSION,
                "selected": self.selected, "playing": self.playing,
                "edit_scene": self.edit_scene, "morph": m, "sd_state": self.sd_state, "live": live,
                "sync": self.sync, "clock_period": self.clock_period,
                "settings": json.loads(json.dumps(self.settings)),
                "store": json.loads(json.dumps(self.store)),
                "sounds": [{"folder": FOLDER_NAMES[s["folder"]], "file": s["file"],
                            "cursor": s["cursors"][s["folder"]], "A": dict(s["scenes"]["A"]),
                            "B": dict(s["scenes"]["B"]),
                            "link_rs": s["link_rs"], "link_sp": s["link_sp"],
                            "settings": {**json.loads(json.dumps(s["settings"])), "link_rs": s["link_rs"],
                                         "link_sp": s["link_sp"], "sync": self.sync},
                            "mod": json.loads(json.dumps(s["mod"]))}
                           for s in self.sounds],
            }

    def file_list(self, folder=None):
        s = self.sounds[self.selected]
        f = s["folder"] if folder is None else folder
        return {"sound": self.selected, "folder": FOLDER_NAMES[f],
                "cursor": s["cursors"][f], "names": list(self.lists[f])}

    def select(self, sound):
        check_args(sound=sound)
        with self.lock:
            self.selected = sound

    def set_scene(self, scene):
        check_args(scene=scene)
        with self.lock:
            self.edit_scene = scene

    def play(self):
        with self.lock:
            self.playing = self.selected

    def set_param(self, sound, scene, name, value):
        check_args(sound, scene, name)
        with self.lock:
            self.sounds[sound]["scenes"][scene][name] = clamp_param(name, value)

    def set_setting(self, scope, key, value, sound=None):
        v = setting_value(scope, key, value)
        with self.lock:
            if scope != "sound":
                self.settings[scope][key] = v
                return
            check_args(sound=sound)
            s = self.sounds[sound]
            if key in FLAG_KEYS:
                s[key] = v
            elif key == "sync":          # one global flag in RAM (0x24025bc1), see docs/SETTINGS.md
                self.sync = v
            else:
                s["settings"][key] = v

    def mock_mode(self, sound, link_rs=None, link_sp=None, sync=None):
        """Mock only: the panel's RATE-SIZE / SIZE-PITCH link buttons (per sound)
        and the RATE sync setting - read-only flags on a real module."""
        check_args(sound=sound)
        with self.lock:
            s = self.sounds[sound]
            if link_rs is not None:
                s["link_rs"] = int(bool(link_rs))
            if link_sp is not None:
                s["link_sp"] = int(bool(link_sp))
            if sync is not None:
                self.sync = int(bool(sync))

    def set_mod(self, sound, scene, src, name, value):
        check_args(sound, scene, name, src)
        with self.lock:
            self.sounds[sound]["mod"][scene][src][name] = min(max(float(value), -1.0), 1.0)

    def load(self, index, folder=None):
        with self.lock:
            snd = self.sounds[self.selected]
            f = snd["folder"] if folder is None else folder
            names = self.lists[f]
            if not 0 <= index < len(names):
                raise ApiError(f"index out of range 0..{len(names) - 1}")
            if self.sd_state:
                raise ApiError("SD busy")
            self.sd_state = 1

        def finish():
            time.sleep(1.2)                  # real loads take ~0.1-1.5 s
            with self.lock:
                snd["folder"], snd["cursors"][f], snd["file"] = f, index, names[index]
                self.sd_state = 0
        threading.Thread(target=finish, daemon=True).start()
        return {"loading": names[index]}

    def _sd_job(self, secs, fn):
        with self.lock:
            if self.sd_state:
                raise ApiError("SD busy")
            self.sd_state = 1

        def finish():
            time.sleep(secs)
            with self.lock:
                fn(self.store)
                self.sd_state = 0
        threading.Thread(target=finish, daemon=True).start()

    def preset(self, action, n):
        st = self.store
        n = slot_arg(n)
        if action in ("load", "lock") and n not in st["presets"]:
            raise ApiError(f"Preset{n + 1:02d} doesn't exist")
        if action == "load":
            self._sd_job(1.2, lambda s: s.update(preset=n))
        elif action == "save":
            if n in st["locked"]:
                raise ApiError(f"Preset{n + 1:02d} is locked")
            self._sd_job(0.6, lambda s: s.update(preset=n, presets=sorted(set(s["presets"]) | {n})))
        elif action == "lock":
            self._sd_job(0.2, lambda s: s.update(locked=sorted(set(s["locked"]) ^ {n})))
        else:
            raise ApiError("action must be load, save or lock")

    def project(self, action, n):
        n = slot_arg(n)
        if action == "save":
            self._sd_job(0.4, lambda s: None)
        elif action == "load":
            if n not in self.store["projects"]:
                raise ApiError(f"Project{n + 1:02d} doesn't exist")
            self._sd_job(2.5, lambda s: s.update(project=n, preset=0, presets=[0, 1], locked=[]))
        else:
            raise ApiError("action must be load or save")


# ---- live SWD backend (built on mg_param / mg_load) --------------------------

class SwdBackend:
    """Live module. A poller thread keeps a cached snapshot; actions take the
    same lock (pyOCD isn't thread-safe). Plain RAM reads/writes, no halt -
    except load(), which needs the one-halt firmware call (small audio blip).
    probe = None: ST-Link via pyOCD; a gv_pico.PicoLink: the Pico's SWD master."""
    mode = "swd"
    BLOCK_LO, BLOCK_HI = 0x48, 0x424     # scene A params .. end of scene B mod matrix

    def __init__(self, freq, hz, probe=None):
        self.freq, self.period, self.probe = freq, 1.0 / hz, probe
        self.lock = threading.Lock()
        self.session = None
        self.t = None
        self.snap = {"mode": self.mode, "connected": False, "error": "connecting",
                     "sounds": []}
        self.st, self.st_t = None, 0.0   # live settings cache (read every SETTINGS_EVERY s)
        threading.Thread(target=self._poll, daemon=True).start()

    def _connect(self):
        if self.probe is not None:
            import gv_pico  # noqa: E402 - needs pyserial
            t = gv_pico.PicoTarget(self.probe, self.freq // 1000)
            t.connect()
            self.t = t
            return
        try:
            self.session = P.connect(self.freq)
        except SystemExit as e:              # mg_peek.connect exits when no probe
            raise RuntimeError(str(e)) from None
        self.t = self.session.target
        if not L.fw_ok(self.t):              # every address here is for that build
            raise FirmwareError(f"unknown Multigrain firmware (this is for {L.FW_VERSION})")

    def _poll(self):
        while True:
            try:
                t0 = time.time()
                with self.lock:                  # publish under the lock, so a read that
                    if self.t is None:           # started before an action's write can't
                        self._connect()          # overwrite its _patch() afterwards
                    self.snap = self._read()
                time.sleep(max(0.0, self.period - (time.time() - t0)))
            except Exception as ex:          # noqa: BLE001 - surface + retry
                self.snap = {"mode": self.mode, "connected": False, "error": str(ex),
                             "sounds": self.snap.get("sounds", []),
                             **({"fw": "unknown"} if isinstance(ex, FirmwareError) else {})}
                with self.lock:
                    if self.session is not None:
                        try:
                            self.session.close()
                        except Exception:    # noqa: BLE001
                            pass
                    self.session = self.t = None
                time.sleep(2.0)

    def _read(self):
        if self.probe is None:
            return self._read_from(self.t)
        snap = self.t.snapshot()             # the Pico's own poll
        if not snap.get("connected") and snap.get("fw"):
            return snap                      # firmware being checked / not ours: the Pico
                                             # refuses writes; reconnecting would restart it
        if not snap.get("connected"):
            raise RuntimeError(snap.get("error") or "Pico: no Multigrain")
        return snap

    def _read_from(self, t):
        if self.st is None or time.time() - self.st_t >= SETTINGS_EVERY:
            self.st, self.st_t = read_settings(t), time.time()
        f32 = lambda b, off: P.f32(int.from_bytes(b[off:off + 4], "little"))  # noqa: E731
        sounds = []
        for n in range(8):
            base = L.SOUND_BASE + n * L.SOUND_STRIDE
            blk = bytes(t.read_memory_block8(base + self.BLOCK_LO, self.BLOCK_HI - self.BLOCK_LO))
            rel = lambda off: off - self.BLOCK_LO  # noqa: E731
            scenes, mod = {}, {}
            for sc in "AB":
                sb = P.SCENE_B if sc == "B" else 0
                scenes[sc] = {k: round(f32(blk, rel(o + sb)), 4)
                              for k, (o, _, _) in P.PARAMS.items()}
                mod[sc] = {s: {k: round(f32(blk, rel(sb + P.MOD_VALS + i * P.MOD_STRIDE
                                                     + o - P.PARAMS["START"][0])), 4)
                               for k, (o, _, _) in P.PARAMS.items()}
                           for s, i in P.MOD_SRC.items()}
            folder = L.u8(t, base + L.SRC_OFF)
            known = folder in L.FOLDERS
            sounds.append({
                "folder": FOLDER_NAMES.get(folder), "A": scenes["A"], "B": scenes["B"],
                "mod": mod,
                "file": (L.fname_field(t, n, folder) or None) if known else None,
                "cursor": L.i32(t, L.CURSORS + (folder * 8 + n) * 4) if known else None,
                "link_rs": L.u8(t, base + FLAG_LINK_RS), "link_sp": L.u8(t, base + FLAG_LINK_SP),
            })
            # cached settings, with the per-poll link flags (fresher)
            sounds[-1]["settings"] = {**self.st["sounds"][n], **{k: sounds[-1][k] for k in FLAG_KEYS}}
        sync = L.u8(t, G_SYNC)
        for s in sounds:
            s["settings"]["sync"] = sync
        return {
            "mode": self.mode, "connected": True, "error": None, "firmware": L.FW_VERSION,
            "selected": L.u8(t, L.CUR_SOUND), "playing": L.u32(t, L.PLAYING),
            "edit_scene": "B" if L.u8(t, P.EDIT_SCENE) else "A",
            "morph": round(P.f32(t.read_memory(P.LIVE["MORPH"])), 4),
            "sd_state": L.u32(t, L.SD_STATE),
            "size_mode": L.u8(t, G_SIZE_MODE), "sync": sync,
            "settings": {"module": self.st["module"], "preset": self.st["preset"]},
            "clock_period": round(P.f32(t.read_memory(G_CLOCK_PERIOD)), 5),
            "live": {k: round(P.f32(t.read_memory(P.LIVE[k])), 4) for k in NAMES},
            "store": {k: v for k, v in PR.status(t).items()
                      if k in ("project", "projects", "presets", "locked", "preset")},
            "sounds": sounds,
        }

    def _target(self):
        if self.t is None:
            raise ApiError("module not connected")
        return self.t

    def snapshot(self):
        return self.snap

    def _patch(self, **kw):
        """After a write, show it in /state at once instead of after the next
        poll (else the UI snaps back to the old value for a frame). Lock held."""
        self.snap = {**self.snap, **kw}

    def file_list(self, folder=None):
        with self.lock:
            t = self._target()
            snd, cur, count, cursor, _ = L.status(t)
            if folder is None:
                folder = cur
            if folder not in L.FOLDERS:
                raise ApiError(f"unknown source byte {folder}")
            if folder != cur:
                count = L.folder_count(t, folder)
                cursor = L.i32(t, L.CURSORS + (folder * 8 + snd) * 4)
            return {"sound": snd, "folder": FOLDER_NAMES[folder], "cursor": cursor,
                    "names": L.file_names(t, folder, count)}

    def select(self, sound):
        check_args(sound=sound)
        with self.lock:
            L.select_nohalt(self._target(), sound)
            self._patch(selected=sound)

    def set_scene(self, scene):
        check_args(scene=scene)
        with self.lock:
            t = self._target()
            L.write8(t, P.EDIT_SCENE, 1 if scene == "B" else 0)
            L.write8(t, SCENE_FLAG, 0, volatile=True)
            self._patch(edit_scene=scene)

    def play(self):
        with self.lock:
            if not L.post_event_nohalt(self._target(), L.EV_PLAY_SELECTED):
                raise ApiError("engine didn't take the play event - try again")
            self._patch(playing=L.u32(self.t, L.PLAYING))

    def set_param(self, sound, scene, name, value):
        check_args(sound, scene, name)
        with self.lock:
            t, v = self._target(), clamp_param(name, value)
            P.write(t, sound, scene, name, v)
            P.sync_panel(t, sound, scene, name, v)
            P.mark_dirty(t)

    def set_setting(self, scope, key, value, sound=None):
        setting_value(scope, key, value)
        raise ApiError(f"{key}: live writes not enabled yet (read-only), see docs/SETTINGS.md")

    def set_mod(self, sound, scene, src, name, value):
        check_args(sound, scene, name, src)
        with self.lock:
            t, v = self._target(), min(max(float(value), -1.0), 1.0)
            P.write_mod(t, sound, scene, src, name, v)
            P.sync_panel(t, sound, scene, name, v, src=src)
            P.mark_dirty(t)

    def load(self, index, folder=None):
        """Same one-halt call as mg_load.py; returns once the call is injected.
        The UI watches sd_state / the sound's file in /state for completion.
        Another folder: the sound switches folder (mg_load.load_plan); if it was
        empty, a thread does the cursor fix-up load once the first one's done."""
        with self.lock:
            t = self._target()
            snd, cur, *_ = L.status(t)
            if cur not in L.FOLDERS:
                raise ApiError(f"unknown source byte {cur}")
            try:
                func, args, name, fixup = L.load_plan(t, cur if folder is None else folder, index)
            except ValueError as e:
                raise ApiError(str(e)) from None
            xpsr = L.wait_idle_and_halt(t)
            if xpsr is None:
                raise ApiError("couldn't catch the CPU in the idle loop - nothing called")
            L.call_returning_to_idle(t, xpsr, func, args)
        if fixup:
            def fix():
                with self.lock:
                    try:
                        L.fix_cursor(self.t, snd, folder, index)
                    except Exception:            # noqa: BLE001
                        traceback.print_exc()
            threading.Thread(target=fix, daemon=True).start()
        return {"loading": name}

    def preset(self, action, n):
        n = slot_arg(n)
        fn = {"load": PR.load_preset, "save": PR.save_preset, "lock": PR.toggle_lock}.get(action)
        if fn is None:
            raise ApiError("action must be load, save or lock")
        with self.lock:
            try:
                fn(self._target(), n)
            except ValueError as e:
                raise ApiError(str(e)) from None

    def project(self, action, n):
        with self.lock:
            t = self._target()
            try:
                if action == "save":
                    PR.autosave_now(t)
                elif action == "load":
                    PR.load_project(t, slot_arg(n))
                else:
                    raise ApiError("action must be load or save")
            except ValueError as e:
                raise ApiError(str(e)) from None


# ---- HTTP -------------------------------------------------------------------

STATIC = {
    "/font_compare.html": ("font_compare.html", "text/html; charset=utf-8"),
    "/wave_compare.html": ("wave_compare.html", "text/html; charset=utf-8"),
    "/gv_settings.json": ("gv_settings.json", "application/json"),
    "/fonts/gv_fonts.js": ("fonts/gv_fonts.js", "text/javascript; charset=utf-8"),
    "/gv_draw.js": ("gv_draw.js", "text/javascript; charset=utf-8"),
    "/gv_units.js": ("gv_units.js", "text/javascript; charset=utf-8"),
}


def make_handler(be, pico=None):
    page_path = os.path.join(HERE, "grainview_emulator.html")

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, body, ctype="application/json"):
            if not isinstance(body, bytes):
                body = json.dumps(body).encode()
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _run(self, fn):
            try:
                self._send(200, {"ok": True, **(fn() or {})})
            except ApiError as e:
                self._send(400, {"ok": False, "error": str(e)})
            except Exception as e:           # noqa: BLE001 - report, keep serving
                traceback.print_exc()
                self._send(500, {"ok": False, "error": f"{type(e).__name__}: {e}"})

        def do_GET(self):
            path = self.path.split("?", 1)[0]
            if path in ("/", "/index.html"):
                with open(page_path, "rb") as f:
                    self._send(200, f.read(), "text/html; charset=utf-8")
            elif path in STATIC:                 # same origin = shared calibration
                with open(os.path.join(HERE, STATIC[path][0]), "rb") as f:
                    self._send(200, f.read(), STATIC[path][1])
            elif path == "/state":
                self._send(200, {**be.snapshot(), "pico": pico.status() if pico else None})
            elif path == "/events":
                self._events()
            elif path == "/files":
                q = dict(kv.split("=", 1) for kv in self.path.partition("?")[2].split("&") if "=" in kv)
                self._run(lambda: be.file_list(folder_arg(q.get("folder"))))
            else:
                self._send(404, {"ok": False, "error": "not found"})

        def _events(self):
            """Server-sent events: Pico key presses -> browser. One thread per open page."""
            if pico is None:
                return self._send(404, {"ok": False, "error": "Pico screen disabled"})
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            q = pico.subscribe()
            try:
                while True:
                    try:
                        msg = "data: " + json.dumps(q.get(timeout=15)) + "\n\n"
                    except queue.Empty:
                        msg = ": ping\n\n"          # keepalive; also detects a closed page
                    self.wfile.write(msg.encode())
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                pico.unsubscribe(q)

        def do_POST(self):
            if self.path == "/frame":
                n = int(self.headers.get("Content-Length") or 0)
                data = self.rfile.read(n)
                if pico is None:
                    return self._send(404, {"ok": False, "error": "Pico screen disabled"})
                return self._run(lambda: pico.send_frame(data))
            try:
                n = int(self.headers.get("Content-Length") or 0)
                a = json.loads(self.rfile.read(n) or b"{}")
            except ValueError:
                return self._send(400, {"ok": False, "error": "bad JSON"})
            # every module-touching action, so a misbehaving module can be traced back
            print(time.strftime("%H:%M:%S"), "POST", self.path, json.dumps(a), flush=True)
            routes = {
                "/select": lambda: be.select(a.get("sound")),
                "/scene": lambda: be.set_scene(a.get("scene")),
                "/play": be.play,
                "/param": lambda: be.set_param(a.get("sound"), a.get("scene"),
                                               a.get("name"), a.get("value")),
                "/mod": lambda: be.set_mod(a.get("sound"), a.get("scene"), a.get("src"),
                                           a.get("name"), a.get("value")),
                "/preset": lambda: be.preset(a.get("action"), a.get("n")),
                "/project": lambda: be.project(a.get("action"), a.get("n", 0)),
                "/mock_mode": lambda: mock_only(be).mock_mode(a.get("sound"), a.get("link_rs"),
                                                              a.get("link_sp"), a.get("sync")),
                "/setting": lambda: be.set_setting(a.get("scope"), a.get("key"), a.get("value"),
                                                   a.get("sound")),
                "/load": lambda: be.load(int(a.get("index", -1)), folder_arg(a.get("folder"))),
            }
            fn = routes.get(self.path)
            if fn is None:
                return self._send(404, {"ok": False, "error": "not found"})
            self._run(fn)

    return H


def main():
    ap = argparse.ArgumentParser(description="GRAINVIEW emulator backend.")
    ap.add_argument("--mock", action="store_true", help="fake module, no hardware")
    ap.add_argument("--port", type=int, default=8745)
    ap.add_argument("--hz", type=float, default=5.0, help="SWD poll rate (live)")
    ap.add_argument("--freq", type=int,
                    help="SWD clock Hz (default 4 MHz ST-Link, 8 MHz Pico)")
    ap.add_argument("--swd", choices=["stlink", "pico"], default="stlink",
                    help="live SWD probe: the ST-Link, or the GRAINVIEW Pico (J3 -> JTRACE)")
    ap.add_argument("--pico", default="auto",
                    help="Pico USB screen: auto (find + reconnect), a serial port, or off")
    a = ap.parse_args()

    pico = None
    if a.pico != "off":
        try:
            import gv_pico  # noqa: E402 - needs pyserial, only when the screen is wanted
            pico = gv_pico.PicoLink(None if a.pico == "auto" else a.pico)
        except ImportError as e:
            print(f"Pico screen off ({e}); run with tools/venv/bin/python")
    if a.mock:
        be = MockBackend()
    elif a.swd == "pico":
        if pico is None:
            sys.exit("--swd pico needs the Pico link (not --pico off; tools/venv/bin/python)")
        be = SwdBackend(a.freq or 8_000_000, a.hz, probe=pico)
    else:
        be = SwdBackend(a.freq or 4_000_000, a.hz)
    httpd = ThreadingHTTPServer(("127.0.0.1", a.port), make_handler(be, pico))
    print(f"GRAINVIEW ({be.mode}{' via Pico' if be.mode == 'swd' and a.swd == 'pico' else ''}):"
          f" http://localhost:{a.port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopping.")


if __name__ == "__main__":
    main()
