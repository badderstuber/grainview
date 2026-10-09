#!/usr/bin/env python3
"""mg_mirror.py - live on-screen mirror of the Multigrain's state over SWD.

Polls a set of RAM addresses (discovered with `mg_peek.py --scan`) WITHOUT
halting the core - the Cortex-M7 debug AP reads in the background, so audio keeps
playing - and serves a live web dashboard + a `/state` JSON endpoint that the
companion UI (demo_app.html) can consume.

Address map: tools/mg_addrs.json, a list of parameters:
    [
      {"name":"SIZE",  "addr":"0x24001234", "type":"f32", "min":0,   "max":1},
      {"name":"SHAPE", "addr":"0x24001240", "type":"u8",  "min":0,   "max":6},
      {"name":"PITCH", "addr":"0x24001260", "type":"f32", "min":-24, "max":24}
    ]
  type: u8 i8 u16 i16 u32 i32 f32   (little-endian)
  min/max are only for the on-screen bar; optional.
A starter file with example entries is created automatically if missing.

Usage:
    # Prove the whole pipeline with NO hardware (fake moving values):
    tools/venv/bin/python tools/mg_mirror.py --mock

    # Live, once addresses are known and the ST-Link is attached:
    tools/venv/bin/python tools/mg_mirror.py

Then open http://localhost:8744/  (use --port to change).

Workflow to fill mg_addrs.json: run `mg_peek.py --scan <base> <len>`, move ONE
knob, note the offset it reports, add {"name","addr","type"} here, repeat.
"""
import argparse
import json
import math
import os
import struct
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
ADDRS_PATH = os.path.join(HERE, "mg_addrs.json")

DECODERS = {
    "u8": ("<B", 1), "i8": ("<b", 1),
    "u16": ("<H", 2), "i16": ("<h", 2),
    "u32": ("<I", 4), "i32": ("<i", 4),
    "f32": ("<f", 4),
}

EXAMPLE_ADDRS = [
    {"name": "START", "addr": "0x24000100", "type": "f32", "min": 0, "max": 1},
    {"name": "WRAP",  "addr": "0x24000104", "type": "f32", "min": 0, "max": 1},
    {"name": "SCAN",  "addr": "0x24000108", "type": "f32", "min": -1, "max": 1},
    {"name": "SIZE",  "addr": "0x2400010c", "type": "f32", "min": 0, "max": 1},
    {"name": "RATE",  "addr": "0x24000110", "type": "f32", "min": 0, "max": 130.8},
    {"name": "PITCH", "addr": "0x24000114", "type": "f32", "min": -24, "max": 24},
    {"name": "TONE",  "addr": "0x24000118", "type": "f32", "min": -1, "max": 1},
    {"name": "LEVEL", "addr": "0x2400011c", "type": "f32", "min": 0, "max": 1},
    {"name": "BLUR",  "addr": "0x24000120", "type": "f32", "min": 0, "max": 1},
    {"name": "SHAPE", "addr": "0x24000124", "type": "u8", "min": 0, "max": 6},
    {"name": "MORPH", "addr": "0x24000128", "type": "f32", "min": 0, "max": 1},
]


def parse_addr(s):
    return int(s, 0) if isinstance(s, str) else int(s)


def load_addrs(path):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(EXAMPLE_ADDRS, f, indent=2)
        print(f"Created starter address map: {path}")
        print("(placeholder addresses - replace with real ones from mg_peek.py --scan)")
    with open(path) as f:
        entries = json.load(f)
    for e in entries:
        if e["type"] not in DECODERS:
            raise SystemExit(f"{path}: bad type {e['type']!r} for {e.get('name')}")
        e["_addr"] = parse_addr(e["addr"])
    return entries


class State:
    """Thread-safe snapshot of the latest values."""
    def __init__(self):
        self._lock = threading.Lock()
        self.values = {}       # name -> {"raw","value","ts"}
        self.connected = False
        self.error = None
        self.updated = 0.0

    def set(self, name, raw, value):
        with self._lock:
            self.values[name] = {"raw": raw, "value": value, "ts": time.time()}
            self.updated = time.time()

    def snapshot(self):
        with self._lock:
            return {
                "connected": self.connected,
                "error": self.error,
                "updated": self.updated,
                "values": dict(self.values),
            }


def decode(entry, data):
    fmt, size = DECODERS[entry["type"]]
    return struct.unpack(fmt, data[:size])[0]


# ---- live SWD poller --------------------------------------------------------

def poll_live(entries, state, hz, freq_hz, stop):
    from pyocd.core.helpers import ConnectHelper
    period = 1.0 / hz
    while not stop.is_set():
        session = None
        try:
            session = ConnectHelper.session_with_chosen_probe(
                blocking=False,
                options={
                    "target_override": "cortex_m",
                    "connect_mode": "attach",      # never halt - audio keeps running
                    "frequency": freq_hz,
                    "resume_on_disconnect": False,
                },
            )
            if session is None:
                raise RuntimeError("No ST-Link found")
            session.open()
            target = session.target
            state.connected = True
            state.error = None
            print("SWD attached - mirroring. Ctrl-C to stop.")
            while not stop.is_set():
                t0 = time.time()
                for e in entries:
                    _, size = DECODERS[e["type"]]
                    data = bytes(target.read_memory_block8(e["_addr"], size))
                    val = decode(e, data)
                    state.set(e["name"], data.hex(), val)
                dt = time.time() - t0
                if dt < period:
                    time.sleep(period - dt)
        except Exception as ex:                    # noqa: BLE001 - surface + retry
            state.connected = False
            state.error = str(ex)
            print(f"SWD: {ex} - retrying in 2s")
            time.sleep(2.0)
        finally:
            if session is not None:
                try:
                    session.close()
                except Exception:
                    pass


# ---- mock poller (no hardware) ---------------------------------------------

def poll_mock(entries, state, hz, stop):
    period = 1.0 / hz
    state.connected = True
    state.error = None
    print("MOCK mode - synthesizing moving values (no hardware). Ctrl-C to stop.")
    t0 = time.time()
    while not stop.is_set():
        t = time.time() - t0
        for i, e in enumerate(entries):
            lo = e.get("min", 0.0)
            hi = e.get("max", 1.0)
            phase = i * 0.7
            frac = 0.5 + 0.5 * math.sin(0.4 * t + phase)
            val = lo + frac * (hi - lo)
            if e["type"] in ("u8", "i8", "u16", "i16", "u32", "i32"):
                val = int(round(val))
            else:
                val = round(val, 4)
            fmt, size = DECODERS[e["type"]]
            try:
                raw = struct.pack(fmt, val).hex()
            except struct.error:
                raw = ""
            state.set(e["name"], raw, val)
        time.sleep(period)


# ---- web server -------------------------------------------------------------

def make_handler(state, entries):
    meta = [{"name": e["name"], "type": e["type"],
             "min": e.get("min", 0), "max": e.get("max", 1)} for e in entries]

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, body, ctype):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path.startswith("/state"):
                body = json.dumps(state.snapshot()).encode()
                self._send(200, body, "application/json")
            elif self.path == "/meta":
                self._send(200, json.dumps(meta).encode(), "application/json")
            elif self.path in ("/", "/index.html"):
                self._send(200, PAGE.encode(), "text/html; charset=utf-8")
            else:
                self._send(404, b"not found", "text/plain")

    return H


PAGE = """<!doctype html><html><head><meta charset="utf-8">
<title>Multigrain - live mirror</title>
<style>
 :root{--bg:#0e1113;--card:#171b1f;--fg:#e8edf0;--dim:#8a949c;--accent:#39d98a;}
 body{margin:0;background:var(--bg);color:var(--fg);
   font:14px/1.4 -apple-system,Segoe UI,Roboto,sans-serif;}
 header{padding:14px 18px;display:flex;align-items:center;gap:14px;
   border-bottom:1px solid #232a30;}
 h1{font-size:15px;margin:0;font-weight:600;letter-spacing:.3px;}
 #status{font-size:12px;padding:3px 9px;border-radius:20px;background:#3a2020;color:#ff8a8a;}
 #status.ok{background:#16351f;color:var(--accent);}
 #grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));
   gap:12px;padding:18px;}
 .card{background:var(--card);border:1px solid #232a30;border-radius:10px;padding:12px 14px;}
 .name{font-size:11px;color:var(--dim);letter-spacing:1px;text-transform:uppercase;}
 .val{font-size:22px;font-weight:600;margin:4px 0 8px;font-variant-numeric:tabular-nums;
   transition:color .15s;}
 .val.changed{color:var(--accent);}
 .bar{height:6px;background:#0a0d0f;border-radius:4px;overflow:hidden;}
 .bar>i{display:block;height:100%;background:var(--accent);width:0;transition:width .1s linear;}
 .raw{font-size:10px;color:#565f66;margin-top:6px;font-family:ui-monospace,monospace;}
 footer{padding:10px 18px;color:var(--dim);font-size:11px;border-top:1px solid #232a30;}
</style></head><body>
<header><h1>MULTIGRAIN &middot; live mirror</h1>
 <span id="status">connecting&hellip;</span><span id="age" style="color:var(--dim);font-size:11px"></span>
</header>
<div id="grid"></div>
<footer>SWD background read &middot; no halt &middot; polling <span id="rate"></span></footer>
<script>
let meta=[], cards={}, last={};
async function init(){
  meta = await (await fetch('/meta')).json();
  const g=document.getElementById('grid');
  for(const m of meta){
    const c=document.createElement('div'); c.className='card';
    c.innerHTML=`<div class="name">${m.name}</div>
      <div class="val" id="v-${m.name}">&mdash;</div>
      <div class="bar"><i id="b-${m.name}"></i></div>
      <div class="raw" id="r-${m.name}"></div>`;
    g.appendChild(c); cards[m.name]=m;
  }
  tick();
}
function fmt(v){ return (typeof v==='number' && !Number.isInteger(v))? v.toFixed(3): v; }
async function tick(){
  try{
    const s = await (await fetch('/state')).json();
    const st=document.getElementById('status');
    st.textContent = s.connected? 'live' : (s.error||'waiting');
    st.className = s.connected? 'ok':'';
    document.getElementById('age').textContent =
      s.updated? `updated ${((Date.now()/1000)-s.updated).toFixed(1)}s ago`:'';
    for(const m of meta){
      const d=s.values[m.name]; if(!d) continue;
      const v=d.value, el=document.getElementById('v-'+m.name);
      el.textContent=fmt(v);
      if(last[m.name]!==v){ el.classList.add('changed');
        setTimeout(()=>el.classList.remove('changed'),150); last[m.name]=v; }
      const span=(m.max-m.min)||1, pct=Math.max(0,Math.min(100,100*(v-m.min)/span));
      document.getElementById('b-'+m.name).style.width=pct+'%';
      document.getElementById('r-'+m.name).textContent='0x'+(d.raw||'');
    }
  }catch(e){ document.getElementById('status').textContent='server gone'; }
  setTimeout(tick, 100);
}
init();
</script></body></html>"""


def main():
    ap = argparse.ArgumentParser(description="Live Multigrain state mirror over SWD.")
    ap.add_argument("--mock", action="store_true",
                    help="no hardware; synthesize moving values to test the pipeline")
    ap.add_argument("--addrs", default=ADDRS_PATH, help="address map JSON")
    ap.add_argument("--hz", type=float, default=20.0, help="poll rate (default 20)")
    ap.add_argument("--port", type=int, default=8744, help="web port (default 8744)")
    ap.add_argument("--freq", type=int, default=4_000_000, help="SWD clock Hz")
    args = ap.parse_args()

    entries = load_addrs(args.addrs)
    state = State()
    stop = threading.Event()

    if args.mock:
        worker = threading.Thread(target=poll_mock, args=(entries, state, args.hz, stop),
                                  daemon=True)
    else:
        worker = threading.Thread(target=poll_live,
                                  args=(entries, state, args.hz, args.freq, stop),
                                  daemon=True)
    worker.start()

    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(state, entries))
    print(f"Mirror UI: http://localhost:{args.port}/   ({len(entries)} params @ {args.hz:g} Hz)")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopping.")
    finally:
        stop.set()
        httpd.shutdown()


if __name__ == "__main__":
    main()
