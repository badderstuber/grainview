# GRAINVIEW breadboard — pin map

_Decided 2026-10-13 (Leo + Claude). Board: **Pico 2 WH** (RP2350, wireless, headers fitted)._
Physical pin numbers count 1–20 down the left (USB at top), 21–40 up the right.

## Rules

- **All inputs active-low, internal PULL-UP.** Never use pull-downs: RP2350 erratum E9 can
  latch a pulled-down input at ~2 V.
- Screen on **SPI**, not I2C. A full 128×128 4-bit frame is 8 KB: I2C at 400 kHz gives ~5 fps,
  but SPI at 10 MHz sends it in ~7 ms. The grain animation needs SPI.
- GP23/24/25/29 are taken by the wireless chip (not on the header). LED = `Pin("LED")`.
- Run one GND pin to the breadboard's − rail. Every GND below goes to that rail.

## Screen — Adafruit 1.5" SSD1327 (SPI0, right side)

**Ships in I2C mode.** For SPI, cut the traces between the pads of **J1 and J2** on the back
(re-bridge with solder to go back to I2C). Header order: Data · Clk · DC/A0 · Rst · CS · 3Vo · VIN · GND.

| Screen pin | Pico GP | Phys pin | Notes |
|---|---|---|---|
| Data | GP19 | 25 | SPI0 TX (MOSI) |
| Clk | GP18 | 24 | SPI0 SCK |
| DC (A0) | GP20 | 26 | data/command (A0 = I2C address select, unused in SPI) |
| Rst | GP21 | 27 | |
| CS | GP17 | 22 | SPI0 CSn |
| 3Vo | — | — | 3.3 V **output** from the screen's regulator; leave empty |
| VIN | 3V3(OUT) | 36 | accepts 3–5 V; **not** VBUS/VSYS |
| GND | GND | 38 | |

Start SPI at 10 MHz (the SSD1327 is rated to 10 MHz); try higher later.

## Encoder — bare EC11 from the O&C kit (left side)

| Encoder leg | Pico GP | Phys pin |
|---|---|---|
| A (3-leg side, outer) | GP2 | 4 |
| C (3-leg side, middle) | GND | 3 |
| B (3-leg side, outer) | GP3 | 5 |
| SW (2-leg side) | GP4 | 6 |
| SW other leg | GND | rail |

With this wiring the O&C encoder counted CW as negative, so `pico/pins.py` swaps A/B in
software (ENC_A = 3, ENC_B = 2). Leave the wires as above.

## Buttons (left side, panel order top→bottom)

| Button | Pico GP | Phys pin |
|---|---|---|
| BACK | GP6 | 9 |
| VIEW | GP7 | 10 |
| FILE | GP8 | 11 |
| SOUND‹ | GP9 | 12 |
| SOUND› | GP10 | 14 |
| A/B | GP11 | 15 |
| SETUP | GP12 | 16 |

Each button: one leg → GP, the diagonally opposite leg → GND rail.
(4-leg tactiles are two internally joined pairs; using diagonal legs means you always get the switch.)

## Reserved (don't use for anything else)

| Function | Pico GP | Phys pin | Notes |
|---|---|---|---|
| SWCLK → Multigrain JTRACE | GP14 | 19 | PIO SWD master (Phase 3) |
| SWDIO ↔ Multigrain JTRACE | GP15 | 20 | |
| VTREF sense | GP26 / ADC0 | 31 | Multigrain 3.3 V present? 1 kΩ series resistor |
| Debug UART TX / RX | GP0 / GP1 | 1 / 2 | |

Spare: GP5, GP13, GP16, GP22, GP27, GP28.
