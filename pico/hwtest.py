# GRAINVIEW breadboard test: screen pattern + live encoder/button readout.
# Run from the Mac:  mpremote cp pico/ssd1327.py pico/pins.py :  &&  mpremote run pico/hwtest.py
# Ctrl-C to stop.
import time
from machine import Pin, SPI
import pins
from ssd1327 import SSD1327

# --- inputs ---
def inp(n):
    return Pin(n, Pin.IN, Pin.PULL_UP)

enc_a, enc_b, enc_sw = inp(pins.ENC_A), inp(pins.ENC_B), inp(pins.ENC_SW)
buttons = [(name, inp(gp)) for name, gp in pins.BUTTONS] + [("ENC PUSH", enc_sw)]

print("Idle pin levels (all should be 1):")
print("  ENC A", enc_a(), " ENC B", enc_b())
for name, p in buttons:
    print("  {:8s} {}".format(name, p()))

# --- screen ---
spi = SPI(pins.SPI_ID, baudrate=10_000_000, polarity=0, phase=0,
          sck=Pin(pins.SCR_SCK), mosi=Pin(pins.SCR_MOSI))
oled = SSD1327(spi, dc=Pin(pins.SCR_DC, Pin.OUT, value=0),
               cs=Pin(pins.SCR_CS, Pin.OUT, value=1),
               rst=Pin(pins.SCR_RST, Pin.OUT, value=1))

def draw(count, last):
    o = oled
    o.fill(0)
    o.rect(0, 0, 128, 128, 6)
    o.text("GRAINVIEW", 28, 6, 15)
    o.text("test", 48, 16, 8)
    o.text("ENC {:+d}".format(count), 8, 40, 15)
    o.text(last[:15], 8, 56, 12)
    for g in range(16):            # greyscale ramp 0..15
        o.fill_rect(4 + g * 7 + (g > 7), 100, 7, 18, g)
    o.show()

# --- encoder: Gray-code decoder, one step per detent (rest state A=B=1) ---
TRANS = (0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0)
prev = (enc_a() << 1) | enc_b()
acc = 0
count = 0
last = "ready"
draw(count, last)
print("Screen drawn. Turn the encoder and press buttons.")

state = {name: p() for name, p in buttons}
changed_at = {name: 0 for name, _ in buttons}
dirty = False
while True:
    cur = (enc_a() << 1) | enc_b()
    if cur != prev:
        acc += TRANS[(prev << 2) | cur]
        prev = cur
        if cur == 0b11:
            if acc >= 2:
                count += 1; last = "ENC CW"; dirty = True
            elif acc <= -2:
                count -= 1; last = "ENC CCW"; dirty = True
            acc = 0
            if dirty:
                print(last, count)
    now = time.ticks_ms()
    for name, p in buttons:
        v = p()
        if v != state[name] and time.ticks_diff(now, changed_at[name]) > 20:
            state[name] = v
            changed_at[name] = now
            last = name + (" down" if v == 0 else " up")
            print(last)
            dirty = True
    if dirty:
        draw(count, last)
        dirty = False
