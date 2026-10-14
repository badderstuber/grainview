#!/usr/bin/env python3
"""grainview_route.py - autoroute the GRAINVIEW control + main PCBs (KiCad 10 + Freerouting).

Run with KiCad's Python after grainview_gen.py (which rewrites the boards unrouted):

    /Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3 \
        hardware/grainview_route.py /path/to/java21 /path/to/freerouting-2.1.0.jar [control|main ...]

For each board: set the track rules, export Specctra DSN, route it with Freerouting
(headless), import the session, add a ground pour on both layers, fill, save in place.
Freerouting 2.x runs headless but needs Java 21 (1.9.0 runs on Java 17 but only with its GUI);
a portable JDK 21 (adoptium.net tar.gz, no install) works.
"""
import os
import subprocess
import sys
import tempfile

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
MM = pcbnew.FromMM

TRACK, CLEARANCE, VIA, VIA_DRILL = 0.3, 0.2, 0.7, 0.35   # JLC 2-layer is fine with all of these
POWER_TRACK = 0.6
POWER = ["P12V_IN", "P12V", "P5V", "VSYS", "3V3", "GND"]
ZONE_CLEARANCE, ZONE_MIN = 0.3, 0.25
EDGE = 0.5                                 # KiCad's default copper-to-edge clearance
PASSES = 100


def rules(b):
    ns = b.GetDesignSettings().m_NetSettings
    d = ns.GetDefaultNetclass()
    d.SetTrackWidth(MM(TRACK))
    d.SetClearance(MM(CLEARANCE))
    d.SetViaDiameter(MM(VIA))
    d.SetViaDrill(MM(VIA_DRILL))
    pw = pcbnew.NETCLASS("Power")
    pw.SetTrackWidth(MM(POWER_TRACK))
    pw.SetClearance(MM(CLEARANCE))
    pw.SetViaDiameter(MM(VIA))
    pw.SetViaDrill(MM(VIA_DRILL))
    ns.SetNetclass("Power", pw)
    for net in POWER:
        ns.SetNetclassPatternAssignment(net, "Power")
    ns.RecomputeEffectiveNetclasses()
    b.SynchronizeNetsAndNetClasses(True)


def edge_keepout(b):
    """Freerouting doesn't know KiCad's edge clearance: fence the board edge with a no-track
    rule area EDGE mm wide (it is exported to the DSN as a keep-out)."""
    outline = pcbnew.SHAPE_POLY_SET()
    b.GetBoardPolygonOutlines(outline, False)
    inner = outline.CloneDropTriangulation()
    inner.Inflate(MM(-EDGE), pcbnew.CORNER_STRATEGY_CHAMFER_ALL_CORNERS, MM(0.01))
    z = pcbnew.ZONE(b)
    z.SetIsRuleArea(True)
    z.SetZoneName("edge clearance")
    z.SetDoNotAllowTracks(True)
    z.SetDoNotAllowVias(True)
    z.SetDoNotAllowPads(False)
    z.SetDoNotAllowZoneFills(False)
    z.SetDoNotAllowFootprints(False)
    ls = pcbnew.LSET()
    ls.AddLayer(pcbnew.F_Cu)
    ls.AddLayer(pcbnew.B_Cu)
    z.SetLayerSet(ls)
    o = z.Outline()                        # outer = board outline, hole = outline inset by EDGE
    o.NewOutline()
    for i in range(outline.COutline(0).PointCount()):
        pt = outline.COutline(0).CPoint(i)
        o.Append(pt.x, pt.y)
    o.NewHole()
    for i in range(inner.COutline(0).PointCount()):
        pt = inner.COutline(0).CPoint(i)
        o.Append(pt.x, pt.y, -1, 0)
    b.Add(z)
    return z


def ground_pour(b):
    gnd = b.FindNet("GND")
    if gnd is None:
        return
    bb = b.GetBoardEdgesBoundingBox()
    for layer in (pcbnew.F_Cu, pcbnew.B_Cu):
        z = pcbnew.ZONE(b)
        z.SetLayer(layer)
        z.SetNet(gnd)
        z.SetLocalClearance(MM(ZONE_CLEARANCE))
        z.SetMinThickness(MM(ZONE_MIN))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
        o = z.Outline()
        o.NewOutline()
        for x, y in [(bb.GetLeft(), bb.GetTop()), (bb.GetRight(), bb.GetTop()),
                     (bb.GetRight(), bb.GetBottom()), (bb.GetLeft(), bb.GetBottom())]:
            o.Append(x, y)
        b.Add(z)
    pcbnew.ZONE_FILLER(b).Fill(b.Zones())


def route(java, jar, name):
    path = os.path.join(HERE, f"grainview_{name}.kicad_pcb")
    b = pcbnew.LoadBoard(path)
    rules(b)
    fence = edge_keepout(b)
    tmp = tempfile.mkdtemp(prefix=f"route_{name}_")
    dsn, ses = os.path.join(tmp, name + ".dsn"), os.path.join(tmp, name + ".ses")
    assert pcbnew.ExportSpecctraDSN(b, dsn), "DSN export failed"
    print(f"[{name}] routing ({PASSES} passes max) ...", flush=True)
    r = subprocess.run([java, "-jar", jar, "--gui.enabled=false",
                        "--usage_and_diagnostic_data.disable_analytics=true",
                        "-de", dsn, "-do", ses, "-mp", str(PASSES)],
                       cwd=tmp, timeout=1800, capture_output=True, text=True)
    if r.returncode or not os.path.exists(ses):
        sys.exit(r.stdout[-3000:] + r.stderr[-3000:])
    assert pcbnew.ImportSpecctraSES(b, ses), "SES import failed"
    b.Remove(fence)                        # KiCad's own edge-clearance rule covers it now
    ground_pour(b)
    b.Save(path)
    print(f"[{name}] wrote {path} ({len(b.GetTracks())} tracks/vias)")


if __name__ == "__main__":
    java, jar = sys.argv[1:3]
    for name in sys.argv[3:] or ["control", "main"]:
        route(java, jar, name)
