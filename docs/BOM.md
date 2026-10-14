# GRAINVIEW v1.0 — parts list (one module)

Boards: JLC order 2026-10-14 (panel, control, main). Spec: HARDWARE.md.
"Have?" = what Leo already owns (as of 2026-10-14).

## Control board (front)
| Ref | Qty | Part | Notes | Have? |
|---|---|---|---|---|
| SW1–SW7 | 7 | APEM **PHAP5-30VA2K2T2N2** tact switch (7.3 mm, 160 g, THT) | Switch Electronics UK | buy (+ spares) |
| — | 7 | APEM **U5532** black 4.5 mm round cap | Switch Electronics, sold in 10s | buy |
| ENC1 | 1 | EC11 push encoder, vertical, 20 mm shaft, **7 mm body** (feet → start of thread) | the breadboard one fits; a spare must be ≥ 6.3 mm body | have 1 |
| — | 1 | knob for the encoder shaft | e.g. Thonk; match the shaft (D or knurled) | buy |
| J1 | 1 | Adafruit 4741 1.5" OLED, its own header soldered in | **cut the bottom-right tab first** | have |
| J5, J6 | 2 | 1x12 female header, 2.54 mm, 8.5 mm tall | or cut from 1x20 / 1x40 strips (lose one position per cut) | buy |
| — | 1–2 | 3 mm double-sided foam pad | under the OLED's bottom corners | buy/have |
| — | (opt.) | M2.5 nylon screw + nut + washers to ~2.5 mm | bottom-left OLED hole, if you want it screwed down | optional |

## Main board (back)
| Ref | Qty | Part | Notes | Have? |
|---|---|---|---|---|
| U1 | 1 | Raspberry Pi **Pico 2 WH** | | have |
| — | 2 | 1x20 female header, 2.54 mm, 8.5 mm | Pico sockets | buy |
| J5, J6 | 2 | 1x12 male header, 2.54 mm | break off a 1x40 strip | buy/have |
| J4 | 1 | 1x6 male header, 2.54 mm | same strip; optional (spare GPIOs) | buy/have |
| J2 | 1 | 2x5 shrouded box header, 2.54 mm (Eurorack power) | | buy |
| — | 1 | Eurorack power ribbon, 10-to-16 pin | to the bus board | have? |
| J3 | 1 | 2x5 **1.27 mm** male pin header, THT (SWD) | same part as the one soldered into JTRACE | buy |
| — | 1 | 10-pin 1.27 mm SWD ribbon (female both ends) | the Olimex grey cable works; a 2nd keeps the ST-Link setup intact | have 1 |
| U2 | 1 | **ST L7805CV** 5 V regulator, TO-220 (Switch Electronics, with the buttons) | v1 choice. Stands ~20 mm, so the module is ~41 mm deep: check the case. Runs warm (0.5–1 W, fine). Drop-in upgrade later: RECOM **R-78E5.0-0.5** / Traco **TSR 1-2450** (~10 mm, cool) | buy |
| D1, D2 | 2 | **1N5817** Schottky diode | | buy/have |
| C1 | 1 | 10 µF electrolytic, ≥ 25 V, 5 mm dia, 2 mm pitch | 35 V is fine | have? |
| C2 | 1 | 10 µF electrolytic, ≥ 16 V, 5 mm dia, 2 mm pitch | | have? |
| C3 | 1 | 100 nF ceramic, 2.5 mm pitch | | have? |
| R1, R2 | 2 | 47 Ω, ¼ W axial | SWD series resistors | have? |
| R3 | 1 | 1 kΩ, ¼ W axial | VTREF sense | have? |
| R4 | 0 | 1 kΩ | **do not fit** (nRESET, unused) | — |

## Panel
| Qty | Part | Notes |
|---|---|---|
| 2 | M3 rack screws (+ nylon washers) | usually come with the case |
