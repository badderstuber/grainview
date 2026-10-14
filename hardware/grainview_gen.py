#!/usr/bin/env python3
"""grainview_gen.py - generate the GRAINVIEW 8HP panel + its two PCBs (KiCad 10).

One layout table drives all three boards, so panel holes and board-to-board headers always
line up. Stack, front to back: panel · CONTROL board (OLED, encoder, buttons on its front) ·
MAIN board (Pico in sockets + power + SWD on its back). The two PCBs are joined by two 1x12
2.54 mm strips down the long edges, outside the button columns (female on the control board's
back, male on the main board's front: 8.5 + 2.5 = 11 mm apart).
Run with KiCad's own Python (it has pcbnew):

    /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 \
        hardware/grainview_gen.py

Writes hardware/grainview_{panel,control,main}.kicad_pcb
(placement + nets; then hardware/grainview_route.py routes the two PCBs. Re-running this
script wipes the routing).
Coordinates are mm from the PANEL's top-left corner, y down, seen from the front.
DRAFT v0.5: two PCBs, because the Pico's socket solder joints would sit under the buttons.
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

PCB_X0, PCB_X1 = 1.2, PANEL_W - 1.2      # both PCB outlines (inside panel width,
PCB_Y0, PCB_Y1 = 10.5, 118.5             # inside the 108 mm zone between the rails)

# Layout = tools/panel_mock.html (the agreed mockup), top to bottom:
#   screen · [BACK | encoder] · [VIEW | FILE] · [SOUND‹ | SOUND›] · [A/B | SETUP]
COL = (CX - 8.89, CX + 8.89)             # mockup: 12 / 28 mm

# OLED breakout, Adafruit 4741, from Adafruit's own board file
# (github.com/adafruit/Adafruit-Grayscale-1.5-inch-128x128-OLED-PCB), seen from the glass side:
# 35.56 x 41.91 mm body + two 5.08 mm tabs at the bottom corners (47 mm overall), header
# along the TOP edge, 2.5 mm holes 2.54 mm in from the corners (the bottom pair on the tabs).
# It sits on the front of the control PCB, its own male header soldered straight into J1.
OLED_T = 10.0                             # board top edge (rail zone ends at 10 mm)
OLED_BW, OLED_BH, OLED_TAB = 35.56, 41.91, 5.08
OLED_X0 = CX - OLED_BW / 2
OLED_HDR = (OLED_X0 + 8.89, OLED_T + 2.54)           # pin 1 ("Data"), pins run +x
# Support: the soldered header at the top + an M2.5 nylon standoff under the bottom-LEFT tab.
# The bottom-RIGHT tab (below the GND end of the header) is CUT OFF so the encoder can sit in
# the right button column (it only carries a mounting hole + GND pour, no signals; checked in
# Adafruit's file); that corner rests on a 3 mm foam pad.
OLED_HOLES = [(OLED_X0 + 2.54, OLED_T + 44.45)]
OLED_ACTIVE = 26.855                      # 128 x 0.21 mm
OLED_AC = (OLED_X0 + 17.653, OLED_T + 20.416)        # active-area centre
OLED_WIN = (*OLED_AC, 29.4, 29.4)         # panel window: cx, cy, w, h (active + 1.27/side)
OLED_PINS = ["MOSI", "SCK", "DC", "RST", "CS", None, "3V3", "GND"]  # Data Clk DC Rst CS 3Vo VIN GND
# parts on the breakout's back (facing our PCB): keep our THT leads out from under these.
# The STEMMA QT (JST SH) connectors stand ~3 mm (Leo) > the 2.5 mm header plastic, so the
# control PCB gets an edge notch under each one (STEMMA_NOTCH) and the OLED still sits on its header.
STEMMA = [(OLED_X0, OLED_T + 19.25, OLED_X0 + 5.6, OLED_T + 27.75),
          (OLED_X0 + OLED_BW - 5.6, OLED_T + 19.25, OLED_X0 + OLED_BW, OLED_T + 27.75)]
STEMMA_NOTCH = 0.4                        # clearance around each connector
OLED_TALL = [("STEMMA QT", *STEMMA[0]), ("STEMMA QT", *STEMMA[1]),
             ("L1", OLED_X0 + 14.9, OLED_T + 23.0, OLED_X0 + 20.7, OLED_T + 26.3)]

# All four rows on a 16 mm pitch (62 / 78 / 94 / 110); the window's bottom edge is ~17 mm above
# the top row. The encoder sits in the right column where the OLED's cut-off tab was (at 62 its
# body would still overlap that tab by ~0.9 mm).
ROW1 = 62.0
ENC = (COL[1], ROW1)                      # shaft centre
ENC_HOLE = 7.5                            # M7 bushing

# Buttons: APEM PHAP5-30VA2K (6x6 THT tact, 7.3 mm, 2.4 mm sq. actuator for caps)
# + APEM U5532 black 4.5 mm round cap (5.5 mm tall) -> cap top ≈ 10.3 mm above the PCB.
BTN_CAP = 4.5
BTN_HOLE = 5.2                            # cap + clearance
# name, x, y, GPIO net, panel legend
BUTTONS = [
    ("BACK",    COL[0], ROW1, "BACK", "BACK"),
    ("VIEW",    COL[0], 78.0, "VIEW", "VIEW"),
    ("FILE",    COL[1], 78.0, "FILE", "FILE"),
    ("SOUND‹",  COL[0], 94.0, "SOUND_L", "‹"),
    ("SOUND›",  COL[1], 94.0, "SOUND_R", "›"),
    ("A/B",     COL[0], 110.0, "AB", "A/B"),
    ("SETUP",   COL[1], 110.0, "SETUP", "SETUP"),
]

# Pico on the MAIN board's back, USB end DOWN (reachable from below the module), antenna end
# up, as low as the rail zone allows (USB plug edge ≈ 118.2). Pins 1-20 on the left (x 11.26).
PICO_USB_Y = 115.5                        # y of pins 1 / 40 (pins 20/21 at 67.24)
PICO_KEEPOUT = (CX - 7.1, PICO_USB_Y - 48.26 - 1.87, CX + 7.1, PICO_USB_Y - 48.26 + 7.13)

# Board-to-board strips (control J5/J6 female on its back <-> main J5/J6 male on its front),
# pin 1 at the top. Left = Pico pins 1-20 side (buttons, encoder), right = OLED + 3V3, both in
# the same top-to-bottom order as the Pico pins they go to.
LINK_X = (CX - 16.65, CX + 16.65)         # outside the button legs, inside the PCB edge
LINK_Y = 76.0                             # pin 1; 12 pins down to 103.94
LINK_L = ["GND", "SETUP", "AB", "SOUND_R", "SOUND_L", "FILE", "VIEW", "BACK",
          "ENC_SW", "ENC_B", "ENC_A", "GND"]
LINK_R = ["GND", "CS", "SCK", "MOSI", "DC", "RST", "GND", "GND", "GND", "GND", "3V3", "GND"]

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
    t.SetMirrored(layer == pcbnew.B_SilkS)
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


def oled(b, n):
    """Adafruit 4741 breakout as one footprint: J1 holes for its own (soldered) male header,
    M2.5 holes for standoffs under its bottom tabs, and its outline as courtyard so DRC
    catches the encoder / BACK button running into it."""
    fp = pcbnew.FOOTPRINT(b)
    fp.SetFPID(pcbnew.LIB_ID("grainview", "Adafruit_4741_OLED"))
    fp.SetReference("J1")
    fp.SetValue("Adafruit 4741 OLED (own header)")
    fp.Reference().SetLayer(pcbnew.F_Fab)
    b.Add(fp)
    fp.SetPosition(V(OLED_X0, OLED_T))
    for i, net in enumerate(OLED_PINS):
        q = pcbnew.PAD(fp)
        q.SetNumber(str(i + 1))
        q.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
        q.SetLayerSet(q.PTHMask())
        q.SetShape(pcbnew.PAD_SHAPE_RECT if i == 0 else pcbnew.PAD_SHAPE_CIRCLE)
        q.SetSize(V(1.7, 1.7))
        q.SetDrillSize(V(1.0, 1.0))
        fp.Add(q)
        q.SetPosition(V(OLED_HDR[0] + 2.54 * i, OLED_HDR[1]))
        if net:
            q.SetNet(n(net))
    for x, y in OLED_HOLES:
        q = pcbnew.PAD(fp)
        q.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
        q.SetLayerSet(q.UnplatedHoleMask())
        q.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
        q.SetSize(V(2.7, 2.7))
        q.SetDrillSize(V(2.7, 2.7))
        fp.Add(q)
        q.SetPosition(V(x, y))
    x0, y0, w, h, t = OLED_X0, OLED_T, OLED_BW, OLED_BH, OLED_TAB
    outline = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h),     # right tab cut off
               (x0 + t, y0 + h), (x0 + t, y0 + h + t), (x0, y0 + h + t)]
    for layer, pts in [(pcbnew.F_CrtYd, outline), (pcbnew.F_Fab, outline)]:
        poly(fp, layer, pts)
    a, c = rect_c(*OLED_AC, OLED_ACTIVE, OLED_ACTIVE)
    poly(fp, pcbnew.F_Fab, [a, (c[0], a[1]), c, (a[0], c[1])])
    for _, xa, ya, xb, yb in OLED_TALL:
        poly(fp, pcbnew.F_Fab, [(xa, ya), (xb, ya), (xb, yb), (xa, yb)])
    return fp


def poly(fp, layer, pts):
    for (xa, ya), (xb, yb) in zip(pts, pts[1:] + pts[:1]):
        sh = pcbnew.PCB_SHAPE(fp)
        sh.SetShape(pcbnew.SHAPE_T_SEGMENT)
        sh.SetLayer(layer)
        sh.SetWidth(MM(0.05 if layer == pcbnew.F_CrtYd else 0.1))
        sh.SetStart(V(xa, ya))
        sh.SetEnd(V(xb, yb))
        fp.Add(sh)


def antenna_keepout(b, all_copper=True):
    """Pico W antenna: no copper under it (Pico W datasheet keep-out). On the control board,
    ~21 mm further away, only keep the ground pour out."""
    z = pcbnew.ZONE(b)
    z.SetIsRuleArea(True)
    z.SetZoneName("Pico W antenna")
    z.SetDoNotAllowTracks(all_copper)
    z.SetDoNotAllowVias(all_copper)
    z.SetDoNotAllowPads(all_copper)
    z.SetDoNotAllowZoneFills(True)
    z.SetDoNotAllowFootprints(False)
    ls = pcbnew.LSET()
    ls.AddLayer(pcbnew.F_Cu)
    ls.AddLayer(pcbnew.B_Cu)
    z.SetLayerSet(ls)
    xa, ya, xb, yb = PICO_KEEPOUT
    o = z.Outline()
    o.NewOutline()
    for x, y in [(xa, ya), (xb, ya), (xb, yb), (xa, yb)]:
        o.Append(MM(x), MM(y))
    b.Add(z)


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
    text(b, "SOUND", CX, BUTTONS[3][2], h=1.5)
    text(b, "GRAINVIEW", CX, 10.6, h=2.4, bold=True)
    return b


# Panel colours (to match the Multigrain): white solder mask, black silkscreen, ENIG.
# pcbnew's Python can't reach the stackup, so it's written into the saved file.
PANEL_STACKUP = """\t\t(stackup
\t\t\t(layer "F.SilkS" (type "Top Silk Screen") (color "Black"))
\t\t\t(layer "F.Paste" (type "Top Solder Paste"))
\t\t\t(layer "F.Mask" (type "Top Solder Mask") (color "White") (thickness 0.01))
\t\t\t(layer "F.Cu" (type "copper") (thickness 0.035))
\t\t\t(layer "dielectric 1" (type "core") (thickness 1.51) (material "FR4")
\t\t\t\t(epsilon_r 4.5) (loss_tangent 0.02))
\t\t\t(layer "B.Cu" (type "copper") (thickness 0.035))
\t\t\t(layer "B.Mask" (type "Bottom Solder Mask") (color "White") (thickness 0.01))
\t\t\t(layer "B.Paste" (type "Bottom Solder Paste"))
\t\t\t(layer "B.SilkS" (type "Bottom Silk Screen") (color "Black"))
\t\t\t(copper_finish "ENIG")
\t\t\t(dielectric_constraints no)
\t\t)
"""


def add_stackup(path, stackup):
    s = open(path).read()
    assert "(stackup" not in s
    s = s.replace("\t(setup\n", "\t(setup\n" + stackup, 1)
    open(path, "w").write(s)


# ---------------------------------------------------------------- PCB helpers ---
def outline(b, pts):
    for a, c in zip(pts, pts[1:] + pts[:1]):
        sh = pcbnew.PCB_SHAPE(b)
        sh.SetShape(pcbnew.SHAPE_T_SEGMENT)
        sh.SetLayer(pcbnew.Edge_Cuts)
        sh.SetWidth(MM(0.1))
        sh.SetStart(V(*a))
        sh.SetEnd(V(*c))
        b.Add(sh)


def ref_inside(fp, h=0.9):
    """Put the reference in the middle of the part's outline (silkscreen tidy: the default
    spots collide on tightly packed pairs). Readable while placing parts, hidden once fitted."""
    layer = pcbnew.B_CrtYd if fp.IsFlipped() else pcbnew.F_CrtYd
    bb = fp.GetCourtyard(layer).BBox()
    r = fp.Reference()
    r.SetPosition(bb.Centre())
    r.SetTextSize(V(h, h))
    r.SetTextThickness(MM(h * 0.15))
    r.SetTextAngleDegrees(90 if bb.GetHeight() > bb.GetWidth() else 0)


def placer(b, n):
    def part(lib, name, ref, pins, a, b_, d, at, value="", back=True):
        f = footprint(b, lib, name, ref, 0, 0, back=back, value=value)
        orient(f, a, b_, d)
        place_at_pad(f, a, *at)
        n.connect(f, pins)
        return f
    return part


def link(part, kind, back):
    """The two board-to-board strips (kind: 'PinSocket' on control, 'PinHeader' on main)."""
    for ref, x, nets in [("J5", LINK_X[0], LINK_L), ("J6", LINK_X[1], LINK_R)]:
        part(f"Connector_{kind}_2.54mm", f"{kind}_1x12_P2.54mm_Vertical", ref,
             {str(i + 1): s for i, s in enumerate(nets)}, "1", "12", "+y", (x, LINK_Y),
             value=f"1x12 {'female 8.5 mm' if kind == 'PinSocket' else 'male'} (board link)",
             back=back)


# ---------------------------------------------------------------- control PCB ---
def control_pcb():
    """Front board: OLED, encoder and buttons on the front, the link sockets on the back.
    Nothing else on the back, so the switches sit flat on a clean board."""
    b = pcbnew.CreateEmptyBoard()
    b.SetCopperLayerCount(2)
    n = Nets(b)
    # outline with an edge notch under each STEMMA QT connector of the OLED
    (lx0, ly0, lx1, ly1), (rx0, ry0, rx1, ry1) = STEMMA
    g = STEMMA_NOTCH
    outline(b, [(PCB_X0, PCB_Y0), (PCB_X1, PCB_Y0),
                (PCB_X1, ry0 - g), (rx0 - g, ry0 - g), (rx0 - g, ry1 + g), (PCB_X1, ry1 + g),
                (PCB_X1, PCB_Y1), (PCB_X0, PCB_Y1),
                (PCB_X0, ly1 + g), (lx1 + g, ly1 + g), (lx1 + g, ly0 - g), (PCB_X0, ly0 - g)])

    oled(b, n)
    antenna_keepout(b, all_copper=False)

    e = footprint(b, "Rotary_Encoder", "RotaryEncoder_Alps_EC11E-Switch_Vertical_H20mm",
                  "ENC1", 0, 0, value="EC11 push encoder (7 mm body)")
    mps = [p.GetPosition() for p in e.Pads() if p.GetNumber() == "MP"]
    mid = (mps[0] + mps[1]) / 2
    e.SetPosition(e.GetPosition() + V(*ENC) - mid)
    n.connect(e, {"A": "ENC_A", "B": "ENC_B", "C": "GND", "S1": "ENC_SW", "S2": "GND"})

    # PHAP5-30 = standard 6 mm tact footprint (legs 6.5 x 4.5 mm)
    for i, (name, x, y, net, _) in enumerate(BUTTONS):
        sw = footprint(b, "Button_Switch_THT", "SW_PUSH_6mm", f"SW{i + 1}", 0, 0,
                       value=f"{name} PHAP5-30VA2K + U5532")
        ps = [p.GetPosition() for p in sw.Pads()]
        c = sum(ps[1:], ps[0]) / len(ps)
        sw.SetPosition(sw.GetPosition() + V(x, y) - c)
        n.connect(sw, {"1": net, "2": "GND"})

    link(placer(b, n), "PinSocket", back=True)
    text(b, "GRAINVIEW control v1.0", CX, 71.5, h=1.2, layer=pcbnew.B_SilkS)
    return b


# ---------------------------------------------------------------- main PCB ------
def main_pcb():
    """Rear board: link headers on the front (facing the control board); Pico in sockets,
    power entry, SWD and spare-GPIO headers on the back."""
    b = pcbnew.CreateEmptyBoard()
    b.SetCopperLayerCount(2)
    n = Nets(b)
    outline(b, [(PCB_X0, PCB_Y0), (PCB_X1, PCB_Y0), (PCB_X1, PCB_Y1), (PCB_X0, PCB_Y1)])
    antenna_keepout(b)
    part = placer(b, n)
    link(part, "PinHeader", back=False)

    # Pico 2 W(H) (back) in 2x 1x20 sockets
    p = footprint(b, "Module", "RaspberryPi_Pico_Common_THT", "U1", 0, 0, back=True,
                  value="Pico 2 W (sockets)")
    orient(p, "20", "1", "+y")             # USB end (pins 1/40) at the bottom
    pads = {q.GetNumber(): q.GetPosition() for q in p.Pads()}
    mid = (pads["1"] + pads["40"]) / 2
    p.SetPosition(p.GetPosition() + V(CX, PICO_USB_Y) - mid)
    n.connect(p, {str(k): v for k, v in PICO.items()})

    R = ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    D = ("Diode_THT", "D_DO-41_SOD81_P7.62mm_Horizontal")

    # everything else on the back, above the Pico, placed for short runs to the Pico pins
    # (the antenna keep-out blocks the middle above the Pico, so runs go down the two side
    # channels between the Pico's rows and the link strips):
    #   power chain down the right side (VSYS is the Pico's pin 39, bottom right),
    #   SWD header top left with R1/R2 on the left (GP14/15 = pins 19/20, top left) and R3/R4
    #   on the right (GP26/22 = pins 31/29, right row), spare-GPIO header just above the Pico.
    part("Connector_IDC", "IDC-Header_2x05_P2.54mm_Vertical", "J2",
         {"1": "M12V", "2": "M12V", "3": "GND", "4": "GND", "5": "GND", "6": "GND",
          "7": "GND", "8": "GND", "9": "P12V_IN", "10": "P12V_IN"},
         "1", "9", "+x", (CX - 5.08, 15.5), value="Eurorack power")   # shroud inside the edge
    text(b, "-12V (RED)", CX - 6.6, 23.3, h=1.0, layer=pcbnew.B_SilkS)   # ribbon stripe
    part("Connector_PinHeader_1.27mm", "PinHeader_2x05_P1.27mm_Vertical", "J3",
         {"1": "VTREF", "2": "SWDIO", "3": "GND", "4": "SWCLK", "5": "GND", "9": "GND",
          "10": "NRST"}, "1", "9", "+y", (5.6, 13.0), value="SWD to JTRACE")
    text(b, "RED", 4.97, 11.35, h=0.9, layer=pcbnew.B_SilkS)   # ribbon stripe = pin 1 (VTREF)
    part("Connector_PinHeader_2.54mm", "PinHeader_1x06_P2.54mm_Vertical", "J4",
         {"1": "GP5", "2": "GP13", "3": "GP16", "4": "GP27", "5": "GP28", "6": "GND"},
         "1", "6", "+x", (13.8, 56.5), value="spare GPIO")

    # power entry: rack +12 V -> D1 -> regulator -> 5 V -> D2 -> VSYS.
    # U2: R-78E5.0 / TSR1-2450 (switching, ~10 mm tall, cool) preferred; a 7805 gets bent flat.
    part(*D, "D1", {"1": "P12V", "2": "P12V_IN"}, "2", "1", "+x", (26.0, 26.0),
         value="1N5817 reverse prot.")
    part("Capacitor_THT", "CP_Radial_D5.0mm_P2.00mm", "C1", {"1": "P12V", "2": "GND"},
         "1", "2", "+x", (34.0, 30.5), value="10uF 25V")
    part("Package_TO_SOT_THT", "TO-220-3_Vertical", "U2", {"1": "P12V", "2": "GND", "3": "P5V"},
         "1", "3", "+x", (24.0, 34.0), value="R-78E5.0 / TSR1-2450 / 7805")
    part("Capacitor_THT", "CP_Radial_D5.0mm_P2.00mm", "C2", {"1": "P5V", "2": "GND"},
         "1", "2", "+x", (31.5, 41.0), value="10uF 16V")
    part(*D, "D2", {"1": "VSYS", "2": "P5V"}, "2", "1", "+x", (26.0, 46.5),
         value="1N5817 5V->VSYS")
    part("Capacitor_THT", "C_Disc_D3.0mm_W1.6mm_P2.50mm", "C3", {"1": "VSYS", "2": "GND"},
         "1", "2", "+x", (33.6, 110.5), value="100nF")       # at the Pico's VSYS pin
    for i, (a, c, v, x) in enumerate([("SWDIO_P", "SWDIO", "47R", 4.5),
                                      ("SWCLK_P", "SWCLK", "47R", 7.5),
                                      ("VTREF_P", "VTREF", "1k", 33.0),
                                      ("NRST_P", "NRST", "1k DNP", 36.0)]):
        part(*R, f"R{i + 1}", {"1": c, "2": a}, "1", "2", "+y", (x, 40.0 if x < CX else 52.0),
             value=v)

    text(b, "GRAINVIEW main v1.0", CX - 4.0, 50.0, h=1.2, layer=pcbnew.B_SilkS)
    # caps / regulator: beside the body instead (their middles are between the pads)
    beside = {"C1": (35.0, 34.0), "C2": (36.6, 41.0), "C3": (34.85, 108.6), "U2": (26.54, 38.4)}
    for f in b.GetFootprints():
        r = f.GetReference()
        if r[:1] in "RDCU" and r != "U1":
            ref_inside(f)
            if r in beside:
                f.Reference().SetPosition(V(*beside[r]))
                f.Reference().SetTextAngleDegrees(0)
        if r == "J3":                      # its "RED" stripe mark sits above it
            f.Reference().SetPosition(V(4.97, 19.7))
    return b


if __name__ == "__main__":
    for name, fn in [("grainview_panel", panel), ("grainview_control", control_pcb),
                     ("grainview_main", main_pcb)]:
        path = os.path.join(HERE, name + ".kicad_pcb")
        board = fn()
        board.Save(path)
        if name == "grainview_panel":
            add_stackup(path, PANEL_STACKUP)
        print("wrote", path)
