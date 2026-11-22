# Live Sounds + the recorder on the Pico, over SWD (swd.py) - ports of tools/mg_rec.py's
# set_live / rec_do (hardware-tested 2026-10-21/22; spec docs/RECORDER.md).
#
#   set_live(s, n, on)     sound n (0-7) -> Live / sample, as the panel's SOUND + SAMPLE:
#                          the Live record's setter (live mask, recorder -> looper and back,
#                          autosave), + an empty sound gets the default Live / Sound record
#   rec_do(s, action, n)   press | save | grab | assign (n) | discard: the Home page's own
#                          SAMPLE / SOUND handlers, argument FIXED, each only in its state
import struct

import mg_map as M
from mgfile import inject, u8
from mgpoll import base, phase


def set_live(s, n, on):
    if not 0 <= n < 8:
        raise ValueError("sound must be 1..8")
    rec = base(n) + M.LIVE_REC
    if s.read32(rec) != M.LIVE_VPTR:
        raise ValueError("S%d: Live record not found" % (n + 1))
    v = 1 if on else 0
    if u8(s, rec + 0x15) == v:
        return
    sd = s.read32(M.SD_STATE)
    if sd != 0:
        raise ValueError("SD busy" if sd == 1 else "SD error / no card")
    empty = s.read32(M.AUDIO_LEN + n * 0x10) == 0
    if v and empty:
        inject(s, M.LIVE_DEFAULTS_FN, (n, 1))  # (sets the flag through the setter too)
    inject(s, M.LIVE_SET_FN, (rec, v))
    if not v and empty:
        inject(s, M.LIVE_DEFAULTS_FN, (n, 0))


def i32(s, a):
    return struct.unpack("<i", s.read_block8(a, 4))[0]


def rec_do(s, action, n=None):
    """mg_rec.rec_do: raises ValueError (nothing done) unless the recorder is in the state
    where that handler does what we want."""
    if s.read32(M.PAGE) != M.HOME:
        raise ValueError("module not on its home page")
    sd = s.read32(M.SD_STATE)
    if sd != 0 or s.read32(M.SAVE_REQ):
        raise ValueError("SD busy" if sd in (0, 1) else "SD error / no card")
    mode, state, take = u8(s, M.REC_MODE), i32(s, M.REC_STATE), i32(s, M.REC_TAKE)
    ph = phase(mode, state, take)
    if action in ("save", "assign") and i32(s, M.HOME_BLINK):
        raise ValueError("just saved - try again")
    if action == "press":                     # start / stop / disarm; looper freeze / unfreeze
        if ph == "pending":
            raise ValueError("a take is waiting")
        inject(s, M.SAMPLE_CLICK_FN, (M.HOME, 0))
    elif action == "save":
        if ph != "pending":
            raise ValueError("nothing to save")
        inject(s, M.SAMPLE_CLICK_FN, (M.HOME, 0))
    elif action == "grab":                    # sampler: last 32 s; looper: freeze + the loop
        if ph == "pending" or mode != 2 and state not in (1, 3):
            raise ValueError("nothing to grab now")
        inject(s, M.SAMPLE_LONG_FN, (M.HOME, 0))
    elif action == "assign":
        if n is None or not 0 <= n < 8:
            raise ValueError("sound must be 1..8")
        if ph != "pending":
            raise ValueError("nothing to assign")
        if s.read32(M.LIVE_MASK) >> n & 1 or s.read32(M.AUDIO_LEN + n * 0x10):
            raise ValueError("S%d isn't empty" % (n + 1))
        inject(s, M.SOUND_DOWN_FN, (M.HOME, n))
    elif action == "discard":
        if ph != "pending":
            raise ValueError("nothing to discard")
        if s.read32(M.CLEAR + 4) == 0:        # (+4 == button: that call would only reset it)
            raise ValueError("clear page busy - try again")
        s.write32(M.CLEAR + 8, 0)             # SAMPLE armed, as after its 1st press
        inject(s, M.CLEAR_FN, (M.CLEAR, 0))
        inject(s, M.CLEAR_LEAVE_FN, ())
    else:
        raise ValueError("unknown recorder action")
