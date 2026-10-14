# Minimal SSD1327 128x128 4-bit greyscale OLED driver, 4-wire SPI.
# Init sequence follows mcauser/micropython-ssd1327 (known good on 128x128 panels).
# The framebuffer is GS4_HMSB: colours 0 (off) .. 15 (brightest), 2 pixels per byte.
import framebuf
import time


class SSD1327(framebuf.FrameBuffer):
    def __init__(self, spi, dc, cs, rst, width=128, height=128):
        self.spi, self.dc, self.cs, self.rst = spi, dc, cs, rst
        self.width, self.height = width, height
        self.buffer = bytearray(width * height // 2)
        super().__init__(self.buffer, width, height, framebuf.GS4_HMSB)
        self.reset()
        self.init_display()

    def reset(self):
        self.rst(1)
        time.sleep_ms(1)
        self.rst(0)
        time.sleep_ms(10)
        self.rst(1)
        time.sleep_ms(20)

    def cmd(self, *b):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytes(b))
        self.cs(1)

    def init_display(self):
        for c in (
            (0xFD, 0x12),        # unlock commands
            (0xAE,),             # display off
            (0xA1, 0x00),        # start line
            (0xA2, 0x00),        # display offset
            (0xA0, 0x51),        # segment remap (orientation; tweak here if mirrored/flipped)
            (0xA8, self.height - 1),  # mux ratio
            (0xAB, 0x01),        # internal VDD regulator on
            (0xB1, 0x51),        # phase lengths
            (0xB3, 0x01),        # clock divide
            (0xBC, 0x08),        # pre-charge voltage
            (0xBE, 0x07),        # VCOMH
            (0xB6, 0x01),        # second pre-charge period
            (0xD5, 0x62),        # function select B
            (0xB9,),             # linear greyscale table
            (0x81, 0x7F),        # contrast
            (0xA4,),             # normal display
            (0x2E,),             # scrolling off
        ):
            self.cmd(*c)
        self.fill(0)
        self.show()
        self.cmd(0xAF)           # display on

    def contrast(self, v):
        self.cmd(0x81, v & 0xFF)

    def invert(self, on):
        self.cmd(0xA7 if on else 0xA4)

    def poweroff(self):
        self.cmd(0xAE)

    def show(self):
        self.show_rows(0, self.height)

    def show_rows(self, r0, n):
        """Send rows r0..r0+n-1 of the buffer to the panel."""
        bpr = self.width // 2                    # bytes per row (2 px per byte)
        self.cmd(0x15, 0, bpr - 1)               # column address
        self.cmd(0x75, r0, r0 + n - 1)           # row address
        self.dc(1)
        self.cs(0)
        self.spi.write(memoryview(self.buffer)[r0 * bpr:(r0 + n) * bpr])
        self.cs(1)
