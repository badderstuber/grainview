# Raw encoder diagnostic: prints every change of the A/B pins for 60 s.
# Run from the Mac:  mpremote run pico/enc_raw.py
import time
from machine import Pin
import pins

a = Pin(pins.ENC_A, Pin.IN, Pin.PULL_UP)
b = Pin(pins.ENC_B, Pin.IN, Pin.PULL_UP)
prev = None
changes = 0
t_end = time.ticks_add(time.ticks_ms(), 60_000)
print("Turn the encoder slowly. A B levels:")
while time.ticks_diff(t_end, time.ticks_ms()) > 0:
    cur = (a(), b())
    if cur != prev:
        print("A={} B={}".format(*cur))
        prev = cur
        changes += 1
print("done,", changes - 1, "changes")
