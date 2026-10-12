#!/usr/bin/env python3
"""grainview_server.py - backend for the GRAINVIEW emulator (Phase 2 app).

Serves tools/grainview_emulator.html at / plus a small JSON API. Two backends
with the same API, so the UI can't tell them apart:
    --mock   in-memory fake module (no hardware) - for UI work
    default  live module over SWD (ST-Link), built on the hardware-tested
             helpers in mg_param.py / mg_load.py. No halts except WAV load.

API (all JSON):
    GET  /state                 module snapshot (see Backend.snapshot)
    GET  /files                 file list of the SELECTED sound's folder
    POST /select  {"sound":0-7}               edit focus (no halt)
    POST /scene   {"scene":"A"|"B"}           edited scene, as the panel's A/B (no halt)
    POST /play    {}                          playback -> selected sound
    POST /param   {"sound","scene","name","value"}
    POST /mod     {"sound","scene","src","name","value"}
    POST /load    {"index"}                   WAV -> selected sound (one halt)

Usage:
    tools/venv/bin/python tools/grainview_server.py --mock
    tools/venv/bin/python tools/grainview_server.py          # live
Then open http://localhost:8745/
"""
import argparse
import json
import os
import random
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mg_load as L  # noqa: E402
import mg_param as P  # noqa: E402

# Edited scene setter FUN_080114e4(scene) (offline RE 2026-10-12, mirrors the
# sound setter FUN_08011980): if changed { u8 0x24025b48 = scene; notify via
# std::function @ 0x24024b84+0xfb4 (invoker ptr +0xfc0, set at runtime) }; then
# always u8 state+0x30 = 0. set_scene() does the stores without the notify, like
# select_nohalt(). UNTESTED on hardware: check the panel's A/B LEDs + knob LEDs
# follow; if not, read the invoker ptr @ 0x24025b44 and see what it does.
SCENE_FLAG = L.STATE + 0x30

NAMES = list(P.PARAMS)            # START SCAN WRAP SIZE RATE PITCH LEVEL TONE SHAPE BLUR
SRCS = list(P.MOD_SRC)            # RAND X Y Z
FOLDER_NAMES = {0: "project", 1: "Wavs", 2: "Recs"}


class ApiError(Exception):
    pass


def check_args(sound=None, scene=None, name=None, src=None):
    if sound is not None and sound not in range(8):
        raise ApiError("sound must be 0-7")
    if scene is not None and scene not in ("A", "B"):
        raise ApiError("scene must be A or B")
    if name is not None and name not in P.PARAMS:
        raise ApiError(f"unknown param {name!r}")
    if src is not None and src not in P.MOD_SRC:
        raise ApiError(f"unknown mod source {src!r}")


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
        self.files = ["vox.wav", "drum_loop.wav", "pad_long.wav", "field_rec.wav",
                      "bass_sub.wav", "glass_hit.wav", "choir_ah.wav", "noise_fl.wav",
                      "perc_01.wav", "strings.wav", "vinyl.wav", "leo-bangla-stabs.wav"]
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
            self.sounds.append({"folder": 1, "cursor": cur if cur is not None else 0,
                                "file": None if cur is None else self.files[cur],
                                "scenes": scenes, "mod": mod})
        self.lock = threading.Lock()

    def snapshot(self):
        with self.lock:
            m = self.morph
            p = self.sounds[self.playing]["scenes"]
            live = {k: round(p["A"][k] + (p["B"][k] - p["A"][k]) * m, 3) for k in NAMES}
            return {
                "mode": self.mode, "connected": True, "error": None,
                "selected": self.selected, "playing": self.playing,
                "edit_scene": self.edit_scene, "morph": m, "sd_state": self.sd_state, "live": live,
                "sounds": [{"folder": FOLDER_NAMES[s["folder"]], "file": s["file"],
                            "cursor": s["cursor"], "A": dict(s["scenes"]["A"]),
                            "B": dict(s["scenes"]["B"]),
                            "mod": json.loads(json.dumps(s["mod"]))}
                           for s in self.sounds],
            }

    def file_list(self):
        s = self.sounds[self.selected]
        return {"sound": self.selected, "folder": FOLDER_NAMES[s["folder"]],
                "cursor": s["cursor"], "names": list(self.files)}

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

    def set_mod(self, sound, scene, src, name, value):
        check_args(sound, scene, name, src)
        with self.lock:
            self.sounds[sound]["mod"][scene][src][name] = min(max(float(value), -1.0), 1.0)

    def load(self, index):
        with self.lock:
            if not 0 <= index < len(self.files):
                raise ApiError(f"index out of range 0..{len(self.files) - 1}")
            if self.sd_state:
                raise ApiError("SD busy")
            self.sd_state = 1
            snd = self.sounds[self.selected]

        def finish():
            time.sleep(1.2)                  # real loads take ~0.1-1.5 s
            with self.lock:
                snd["cursor"], snd["file"] = index, self.files[index]
                self.sd_state = 0
        threading.Thread(target=finish, daemon=True).start()
        return {"loading": self.files[index]}


# ---- live SWD backend (built on mg_param / mg_load) --------------------------

class SwdBackend:
    """Live module. A poller thread keeps a cached snapshot; actions take the
    same lock (pyOCD isn't thread-safe). Plain RAM reads/writes, no halt -
    except load(), which needs the one-halt firmware call (small audio blip)."""
    mode = "swd"
    BLOCK_LO, BLOCK_HI = 0x48, 0x424     # scene A params .. end of scene B mod matrix

    def __init__(self, freq, hz):
        self.freq, self.period = freq, 1.0 / hz
        self.lock = threading.Lock()
        self.session = None
        self.t = None
        self.snap = {"mode": self.mode, "connected": False, "error": "connecting",
                     "sounds": []}
        threading.Thread(target=self._poll, daemon=True).start()

    def _connect(self):
        try:
            self.session = P.connect(self.freq)
        except SystemExit as e:              # mg_peek.connect exits when no probe
            raise RuntimeError(str(e)) from None
        self.t = self.session.target

    def _poll(self):
        while True:
            try:
                with self.lock:
                    if self.t is None:
                        self._connect()
                    snap = self._read()
                self.snap = snap
                time.sleep(self.period)
            except Exception as ex:          # noqa: BLE001 - surface + retry
                self.snap = {"mode": self.mode, "connected": False, "error": str(ex),
                             "sounds": self.snap.get("sounds", [])}
                with self.lock:
                    if self.session is not None:
                        try:
                            self.session.close()
                        except Exception:    # noqa: BLE001
                            pass
                    self.session = self.t = None
                time.sleep(2.0)

    def _read(self):
        t = self.t
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
            })
        return {
            "mode": self.mode, "connected": True, "error": None,
            "selected": L.u8(t, L.CUR_SOUND), "playing": L.u32(t, L.PLAYING),
            "edit_scene": "B" if L.u8(t, P.EDIT_SCENE) else "A",
            "morph": round(P.f32(t.read_memory(P.LIVE["MORPH"])), 4),
            "sd_state": L.u32(t, L.SD_STATE),
            "live": {k: round(P.f32(t.read_memory(P.LIVE[k])), 4) for k in NAMES},
            "sounds": sounds,
        }

    def _target(self):
        if self.t is None:
            raise ApiError("module not connected")
        return self.t

    def snapshot(self):
        return self.snap

    def file_list(self):
        with self.lock:
            t = self._target()
            snd, folder, count, cursor, _ = L.status(t)
            if folder not in L.FOLDERS:
                raise ApiError(f"unknown source byte {folder}")
            return {"sound": snd, "folder": FOLDER_NAMES[folder], "cursor": cursor,
                    "names": L.file_names(t, folder, count)}

    def select(self, sound):
        check_args(sound=sound)
        with self.lock:
            L.select_nohalt(self._target(), sound)

    def set_scene(self, scene):
        check_args(scene=scene)
        with self.lock:
            t = self._target()
            t.write_memory(P.EDIT_SCENE, 1 if scene == "B" else 0, 8)
            t.write_memory(SCENE_FLAG, 0, 8)

    def play(self):
        with self.lock:
            if not L.post_event_nohalt(self._target(), L.EV_PLAY_SELECTED):
                raise ApiError("engine didn't take the play event - try again")

    def set_param(self, sound, scene, name, value):
        check_args(sound, scene, name)
        with self.lock:
            t, v = self._target(), clamp_param(name, value)
            P.write(t, sound, scene, name, v)
            P.sync_panel(t, sound, scene, name, v)
            P.mark_dirty(t)

    def set_mod(self, sound, scene, src, name, value):
        check_args(sound, scene, name, src)
        with self.lock:
            t, v = self._target(), min(max(float(value), -1.0), 1.0)
            P.write_mod(t, sound, scene, src, name, v)
            P.sync_panel(t, sound, scene, name, v, src=src)
            P.mark_dirty(t)

    def load(self, index):
        """Same one-halt call as mg_load.py; returns once the call is injected.
        The UI watches sd_state / the sound's file in /state for completion."""
        with self.lock:
            t = self._target()
            snd, folder, count, cursor, sd = L.status(t)
            if folder not in L.FOLDERS:
                raise ApiError(f"unknown source byte {folder}")
            if not 0 <= index < count:
                raise ApiError(f"index out of range 0..{count - 1}")
            if sd in (1, 3):
                raise ApiError("SD busy" if sd == 1 else "SD error / no card")
            name = L.file_names(t, folder, count)[index]
            xpsr = L.wait_idle_and_halt(t)
            if xpsr is None:
                raise ApiError("couldn't catch the CPU in the idle loop - nothing called")
            L.call_returning_to_idle(t, xpsr, L.BROWSE_LOAD_FN,
                                     [L.BROWSER_UI, index - cursor])
            return {"loading": name}


# ---- HTTP -------------------------------------------------------------------

def make_handler(be):
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
                self._send(500, {"ok": False, "error": f"{type(e).__name__}: {e}"})

        def do_GET(self):
            path = self.path.split("?", 1)[0]
            if path in ("/", "/index.html"):
                with open(page_path, "rb") as f:
                    self._send(200, f.read(), "text/html; charset=utf-8")
            elif path == "/state":
                self._send(200, be.snapshot())
            elif path == "/files":
                self._run(be.file_list)
            else:
                self._send(404, {"ok": False, "error": "not found"})

        def do_POST(self):
            try:
                n = int(self.headers.get("Content-Length") or 0)
                a = json.loads(self.rfile.read(n) or b"{}")
            except ValueError:
                return self._send(400, {"ok": False, "error": "bad JSON"})
            routes = {
                "/select": lambda: be.select(a.get("sound")),
                "/scene": lambda: be.set_scene(a.get("scene")),
                "/play": be.play,
                "/param": lambda: be.set_param(a.get("sound"), a.get("scene"),
                                               a.get("name"), a.get("value")),
                "/mod": lambda: be.set_mod(a.get("sound"), a.get("scene"), a.get("src"),
                                           a.get("name"), a.get("value")),
                "/load": lambda: be.load(int(a.get("index", -1))),
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
    ap.add_argument("--freq", type=int, default=4_000_000, help="SWD clock Hz")
    a = ap.parse_args()

    be = MockBackend() if a.mock else SwdBackend(a.freq, a.hz)
    httpd = ThreadingHTTPServer(("127.0.0.1", a.port), make_handler(be))
    print(f"GRAINVIEW ({be.mode}): http://localhost:{a.port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopping.")


if __name__ == "__main__":
    main()
