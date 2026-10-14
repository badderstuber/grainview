#!/bin/bash
# grainview_export.sh - DRC + JLC order files (Gerbers + Excellon drill, one zip per board).
# Run after grainview_gen.py + grainview_route.py:  hardware/grainview_export.sh
set -e
CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
cd "$(dirname "$0")"
rm -rf gerbers && mkdir -p gerbers
for f in panel control main; do
  $CLI pcb drc --refill-zones --save-board --severity-error -o gerbers/drc_$f.rpt grainview_$f.kicad_pcb | tail -2
  O=gerbers/grainview_$f; mkdir -p $O
  $CLI pcb export gerbers --check-zones --no-x2 --no-netlist --subtract-soldermask \
      --layers F.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,Edge.Cuts -o $O/ grainview_$f.kicad_pcb >/dev/null
  # JLC: Excellon, PTH/NPTH separate, oval slots in "alternate" mode
  $CLI pcb export drill --format excellon --excellon-oval-format alternate --excellon-separate-th \
      --generate-map --map-format pdf -o $O/ grainview_$f.kicad_pcb >/dev/null
  (cd gerbers && zip -qr grainview_$f.zip grainview_$f)
  echo "gerbers/grainview_$f.zip"
done
