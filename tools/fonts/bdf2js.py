"""bdf2js.py OUT.js FONT.bdf... - pack BDF bitmap fonts into one JS file for the
GRAINVIEW emulator: GV_FONTS[name] = {ascent, descent, copyright, g: {code: [dw, w, h, xo, yo, "hexrows"]}}.
Keeps ASCII 32-126 plus a few UI symbols."""
import json
import os
import sys

KEEP = set(range(32, 127)) | {0xB7, 0x2026, 0x2192, 0x2039, 0x203A, 0x25B8, 0x25C2, 0x2022}


def parse(path):
    text = open(path, "rb").read().decode("latin-1").replace("\r", "")
    font = {"ascent": None, "descent": None, "copyright": "", "g": {}}
    cur, bitmap = None, None
    for line in text.split("\n"):
        k, _, v = line.strip().partition(" ")
        if bitmap is not None:
            if k == "ENDCHAR":
                if cur["enc"] in KEEP and "bbx" in cur:
                    w, h, xo, yo = cur["bbx"]
                    font["g"][cur["enc"]] = [cur["dw"], w, h, xo, yo, "".join(bitmap)]
                cur, bitmap = None, None
            else:
                bitmap.append(k.lower())
            continue
        if k == "FONT_ASCENT":
            font["ascent"] = int(v)
        elif k == "FONT_DESCENT":
            font["descent"] = int(v)
        elif k == "COPYRIGHT" and not font["copyright"]:
            font["copyright"] = v.strip('"')
        elif k == "STARTCHAR":
            cur = {"enc": -1, "dw": 0}
        elif k == "ENCODING" and cur is not None:
            cur["enc"] = int(v.split()[0])
        elif k == "DWIDTH" and cur is not None:
            cur["dw"] = int(v.split()[0])
        elif k == "BBX" and cur is not None:
            cur["bbx"] = [int(x) for x in v.split()]
        elif k == "BITMAP" and cur is not None:
            bitmap = []
    return font


def main():
    out, paths = sys.argv[1], sys.argv[2:]
    fonts = {}
    for p in paths:
        f = parse(p)
        name = os.path.basename(p)[:-4]
        if f["ascent"] is None:          # derive from glyphs if missing
            f["ascent"] = max(g[2] + g[4] for g in f["g"].values())
            f["descent"] = max(0, -min(g[4] for g in f["g"].values()))
        cap = f["g"].get(ord("H"))       # cap height = lit rows of 'H' above baseline
        if cap:
            dw, w, h, xo, yo, hexrows = cap
            rl = len(hexrows) // h if h else 0
            lit = [i for i in range(h) if int(hexrows[i * rl:(i + 1) * rl] or "0", 16)]
            f["cap"] = (h + yo) - lit[0] if lit else None
        else:
            f["cap"] = None
        fonts[name] = f
        print(f"{name:26} asc {f['ascent']:2} desc {f['descent']:2} cap {f['cap']} glyphs {len(f['g'])}")
    with open(out, "w") as fh:
        fh.write("// Generated from u8g2 BDF fonts (github.com/olikraus/u8g2, tools/font/bdf).\n"
                 "// Each font keeps its own licence - see the copyright field.\n")
        fh.write("const GV_FONTS=" + json.dumps(fonts, separators=(",", ":")) + ";\n")


if __name__ == "__main__":
    main()
