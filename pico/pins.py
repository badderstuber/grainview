# GRAINVIEW breadboard pin map (Pico 2 WH). Source of truth: docs/PINMAP.md.
# All inputs are active-low with internal PULL-UPs (never pull-downs: RP2350 erratum E9).

# Screen: SSD1327 on SPI0
SPI_ID = 0
SCR_SCK = 18   # Clk
SCR_MOSI = 19  # Data
SCR_CS = 17
SCR_DC = 20
SCR_RST = 21

# Encoder (bare EC11, common to GND)
# Wired A->GP2, B->GP3, but this encoder counts CW as negative that way, so swapped here.
ENC_A = 3
ENC_B = 2
ENC_SW = 4

# Buttons, panel order top -> bottom
BUTTONS = (
    ("BACK", 6),
    ("VIEW", 7),
    ("FILE", 8),
    ("SOUND<", 9),
    ("SOUND>", 10),
    ("A/B", 11),
    ("SETUP", 12),
)

# Reserved: SWCLK 14, SWDIO 15 (swd.py defaults), VTREF sense 26 (ADC0), debug UART 0/1
