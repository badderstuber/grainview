# GRAINVIEW module — hardware v1 spec

Working spec for the first PCB + panel order (decided 2026-10-13). Pins: see PINMAP.md —
the PCB copies the breadboard pin map exactly, so the breadboard firmware runs unchanged.

## Decisions
| | |
|---|---|
| Format | Eurorack 3U, **8HP** (panel 40.3 × 128.5 mm). Screen board is 35 mm wide, fits. |
| Build | **Hand-soldered, through-hole only.** No SMD, no assembly service. |
| MCU | **Pico 2 W module** soldered to the main PCB (no bare RP2350). |
| Screen | **Adafruit 1.5" SSD1327 breakout** (product 4741), J1/J2 cut for SPI, on headers. |
| Controls | EC11-style push encoder + **7 buttons**: BACK, VIEW, FILE, SOUND‹, SOUND›, A/B, SETUP. |
| Buttons | **APEM PHAP5-30VA2K2T2N2** (6×6 THT tact, 7.3 mm, 160 g, 2.4 mm sq. actuator) + **APEM U5532** black 4.5 mm round cap (Leo's pick 2026-10-13: used in kits, feels good). Switch Electronics UK stocks both. Cap top ≈ 10.3 mm above the PCB; panel hole 5.2 mm. |
| Panel | **FR4 PCB panel**, black mask, white silkscreen, ENIG. Ordered with the main PCB (JLCPCB). |
| Link | 2×5 1.27 mm SWD header on the back → short ribbon → Multigrain JTRACE pins 1–10. |

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

## Mechanics (to confirm before layout)
- **Stack height:** the encoder's bushing seat sets the PCB↔panel gap (EC11 ≈ 7 mm). With the
  PHAP5 + U5532 cap top at ≈ 10.3 mm, caps stand ≈ 1.7 mm proud of a 1.6 mm panel at a 7 mm gap.
  The OLED glass must sit just behind the panel at that same gap, so a standard 8.5 mm socket is
  too tall — the OLED mounting (low-profile socket / direct solder / standoffs) is set once the
  breakout is measured.
- Main PCB parallel to the panel; encoder, buttons and the screen board stand off it.
  PCB↔panel distance is set by the encoder bushing + switch height — the **switch part
  decides this**, so it has to be chosen first.
- Screen board: 35 mm wide — still need its **height, mounting holes, header position, and
  glass offset** (measure the real board).
- Panel window over the OLED active area (≈ 27 × 27 mm), countersunk/rounded corners.

## Open
- [x] Buttons chosen: PHAP5-30VA2K2T2N2 + U5532 (standard 6 mm tact footprint, legs 6.5 × 4.5 mm).
- [ ] Measure the OLED breakout (above).
- [ ] **Pico-as-SWD-master check** (can run while the boards are at the fab): Raspberry Pi
      `debugprobe` firmware on the Pico 2 → pyOCD reads the Multigrain through the Pico's GPIOs.
- [ ] KiCad design → DRC → renders → Gerbers → order.

## Design files (draft v0.2, 2026-10-13)
`hardware/grainview_gen.py` (run with KiCad's Python) writes `hardware/grainview_panel.kicad_pcb`
and `hardware/grainview_main.kicad_pcb` from one layout table, so panel holes track the parts.
Placement + nets only, not routed.
- **Layout = `tools/panel_mock.html`**: screen · [BACK | encoder] · [VIEW | FILE] ·
  [SOUND‹ | SOUND›] · [A/B | SETUP]. Columns at CX ± 8.89 mm (mockup 12 / 28) = exactly the
  Pico's pin rows, so each button's legs straddle a Pico row (~1.4 mm clearance with the 6 mm
  tact placeholder). Rows 55 / 75.5 / 92 / 108.5 mm — VIEW/FILE moved down 2.5 mm from the
  mockup to clear the Pico W antenna keep-out.
- **Pico** on the back below the encoder, in sockets, **USB end down**, antenna end up.
- **Back-side parts** all in the top zone behind the raised OLED board: power entry (J2,
  regulator, diodes, caps), SWD header + resistors, spare-GPIO header.
- DRC: no clearance/edge/keep-out errors. The 32 "PTH inside courtyard" are the button legs
  straddling the socketed Pico's rows (intended, opposite sides of the board).
- Buttons final (v0.3): PHAP5-30 on the 6 mm tact footprint, 5.2 mm round panel holes.
- Placeholder: OLED 35×35 with header along the bottom (→ measure).
