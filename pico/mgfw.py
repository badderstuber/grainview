# Firmware check: every address in mg_map.py is for one Multigrain build, so before GRAINVIEW
# polls or writes anything it hashes the module's flash image and compares (mg_load.FW_*,
# no version string in the image). ~2 s for the 620 KB at 8 MHz SWCLK, so main.py does it a
# chunk per loop pass and the panel stays live meanwhile.
#
#   c = Check()
#   r = c.step(swd)        # None while hashing, then True (FW_VERSION) / False (another build)
import binascii
import hashlib

import mg_map as M

CHUNK = 4096                                  # ~12 ms of SWD per step
DHCSR, S_RESET_ST = 0xE000EDF0, 1 << 25       # sticky: the core reset since the last read


class Check:
    def __init__(self):
        self.a, self.h = M.FW_BASE, hashlib.sha256()

    def step(self, s):
        end = M.FW_BASE + M.FW_SIZE
        n = min(CHUNK, end - self.a)
        self.h.update(s.read_block8(self.a, n))
        self.a += n
        if self.a < end:
            return None
        return binascii.hexlify(self.h.digest()).decode() == M.FW_SHA256


def was_reset(s):
    """The module rebooted since we last looked (a reflash would): check it again."""
    return bool(s.read32(DHCSR) & S_RESET_ST)
