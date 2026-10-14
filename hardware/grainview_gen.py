#!/usr/bin/env python3
"""grainview_gen.py - generate the GRAINVIEW 8HP panel + main PCB (KiCad 10).

One layout table drives both boards, so panel holes always line up with the parts.
Run with KiCad's own Python (it has pcbnew):

    /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 \
        hardware/grainview_gen.py

Writes hardware/grainview_panel.kicad_pcb and hardware/grainview_main.kicad_pcb
(placement + nets; routing comes after the mechanics are confirmed, see docs/HARDWARE.md).
Coordinates are mm from the PANEL's top-left corner, y down, seen from the front.
DRAFT v0.3 (mockup layout, APEM buttons): OLED board size is a placeholder until measured.
"""
import os
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/"
MM = pcbnew.FromMM


def V(x, y):
    return pcbnew.VECTOR2I(MM(x), MM(y))


# ---------------------------------------------------------------- layout --------
HP = 8
PANEL_W, PANEL_H = 40.3, 128.5           # Doepfer A-100: 8HP = 40.3 mm
CX = PANEL_W / 2
MOUNT_HOLES = [(x, y) for x in (7.5, 7.5 + 5 * 5.08) for y in (3.0, PANEL_H - 3.0)]
MOUNT_D = 3.2                            # Doepfer: 7.5 mm in, 3 mm from top/bottom edge

PCB_X0, PCB_X1 = 1.2, PANEL_W - 1.2      # main PCB outline (inside panel width,
PCB_Y0, PCB_Y1 = 11.0, 117.5             # clear of the rails top/bottom)

# Layout = tools/panel_mock.html (the agreed mockup), top to bottom:
#   screen · [BACK | encoder] · [VIEW | FILE] · [SOUND‹ | SOUND›] · [A/B | SETUP]
# The two control columns sit exactly on the Pico's pin rows (CX ± 8.89, Pico on the back,
# below the encoder): each button's legs straddle the Pico row with ~1.4 mm clearance.
COL = (CX - 8.89, CX + 8.89)             # mockup: 12 / 28 mm

# OLED breakout (Adafruit 4741) on a 1x8 socket. Active area 26.7 mm square, top at 12.5 mm
# (mockup). Board size / header position are PLACEHOLDERS until measured.
OLED_ACTIVE = 26.7
OLED_WIN = (CX, 12.5 + OLED_ACTIVE / 2, 28.5, 28.5)   # panel window: cx, cy, w, h
OLED_W, OLED_H = 35.0, 35.0
OLED_HDR_Y = OLED_WIN[1] + OLED_H / 2 - 2.5          # assume header along the bottom edge
OLED_PINS = ["MOSI", "SCK", "DC", "RST", "CS", None, "3V3", "GND"]  # Data Clk DC Rst CS 3Vo VIN GND

ENC = (COL[1], 54.0)                      # encoder shaft centre
ENC_HOLE = 7.5                            # M7 bushing

# Buttons: APEM PHAP5-30VA2K (6x6 THT tact, 7.3 mm, 2.4 mm sq. actuator for caps)
# + APEM U5532 black 4.5 mm round cap (5.5 mm tall) -> cap top ≈ 10.3 mm above the PCB.
BTN_CAP = 4.5
BTN_HOLE = 5.2                            # cap + clearance
# name, x, y, GPIO net, panel legend
BUTTONS = [
    ("BACK",    COL[0], 55.0, "BACK", "BACK"),
    ("VIEW",    COL[0], 75.5, "VIEW", "VIEW"),     # mockup 73: moved clear of the
    ("FILE",    COL[1], 75.5, "FILE", "FILE"),     # Pico W antenna keep-out (y 63-72)
    ("SOUND‹",  COL[0], 92.0, "SOUND_L", "‹"),
    ("SOUND›",  COL[1], 92.0, "SOUND_R", "›"),
    ("A/B",     COL[0], 108.5, "AB", "A/B"),
    ("SETUP",   COL[1], 108.5, "SETUP", "SETUP"),
]

# Pico on the back below the encoder, USB end DOWN (reachable from below the module) and
# the Pico W antenna end up, clear of the button legs.
PICO_USB_Y = 113.26                       # y of pins 1 / 40 (pins 20/21 at 65.0)

# Pico pin number -> net (only the pins we use; see docs/PINMAP.md)
PICO = {
    3: "GND", 8: "GND", 13: "GND", 18: "GND", 23: "GND", 28: "GND", 33: "GND", 38: "GND",
    4: "ENC_A", 5: "ENC_B", 6: "ENC_SW", 7: "GP5",
    9: "BACK", 10: "VIEW", 11: "FILE", 12: "SOUND_L", 14: "SOUND_R", 15: "AB", 16: "SETUP",
    17: "GP13", 19: "SWCLK_P", 20: "SWDIO_P", 21: "GP16", 22: "CS", 24: "SCK", 25: "MOSI",
    26: "DC", 27: "RST", 29: "NRST_P", 31: "VTREF_P", 32: "GP27", 34: "GP28",
    36: "3V3", 39: "VSYS",
}


# ---------------------------------------------------------------- helpers -------
def edge(board, shape, **kw):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(shape)
    s.SetLayer(pcbnew.Edge_Cuts)
    s.SetWidth(MM(0.1))
    if shape == pcbnew.SHAPE_T_RECT:
        s.SetStart(V(*kw["a"]))
        s.SetEnd(V(*kw["b"]))
        if kw.get("r"):
            s.SetCornerRadius(MM(kw["r"]))
    else:
        s.SetCenter(V(*kw["c"]))
        s.SetEnd(V(kw["c"][0] + kw["d"] / 2, kw["c"][1]))
    board.Add(s)


def rect_c(cx, cy, w, h):
    return (cx - w / 2, cy - h / 2), (cx + w / 2, cy + h / 2)


def text(board, s, x, y, h=1.6, layer=pcbnew.F_SilkS, bold=False):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(s)
    t.SetPosition(V(x, y))
    t.SetLayer(layer)
    t.SetTextSize(V(h, h))
    t.SetTextThickness(MM(h * (0.2 if bold else 0.15)))
    board.Add(t)


def footprint(board, lib, name, ref, x, y, rot=0, back=False, value=""):
    fp = pcbnew.FootprintLoad(LIB + lib + ".pretty", name)
    fp.SetReference(ref)
    fp.SetValue(value or name)
    board.Add(fp)
    fp.SetPosition(V(x, y))
    fp.SetOrientationDegrees(rot)
    if back:
        fp.Flip(fp.GetPosition(), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
    return fp


class Nets:
    def __init__(self, board):
        self.board, self.nets = board, {}

    def __call__(self, name):
        if name not in self.nets:
            n = pcbnew.NETINFO_ITEM(self.board, name)
            self.board.Add(n)
            self.nets[name] = n
        return self.nets[name]

    def connect(self, fp, padmap):
        for p in fp.Pads():
            net = padmap.get(p.GetNumber())
            if net:
                p.SetNet(self(net))


def pad_pos(fp, num):
    return next(p for p in fp.Pads() if p.GetNumber() == num).GetPosition()


def orient(fp, a, b, d):
    """Rotate fp so the vector pad a -> pad b points along d ('+x', '-x', '+y', '-y')."""
    for ang in (0, 90, 180, 270):
        fp.SetOrientationDegrees(ang)
        v = pad_pos(fp, b) - pad_pos(fp, a)
        got = ("+x" if v.x > 0 else "-x") if abs(v.x) > abs(v.y) else ("+y" if v.y > 0 else "-y")
        if got == d:
            return
    raise ValueError(f"can't orient {fp.GetReference()}")


def place_at_pad(fp, pad, x, y):
    """Move fp so that its pad `pad` sits at (x, y)."""
    p = next(p for p in fp.Pads() if p.GetNumber() == pad)
    d = fp.GetPosition() - p.GetPosition()
    fp.SetPosition(V(x, y) + d)


# ---------------------------------------------------------------- panel ---------
def panel():
    b = pcbnew.CreateEmptyBoard()
    b.SetCopperLayerCount(2)
    edge(b, pcbnew.SHAPE_T_RECT, a=(0, 0), b=(PANEL_W, PANEL_H))
    for x, y in MOUNT_HOLES:
        edge(b, pcbnew.SHAPE_T_CIRCLE, c=(x, y), d=MOUNT_D)
    cx, cy, w, h = OLED_WIN
    a, c = rect_c(cx, cy, w, h)
    edge(b, pcbnew.SHAPE_T_RECT, a=a, b=c, r=1.0)
    edge(b, pcbnew.SHAPE_T_CIRCLE, c=ENC, d=ENC_HOLE)
    for name, x, y, _, legend in BUTTONS:
        edge(b, pcbnew.SHAPE_T_CIRCLE, c=(x, y), d=BTN_HOLE)
        text(b, legend, x, y + BTN_HOLE / 2 + 2.4, h=1.6, bold=True)
    text(b, "SOUND", CX, 92.0, h=1.5)
    text(b, "GRAINVIEW", CX, 8.0, h=2.4, bold=True)
    text(b, "for MULTIGRAIN", CX, 120.0, h=1.5)
    return b


# ---------------------------------------------------------------- main PCB ------
def main_pcb():
    b = pcbnew.CreateEmptyBoard()
    b.SetCopperLayerCount(2)
    n = Nets(b)
    edge(b, pcbnew.SHAPE_T_RECT, a=(PCB_X0, PCB_Y0), b=(PCB_X1, PCB_Y1), r=1.0)

    # OLED socket (front), centred under the breakout
    j = footprint(b, "Connector_PinSocket_2.54mm", "PinSocket_1x08_P2.54mm_Vertical",
                  "J1", 0, 0, value="OLED 1x8 socket")
    orient(j, "1", "8", "+x")
    place_at_pad(j, "1", CX - 3.5 * 2.54, OLED_HDR_Y)
    n.connect(j, {str(i + 1): s for i, s in enumerate(OLED_PINS) if s})

    # encoder (front), above the Pico
    e = footprint(b, "Rotary_Encoder", "RotaryEncoder_Alps_EC11E-Switch_Vertical_H20mm",
                  "ENC1", 0, 0, value="EC11 push encoder")
    mps = [p.GetPosition() for p in e.Pads() if p.GetNumber() == "MP"]
    mid = (mps[0] + mps[1]) / 2
    e.SetPosition(e.GetPosition() + V(*ENC) - mid)
    n.connect(e, {"A": "ENC_A", "B": "ENC_B", "C": "GND", "S1": "ENC_SW", "S2": "GND"})

    # buttons (front): PHAP5-30 = standard 6 mm tact footprint (legs 6.5 x 4.5 mm); the
    # 6.5 mm pair runs along x so the legs straddle the Pico pin row under each column
    for i, (name, x, y, net, _) in enumerate(BUTTONS):
        s = footprint(b, "Button_Switch_THT", "SW_PUSH_6mm", f"SW{i + 1}", 0, 0,
                      value=f"{name} PHAP5-30VA2K + U5532")
        ps = [p.GetPosition() for p in s.Pads()]
        c = sum(ps[1:], ps[0]) / len(ps)
        s.SetPosition(s.GetPosition() + V(x, y) - c)
        n.connect(s, {"1": net, "2": "GND"})

    # Pico 2 W (back) in 2x 1x20 sockets
    p = footprint(b, "Module", "RaspberryPi_Pico_Common_THT", "U1", 0, 0, back=True,
                  value="Pico 2 W (sockets)")
    orient(p, "20", "1", "+y")             # USB end (pins 1/40) at the bottom
    pads = {q.GetNumber(): q.GetPosition() for q in p.Pads()}
    mid = (pads["1"] + pads["40"]) / 2
    p.SetPosition(p.GetPosition() + V(CX, PICO_USB_Y) - mid)
    n.connect(p, {str(k): v for k, v in PICO.items()})

    # --- back side. Front parts' pins come through, so back parts only go where the
    # front is free: under the raised OLED board (top) and below the buttons (bottom).
    def part(lib, name, ref, pins, a, b_, d, at, value=""):
        f = footprint(b, lib, name, ref, 0, 0, back=True, value=value)
        orient(f, a, b_, d)
        place_at_pad(f, a, *at)
        n.connect(f, pins)
        return f

    R = ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    D = ("Diode_THT", "D_DO-41_SOD81_P7.62mm_Horizontal")

    # all back-side parts sit in the top zone, behind the screen (the Pico fills the rest).
    # Keep bodies above y ≈ 39: the OLED socket's pins come through at y = OLED_HDR_Y.
    part("Connector_IDC", "IDC-Header_2x05_P2.54mm_Vertical", "J2",
         {"1": "M12V", "2": "M12V", "3": "GND", "4": "GND", "5": "GND", "6": "GND",
          "7": "GND", "8": "GND", "9": "P12V_IN", "10": "P12V_IN"},
         "1", "9", "+x", (CX - 5.08, 14.5), value="Eurorack power")
    text(b, "-12V", CX - 7.5, 21.0, h=1.0, layer=pcbnew.B_SilkS)
    part("Connector_PinHeader_1.27mm", "PinHeader_2x05_P1.27mm_Vertical", "J3",
         {"1": "VTREF", "2": "SWDIO", "3": "GND", "4": "SWCLK", "5": "GND", "9": "GND",
          "10": "NRST"}, "1", "9", "+y", (4.2, 13.0), value="SWD to JTRACE")
    part("Connector_PinHeader_2.54mm", "PinHeader_1x06_P2.54mm_Vertical", "J4",
         {"1": "GP5", "2": "GP13", "3": "GP16", "4": "GP27", "5": "GP28", "6": "GND"},
         "1", "6", "+y", (PCB_X1 - 2.4, 12.8), value="spare GPIO")

    # power entry: rack +12 V -> D1 -> regulator -> 5 V -> D2 -> VSYS
    part("Package_TO_SOT_THT", "TO-220-3_Vertical", "U2", {"1": "P12V", "2": "GND", "3": "P5V"},
         "1", "3", "+x", (4.0, 25.5), value="7805 / R-78E5.0 / TSR1-2450")
    part("Capacitor_THT", "CP_Radial_D5.0mm_P2.00mm", "C1", {"1": "P12V", "2": "GND"},
         "1", "2", "+x", (14.5, 25.0), value="10uF 25V")
    part("Capacitor_THT", "CP_Radial_D5.0mm_P2.00mm", "C2", {"1": "P5V", "2": "GND"},
         "1", "2", "+x", (21.0, 25.0), value="10uF 16V")
    part("Capacitor_THT", "C_Disc_D3.0mm_W1.6mm_P2.50mm", "C3", {"1": "VSYS", "2": "GND"},
         "1", "2", "+x", (27.0, 25.0), value="100nF")
    part(*D, "D1", {"1": "P12V", "2": "P12V_IN"}, "2", "1", "+x", (2.8, 31.5),
         value="1N5817 reverse prot.")
    part(*D, "D2", {"1": "VSYS", "2": "P5V"}, "2", "1", "+x", (2.8, 35.0),
         value="1N5817 5V->VSYS")
    for i, (a, c, v) in enumerate([("SWDIO_P", "SWDIO", "47R"), ("SWCLK_P", "SWCLK", "47R"),
                                   ("VTREF_P", "VTREF", "1k"), ("NRST_P", "NRST", "1k DNP")]):
        part(*R, f"R{i + 1}", {"1": c, "2": a}, "1", "2", "+x",
             (14.0 + 11.0 * (i // 2), 31.5 + 3.5 * (i % 2)), value=v)

    text(b, "GRAINVIEW v0.1", CX, 44.0, h=1.2, layer=pcbnew.B_SilkS)
    return b


if __name__ == "__main__":
    for name, fn in [("grainview_panel", panel), ("grainview_main", main_pcb)]:
        path = os.path.join(HERE, name + ".kicad_pcb")
        board = fn()
        board.Save(path)
        print("wrote", path)
