# GRAINVIEW module — hardware v1 spec

Working spec for the first PCB + panel order (decided 2026-10-13). Pins: see PINMAP.md —
the PCBs copy the breadboard pin map exactly, so the breadboard firmware runs unchanged.

## Decisions
| | |
|---|---|
| Format | Eurorack 3U, **8HP** (panel 40.3 × 128.5 mm). Screen board is 35 mm wide, fits. |
| Build | **Hand-soldered, through-hole only.** No SMD, no assembly service. |
| Boards | **Two PCBs** (2026-10-14): a **control board** (OLED, encoder, buttons on its front; nothing else, so the switches sit flat) and a **main board** behind it (Pico in sockets, power, SWD on its back). Joined by two 1x12 2.54 mm strips down the long edges, outside the button columns: female 8.5 mm sockets on the control board's back, male headers on the main board's front → boards 11 mm apart, separable. Why: with one board the Pico's socket solder joints sat under the switch bodies. |
| MCU | **Pico 2 WH** (Leo's existing one, headers fitted) in 2× 1x20 sockets on the main board (no bare RP2350). |
| Screen | **Adafruit 1.5" SSD1327 breakout** (product 4741), J1/J2 cut for SPI. Its own male header is **soldered straight into the control PCB** (no socket: too tall), plus one M2.5 nylon standoff under the bottom-left tab. **Cut off the bottom-right tab** (below the GND end of the header; only a hole + GND pour, no signals) so the encoder fits in the right column; a foam pad supports that corner. |
| Controls | EC11-style push encoder + **7 buttons**: BACK, VIEW, FILE, SOUND‹, SOUND›, A/B, SETUP. |
| Buttons | **APEM PHAP5-30VA2K2T2N2** (6×6 THT tact, 7.3 mm, 160 g, 2.4 mm sq. actuator) + **APEM U5532** black 4.5 mm round cap (Leo's pick 2026-10-13: used in kits, feels good). Switch Electronics UK stocks both. Cap top ≈ 10.3 mm above the PCB; panel hole 5.2 mm. |
| Panel | **FR4 PCB panel**, **white mask, black silkscreen** (matches the Multigrain; metal maybe later), ENIG. Ordered with the PCBs (JLCPCB). |
| Link | 2×5 1.27 mm SWD header on the main board's back → short ribbon → Multigrain JTRACE pins 1–10. |

## Circuit
- **Power:** Eurorack 2×5 shrouded header (−12 V / GND / +12 V; only +12 V used).
  Reverse-polarity diode → 7805-class TO-220 regulator (or LM2940 / 78M05) → **5 V → Schottky →
  Pico VSYS**, so USB and rack power can both be connected (Pico's own VBUS diode does the
  other side). Pico 3V3(OUT) feeds the OLED as now (OLED ≈ 30–50 mA, well inside 300 mA).
  Bulk caps on +12 V and 5 V.
- **SWD:** SWCLK GP14, SWDIO GP15 via **33–100 Ω series resistors**; VTREF → 1 kΩ → GP26/ADC0
  (detects a powered Multigrain); GND on the odd pins. nRESET: route to a spare GPIO through a
  jumper/DNP resistor (optional; we don't use it today). Ribbon kept short (< 15 cm).
- **Controls:** buttons and encoder to GND, internal pull-ups (RP2350 erratum E9: pull-ups only).
  Optional 100 nF on encoder A/B footprints (DNP by default; IRQ decoder works without).
- **Spare GPIOs** (GP5, 13, 16, 22, 27, 28) broken out to a small 0.1" header for later
  (e.g. LEDs on the buttons, a gate in).

## Mechanics
- **OLED breakout geometry** (from Adafruit's own board file,
  github.com/adafruit/Adafruit-Grayscale-1.5-inch-128x128-OLED-PCB; matches Leo's 35 / 42 / 47 mm):
  35.56 × 41.91 mm body + two 5.08 mm tabs at the bottom corners (47 mm overall). Seen from the
  glass side: 8-pin header along the **top**, 2.54 mm in, pins 1–8 = Data Clk DC Rst CS 3Vo VIN
  GND left to right, centred. Four 2.5 mm holes 2.54 mm in from the corners (bottom pair on the
  tabs). Glass 33.8 × 36.5 mm; active area 26.855 mm square, 2.0 mm below the glass top (the
  flex tail is at the bottom). Back side: two STEMMA QT connectors at the left/right edges,
  23.5 mm below the top edge, and SMD parts (an inductor is the tallest).
- **Placement:** board top at y 10 (the rail zone ends there), so the active area is centred at
  y 30.4 and the panel window is 29.4 mm square around it.
- **Stack height (Z):** the encoder's body sets the control-PCB↔panel gap **G = 7 mm** (Leo's EC11, measured). The OLED
  sits on its header plastic (**S** = 2.5 mm above the control PCB), so the glass front is at S + OLED
  thickness and has to be ≤ G. The STEMMA connectors stand ~3 mm (Leo, 2026-10-14) > S, so the
  control PCB has an **edge notch under each one** (`STEMMA`/`STEMMA_NOTCH` in the generator).
  OLED: glass ≈ 2 mm (Leo, tape measure) + 1.6 mm PCB ≈ 3.6 mm → glass front at 2.5 + 3.6 ≈ **6.1 mm**
  above the control PCB, so the encoder body (G) must be ≥ ~6.3 mm.
  Caps: PHAP5 + U5532 top at ≈ 10.3 mm → ≈ 1.7 mm proud at G = 7.
- The control board has no parts on its back except the link sockets, so nothing's solder joints
  sit under the OLED or the switches. Trim the OLED / switch / encoder leads short on the back
  (the main board is 11 mm behind).
- Both PCBs parallel to the panel; the main board hangs off the control board on the link strips.

## Open
- [x] Buttons chosen: PHAP5-30VA2K2T2N2 + U5532 (standard 6 mm tact footprint, legs 6.5 × 4.5 mm).
- [x] OLED breakout outline / header / holes (Adafruit board file + Leo's measurements).
- [x] STEMMA connector height ≈ 3 mm → edge notches in the control PCB.
- [x] OLED thickness ≈ 3.6 mm (2 mm glass + 1.6 mm PCB) → glass front ≈ 6.1 mm above the control PCB.
- [x] Encoder body height = **7 mm** (Leo's EC11, feet → top of the metal frame) → G = 7 mm:
      glass ≈ 0.9 mm behind the panel, button caps ≈ 1.7 mm proud. Z stack settled.
- [x] **Pico-as-SWD-master check** (2026-10-20, on the built v1.0 module): `pico/swdtest.py`
      bit-bangs SWD on GP14/15 through J3 → JTRACE and reads DPIDR / CPUID / DBGMCU_IDCODE
      (STM32H743/753 rev V). No debugprobe (its default SWD pins are our encoder pins).
- [x] Two boards (switches would sit on the Pico socket joints with one board).
- [ ] Check the case depth (module ≈ 33 mm behind the panel).
- [x] Route control + main → DRC.
- [x] Tidy silkscreen → Gerbers + drill files (3 boards), 2026-10-14.
- [x] Ordered from JLC 2026-10-14 (all three boards, one order; ETA ~5–7 days).

## Stack (front → back, mm behind the panel's back face)
| | |
|---|---|
| Control board front | 7.0 (= encoder body). OLED glass front ≈ 0.9 mm behind the panel. |
| Control board back | 8.6; link sockets 8.5 mm tall |
| Main board front / back | 19.6 / 21.2 |
| Pico (in 8.5 mm sockets) top parts | ≈ 31 |
| Deepest part | U2: **L7805CV fitted for v1** (Leo, 2026-10-14) stands ~20 mm → ≈ 41 (no room to bend it flat). R-78E5.0 / TSR1-2450 (drop-in) ≈ 31 |
Total ≈ **41 mm** behind the panel with the L7805 (≈ 33 mm with the R-78E) + the power ribbon plug: check the case depth.

## Design files (v1.0, 2026-10-14)
`hardware/grainview_gen.py` (run with KiCad's Python) writes `hardware/grainview_panel.kicad_pcb`,
`grainview_control.kicad_pcb` and `grainview_main.kicad_pcb` from one layout table, so panel holes
and the board-to-board strips line up (placement + nets). **`hardware/grainview_route.py`** then
routes the control and main boards in place: track rules (0.3 mm signals, 0.6 mm power/GND,
0.2 mm clearance, 0.7/0.35 mm vias), a 0.5 mm no-track fence along the edges, Freerouting 2.1
headless (needs Java 21; a portable Adoptium JDK works), then a GND pour on both layers.
**Re-running the generator wipes the routing**, so route again after any placement change.
Freerouting is random: re-run until DRC shows 0 unconnected (the main board took 2 tries).
- v1.0 routed 2026-10-14 (after the silkscreen tidy; main took 5 tries): DRC 0 unconnected, no
  silkscreen issues. One expected DRC item left on the control board: J6 pin 1 (GND) reaches the
  front pour with 1 thermal spoke instead of 2 ("starved thermal"); it's also connected by its
  tracks and the back pour. Plus the "missing library 'grainview'" warning.

- **Layout = `tools/panel_mock.html`**: screen · [BACK | encoder] · [VIEW | FILE] ·
  [SOUND‹ | SOUND›] · [A/B | SETUP]. Columns at CX ± 8.89 mm (11.26 / 29.04), rows
  62 / 78 / 94 / 110 mm: all on a 16 mm pitch, window bottom ~17 mm above the top row (Leo,
  2026-10-14). Encoder in the right column thanks to the
  cut-off OLED tab.
- **Control board**: OLED (J1 = one footprint: 8 header holes, one M2.5 hole, outline as
  courtyard, active area + its tall back parts on F.Fab), edge notches for the STEMMA connectors,
  encoder, 7 buttons, link sockets J5/J6 on the back. No ground pour under the Pico W antenna.
- **Link strips** at x 3.5 / 36.8, pins y 76–103.9 (pin 1 at the top). J5 (left, Pico pins 1–20
  side): GND, SETUP, AB, SOUND_R, SOUND_L, FILE, VIEW, BACK, ENC_SW, ENC_B, ENC_A, GND.
  J6 (right): GND, CS, SCK, MOSI, DC, RST, GND ×4, 3V3, GND. Generator check: both boards'
  strips match pin-for-pin, and every control-board net reaches the Pico.
- **Main board**: link headers J5/J6 on the front; on the back the Pico (sockets, **USB end
  down**, pins 1/40 at y 115.5, USB plug edge ≈ 118.2, antenna up with a full copper keep-out).
  Above it, placed for short runs down the two side channels (the keep-out blocks the middle):
  power header J2 top centre, the power chain down the right (D1, C1, U2, C2, D2; C3 at the
  Pico's VSYS pin), SWD header J3 top left (+ R1/R2 left, R3/R4 right), spare-GPIO header J4
  just above the Pico. Silkscreen marks the ribbon stripes: "RED" above J3 (pin 1 = VTREF) and
  "-12V (RED)" at J2.
- **The OLED's bottom-right tab has to be cut**: the OLED courtyard already leaves it out, and the
  encoder would hit it by ~0.9 mm.

## Order files (`hardware/gerbers/`, v1.0)
One zip per board (Gerbers: Cu, mask, silk both sides + Edge.Cuts; Excellon drill, PTH/NPTH
separate, oval slots in "alternate" mode, which is what JLC asks for). Upload each zip as its own
design. Re-export after any change: `hardware/grainview_export.sh` (DRC reports land next to the zips).

| Zip | Size | JLC settings |
|---|---|---|
| `grainview_control.zip` | 37.9 × 108 mm | 2 layers, 1.6 mm, any colour, HASL lead-free |
| `grainview_main.zip` | 37.9 × 108 mm | 2 layers, 1.6 mm, any colour, HASL lead-free |
| `grainview_panel.zip` | 40.3 × 128.5 mm | 2 layers, 1.6 mm, **white mask / black silk**, **"Remove order number"** (else JLC prints it on the front). No exposed copper, so the finish doesn't matter (HASL is fine). All panel holes are milled from Edge.Cuts (no drill hits). |
