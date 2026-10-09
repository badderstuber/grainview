#!/usr/bin/env python3
"""Multigrain microSD browser.

Scans a Multigrain card (the folder that contains `Multigrain/`, or the
`Multigrain/` folder itself), parses every WAV, renders waveform envelopes, and
writes a single self-contained HTML file you can open in any browser. No
dependencies, no server, no network — pure stdlib.

    python sd_browser.py <card_root> [-o out.html]

When your real microSD is mounted, point it at the card, e.g.:
    python sd_browser.py /Volumes/MULTIGRAIN -o card.html
"""
import argparse, html, json, os, struct, sys, wave

COLS = 900  # waveform resolution (envelope columns)


def find_base(root):
    """Return the Multigrain/ dir given a card root or the dir itself."""
    if os.path.basename(os.path.normpath(root)).lower() == "multigrain":
        return root
    cand = os.path.join(root, "Multigrain")
    return cand if os.path.isdir(cand) else root


def wav_info(path):
    """Parse a WAV: metadata + a downmixed min/max envelope of COLS columns."""
    with wave.open(path, "rb") as w:
        ch, sw, fr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        dur = n / fr if fr else 0.0
        full = (1 << (8 * sw - 1)) if sw > 1 else 128
        per_col = max(1, n // COLS)
        env = []  # (min, max) in [-1, 1]
        cmin, cmax, cnt = 1.0, -1.0, 0
        read = 0
        chunk = max(1, per_col)
        while read < n:
            frames = w.readframes(min(chunk, n - read))
            if not frames:
                break
            nf = len(frames) // (sw * ch)
            read += nf
            for i in range(nf):
                # downmix channels to mono
                acc = 0
                off = i * sw * ch
                for c in range(ch):
                    b = frames[off + c * sw: off + c * sw + sw]
                    if sw == 1:
                        s = b[0] - 128
                    elif sw == 2:
                        s = struct.unpack("<h", b)[0]
                    elif sw == 3:
                        s = int.from_bytes(b, "little", signed=True)
                    elif sw == 4:
                        s = struct.unpack("<i", b)[0]
                    else:
                        s = 0
                    acc += s
                v = (acc / ch) / full
                cmin = min(cmin, v)
                cmax = max(cmax, v)
                cnt += 1
                if cnt >= per_col:
                    env.append((cmin, cmax))
                    cmin, cmax, cnt = 1.0, -1.0, 0
        if cnt:
            env.append((cmin, cmax))
    return {"channels": ch, "sampwidth": sw, "framerate": fr, "nframes": n,
            "duration": dur, "env": env, "bits": sw * 8}


PRESET_VERSION = 0x11  # from firmware RE (see PRESET_FORMAT.md): stream byte 0 = version 17


def preset_info(path):
    """Peek at a preset/project stream. Format (from firmware RE): a packed
    little-endian stream starting with a 1-byte version (0x11), then 8 sounds,
    then preset-level fields. Full field decode pending real-file diffing."""
    with open(path, "rb") as f:
        head = f.read(16)
    ver = head[0] if head else None
    hx = " ".join("%02x" % b for b in head)
    return {"version": ver, "recognized": ver == PRESET_VERSION, "hex": hx}


def svg_waveform(env):
    if not env:
        return '<svg class="wf" viewBox="0 0 900 120"></svg>'
    w, h, mid = 900, 120, 60
    step = w / len(env)
    top = " ".join(f"{i*step:.1f},{mid - mx*mid:.1f}" for i, (_, mx) in enumerate(env))
    bot = " ".join(f"{i*step:.1f},{mid - mn*mid:.1f}" for i, (mn, _) in reversed(list(enumerate(env))))
    return (f'<svg class="wf" viewBox="0 0 {w} {h}" preserveAspectRatio="none">'
            f'<line x1="0" y1="{mid}" x2="{w}" y2="{mid}" class="axis"/>'
            f'<polygon class="fill" points="{top} {bot}"/></svg>')


def human(n):
    for unit in ("B", "KB", "MB"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} GB"


def scan(base):
    sections = []
    for name in ("Wavs", "Recs"):
        d = os.path.join(base, name)
        if os.path.isdir(d):
            sections.append((name, d))
    for entry in sorted(os.listdir(base)):
        full = os.path.join(base, entry)
        if os.path.isdir(full) and entry.lower().startswith("project"):
            sections.append((entry, full))
    return sections


def build(base, out):
    items = []  # flat list of dicts for rendering
    tree = []
    for label, d in scan(base):
        files = []
        for fn in sorted(os.listdir(d)):
            fp = os.path.join(d, fn)
            if not os.path.isfile(fp):
                # one level of nesting (e.g. Project01/Wavs)
                if os.path.isdir(fp):
                    for fn2 in sorted(os.listdir(fp)):
                        fp2 = os.path.join(fp, fn2)
                        if os.path.isfile(fp2):
                            files.append((f"{fn}/{fn2}", fp2))
                continue
            files.append((fn, fp))
        rendered = []
        for disp, fp in files:
            size = os.path.getsize(fp)
            ext = os.path.splitext(fp)[1].lower()
            idx = len(items)
            if ext == ".wav":
                try:
                    info = wav_info(fp)
                    meta = (f"{info['framerate']/1000:.1f} kHz · "
                            f"{'mono' if info['channels']==1 else 'stereo' if info['channels']==2 else str(info['channels'])+'ch'} · "
                            f"{info['bits']}-bit · {info['duration']:.2f}s · {human(size)}")
                    body = svg_waveform(info["env"]) + f'<div class="meta">{html.escape(meta)}</div>'
                    kind = "wav"
                except Exception as e:  # malformed / non-PCM
                    body = f'<div class="meta err">Not a readable RIFF/WAVE: {html.escape(str(e))}</div>'
                    kind = "bad"
            elif ext in (".mgp", ".bin", ".dat") or disp.lower().startswith("preset") or disp.lower().startswith("autosave"):
                pi = preset_info(fp)
                if pi["version"] is None:
                    status = "empty file"
                elif pi["recognized"]:
                    status = "✓ recognized Multigrain preset container (version 17)"
                else:
                    status = f'version byte 0x{pi["version"]:02x} ≠ 0x11 — not a recognized preset stream'
                body = (f'<div class="meta">Preset/Project stream · {human(size)}<br>'
                        f'first byte (version) = <code>0x{(pi["version"] or 0):02x}</code> — {html.escape(status)}<br>'
                        f'head: <code>{html.escape(pi["hex"])}</code><br>'
                        f'<span class="note">container cracked (version + 8 sounds + trailer); '
                        f'per-field decode pending diff vs real files — see PRESET_FORMAT.md</span></div>')
                kind = "preset"
            elif disp == ".lock" or disp.endswith(".lock"):
                body = '<div class="meta">🔒 Lock file — delete to unlock this project.</div>'
                kind = "lock"
            else:
                body = f'<div class="meta">{human(size)}</div>'
                kind = "other"
            items.append({"id": f"f{idx}", "disp": disp, "body": body})
            rendered.append({"id": f"f{idx}", "disp": disp, "kind": kind, "size": size})
        tree.append((label, rendered))

    # ---- HTML ----
    dot = {"wav": "●", "preset": "◆", "lock": "🔒", "bad": "⚠", "other": "·"}
    nav = []
    for label, files in tree:
        nav.append(f'<div class="sec">{html.escape(label)} <span class="count">{len(files)}</span></div>')
        for f in files:
            nav.append(f'<a class="row" data-t="{f["id"]}">{dot.get(f["kind"],"·")} '
                       f'{html.escape(f["disp"])}</a>')
    panels = [f'<div class="panel" id="{it["id"]}"><h2>{html.escape(it["disp"])}</h2>{it["body"]}</div>'
              for it in items]
    first = items[0]["id"] if items else ""
    total_wav = sum(1 for _, fs in tree for f in fs if f["kind"] == "wav")

    doc = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Multigrain SD — {html.escape(os.path.abspath(base))}</title>
<style>
:root{{--bg:#fff;--fg:#1b1d21;--mut:#6b7280;--line:#e5e7eb;--accent:#0e9db3;--sel:#e6f6f8;--card:#fafafa}}
@media(prefers-color-scheme:dark){{:root{{--bg:#15171a;--fg:#e8eaed;--mut:#9aa1ab;--line:#2a2e34;--accent:#3fd0e0;--sel:#102a2e;--card:#1b1e22}}}}
*{{box-sizing:border-box}}body{{margin:0;font:14px/1.5 -apple-system,system-ui,Segoe UI,sans-serif;background:var(--bg);color:var(--fg)}}
header{{padding:14px 18px;border-bottom:1px solid var(--line);display:flex;gap:16px;align-items:baseline}}
header b{{font-size:15px}}header .sub{{color:var(--mut);font-size:12px}}
.wrap{{display:flex;height:calc(100vh - 52px)}}
nav{{width:300px;overflow:auto;border-right:1px solid var(--line);padding:8px 0}}
.sec{{padding:10px 16px 4px;font-weight:600;font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut)}}
.sec .count{{float:right;font-weight:400}}
.row{{display:block;padding:5px 16px;cursor:pointer;color:var(--fg);text-decoration:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.row:hover{{background:var(--card)}}.row.on{{background:var(--sel);box-shadow:inset 3px 0 var(--accent)}}
main{{flex:1;overflow:auto;padding:24px 28px}}
.panel{{display:none}}.panel.on{{display:block}}
h2{{margin:0 0 14px;font-size:18px}}
svg.wf{{width:100%;height:150px;background:var(--card);border:1px solid var(--line);border-radius:8px;display:block}}
.wf .fill{{fill:var(--accent);fill-opacity:.85}}.wf .axis{{stroke:var(--line);stroke-width:1}}
.meta{{margin-top:12px;color:var(--mut)}}.meta code{{color:var(--fg);background:var(--card);padding:1px 5px;border-radius:4px}}
.note{{font-style:italic}}.err{{color:#d14343}}
.empty{{color:var(--mut);padding:40px}}
</style></head><body>
<header><b>Multigrain SD Browser</b>
<span class="sub">{html.escape(os.path.abspath(base))} · {total_wav} wav(s)</span></header>
<div class="wrap">
<nav>{''.join(nav) or '<div class="empty">No Multigrain content found.</div>'}</nav>
<main>{''.join(panels) or '<div class="empty">Nothing to show. Is this a Multigrain card?</div>'}</main>
</div>
<script>
const rows=[...document.querySelectorAll('.row')],panels=[...document.querySelectorAll('.panel')];
function sel(id){{rows.forEach(r=>r.classList.toggle('on',r.dataset.t===id));
panels.forEach(p=>p.classList.toggle('on',p.id===id));}}
rows.forEach(r=>r.onclick=()=>sel(r.dataset.t));
if("{first}")sel("{first}");
</script></body></html>"""
    with open(out, "w") as f:
        f.write(doc)
    return total_wav, len(items)


# ---------------------------------------------------------------------------
# Preset diff mode — label the format by comparing two presets that differ by
# one change. See PRESET_FORMAT.md. The file is a packed stream: byte 0 =
# version (0x11), then 8 sounds, then trailer.
# ---------------------------------------------------------------------------
DEFAULT_LABELS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "preset_labels.json")


def load_labels(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (IOError, ValueError):
        return {}


def regions(a, b, merge_gap):
    """Offsets where a,b differ, grouped into regions (merge runs <= merge_gap apart)."""
    n = min(len(a), len(b))
    diffs = [i for i in range(n) if a[i] != b[i]]
    out = []
    for i in diffs:
        if out and i - out[-1][1] <= merge_gap + 1:
            out[-1][1] = i + 1
        else:
            out.append([i, i + 1])
    return [(s, e) for s, e in out], (len(a), len(b))


def decode_region(a, b, s, e):
    """Decode a byte region as the plausible scalar types, old -> new."""
    oa, ob = a[s:e], b[s:e]
    lines = ["  bytes: %s -> %s" % (oa.hex(" "), ob.hex(" "))]
    width = e - s
    if width == 1:
        lines.append("  u8:  %d -> %d   (i8: %d -> %d)" %
                     (oa[0], ob[0], struct.unpack("<b", oa)[0], struct.unpack("<b", ob)[0]))
    elif width == 2:
        lines.append("  u16: %d -> %d   (i16: %d -> %d)" %
                     (struct.unpack("<H", oa)[0], struct.unpack("<H", ob)[0],
                      struct.unpack("<h", oa)[0], struct.unpack("<h", ob)[0]))
    elif width == 4:
        fa, fb = struct.unpack("<f", oa)[0], struct.unpack("<f", ob)[0]
        lines.append("  u32: %d -> %d" % (struct.unpack("<I", oa)[0], struct.unpack("<I", ob)[0]))
        lines.append("  f32: %g -> %g   (delta %g)" % (fa, fb, fb - fa))
    return "\n".join(lines)


def diff_presets(path_a, path_b, labels_path, record_label, merge_gap):
    with open(path_a, "rb") as f:
        a = f.read()
    with open(path_b, "rb") as f:
        b = f.read()
    labels = load_labels(labels_path)
    regs, (la, lb) = regions(a, b, merge_gap)

    print("A: %s (%d bytes)\nB: %s (%d bytes)" % (path_a, la, path_b, lb))
    if la != lb:
        print("! sizes differ by %d bytes (field may be variable-length)" % (lb - la))
    print("version byte: A=0x%02x B=0x%02x%s" %
          (a[0] if a else -1, b[0] if b else -1,
           "  (0x11 = v17 OK)" if a[:1] == b"\x11" else "  (! expected 0x11)"))
    print("\n%d changed region(s) (merge_gap=%d):" % (len(regs), merge_gap))
    for s, e in regs:
        tag = "  <- version" if s == 0 else ("  [%s]" % labels[str(s)] if str(s) in labels else "")
        print("\noffset 0x%04x (%d)  width %d%s" % (s, s, e - s, tag))
        print(decode_region(a, b, s, e))

    if record_label:
        if len(regs) != 1:
            print("\n! --label needs exactly ONE changed region, found %d. "
                  "Change only one parameter between saves." % len(regs))
            return
        s, e = regs[0]
        labels[str(s)] = record_label
        with open(labels_path, "w") as f:
            json.dump(labels, f, indent=2, sort_keys=True)
        print("\nlabeled offset 0x%04x (width %d) = %r  -> %s" %
              (s, e - s, record_label, labels_path))


def main():
    ap = argparse.ArgumentParser(description="Multigrain microSD browser + preset diff tool")
    ap.add_argument("root", nargs="?", help="card root, or the Multigrain/ folder (browse mode)")
    ap.add_argument("-o", "--out", default="multigrain_card.html")
    ap.add_argument("--diff", nargs=2, metavar=("PRESET_A", "PRESET_B"),
                    help="compare two preset files and report changed offsets")
    ap.add_argument("--label", metavar="NAME",
                    help="with --diff: record the single changed offset as NAME in the labels file")
    ap.add_argument("--labels", default=DEFAULT_LABELS, help="labels JSON path")
    ap.add_argument("--merge-gap", type=int, default=2,
                    help="merge changed bytes within N of each other into one region (default 2)")
    args = ap.parse_args()

    if args.diff:
        diff_presets(args.diff[0], args.diff[1], args.labels, args.label, args.merge_gap)
        return

    if not args.root:
        ap.error("give a card root to browse, or --diff A B to compare presets")
    base = find_base(args.root)
    if not os.path.isdir(base):
        print(f"Not a directory: {base}", file=sys.stderr)
        sys.exit(1)
    nwav, nitems = build(base, args.out)
    print(f"Scanned {base}\n  {nwav} wav(s), {nitems} item(s)\n  -> {os.path.abspath(args.out)}")


if __name__ == "__main__":
    main()
