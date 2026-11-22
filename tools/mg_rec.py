#!/usr/bin/env python3
"""mg_rec.py - Live Sounds and the recorder over SWD. Spec: docs/RECORDER.md.

A sound's Live flag is a reactive record at sound+0x930 (value byte +0x945). Its setter
FUN_0800c320(rec, v) runs the change callback FUN_0800d7a4, which keeps the live mask
(STATE+0x40) and switches the recorder to the Looping Recorder when the first Live Sound
appears (back when the last goes), and sets the autosave flag - so a raw poke of +0x945
is NOT enough. The panel (SOUND + SAMPLE, or the ALT page) also gives an EMPTY sound the
default Live Sound / default Sound record (FUN_08012494(n, v)); we do the same:
    on:  empty -> FUN_08012494(n, 1);  setter(rec, 1)
    off: setter(rec, 0);  empty -> FUN_08012494(n, 0)
"empty" = no sample (u32 mg_load.AUDIO_LEN + n*0x10 == 0). One short halt per call, no SD.
Turning the first Live Sound on (or the last off) re-points the recorder: a pending
take / the Always-Listening audio is lost - as on the panel.

The recorder (object R = 0x20000468, state R+0x28): the actions are the Home page's own
SAMPLE / SOUND handlers, called with a FIXED argument (another argument = another button:
THRU / LATCH, preset load / save...). Each refuses unless the module is on its Home page,
the SD card is idle and no save is queued - and unless the recorder is in the state where
that handler does what we want (else e.g. the long press opens the Advanced Sampling page,
a SOUND press selects / copies sounds):
    press    FUN_08033ab0(home, 0)   SAMPLE click: start (arm) / stop / disarm; looper freeze
    save     same call, pending       -> /Recs (the UI task writes the WAV a moment later)
    grab     FUN_080331ac(home, 0)   SAMPLE long: Always Listening (states 1/3) / the loop
    assign   FUN_08034a70(home, n)   SOUND n: pending + empty sound n -> save + assign
    discard  clear page: arm (+8 = 0), FUN_0803240c(clr, 0) = SAMPLE, FUN_080314a0() = leave
The WAV write runs in the module's main loop (up to ~6 MB for 32 s): no calls until the SD
state is back to 0 (status()["busy"]).

Usage:
    tools/venv/bin/python tools/mg_rec.py                 # status (read-only)
    tools/venv/bin/python tools/mg_rec.py --live 3 on     # sound 3 -> Live (1-8)
    tools/venv/bin/python tools/mg_rec.py --live 3 off
    tools/venv/bin/python tools/mg_rec.py --rec press|save|grab|discard
    tools/venv/bin/python tools/mg_rec.py --rec assign --sound 3
    ... --swd pico                                         # through GRAINVIEW, no ST-Link
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
import mg_load as L  # noqa: E402

LIVE_REC = 0x930              # sound + : the Live record (vptr, std::function, value +0x15)
LIVE_OFF = LIVE_REC + 0x15    # u8 0/1 = sound+0x945
LIVE_VPTR = 0x0805C668        # the record's vtable; [0] = the setter
LIVE_SET_FN = 0x0800C320      # setter(rec, v): store + change callback (FUN_0800d7a4)
LIVE_DEFAULTS_FN = 0x08012494  # (n, v): sound n <- Settings' default Live Sound (1) / Sound (0)
LIVE_MASK = L.STATE + 0x40    # u32 bit n = sound n is Live (mg_load's EMPTY_MASK)
REC_MODE = 0x20000454         # u8 recorder: 0 sample in, 1 resample, 2 looper
# the recorder object R (FUN_080129a8)
REC = 0x20000468
REC_SIZE = REC + 0x04         # i32 ring frames (32 s sampler / the looper's 8-32 s)
REC_STATE = REC + 0x28        # i32 state, see phase()
REC_FILL = REC + 0x34         # i32 frames in memory (Always Listening / the loop)
REC_TAKE = REC + 0x58         # i32 take length, frames (counts up while recording)
REC_RATE = 48000
TAKE_MIN = 4800               # 0.1 s: a take this long = something to save
LOOP_SIZE = 0x20000458        # i32 looper length, frames
SLOTS_END = L.AUDIO_LEN + 8 * 0x10   # one read REC_MODE.. covers R + the sounds' sample lengths
SAVE_REQ = 0x24020B44         # u32 bit0 = basic save queued (the UI task clears it)
PAGE = 0x20008CC0             # current UI page object
HOME = 0x24020B48             # the Home page
HOME_BLINK = HOME + 0x14      # i32 save-blink countdown: a save while != 0 is ignored
CLEAR = 0x240451EC            # the Clear page (+8 = SAMPLE armed: 0)
SAMPLE_CLICK_FN = 0x08033AB0  # (home, button) - button 0 = SAMPLE only
SAMPLE_LONG_FN = 0x080331AC   # (home, button) - button 0 = SAMPLE only
SOUND_DOWN_FN = 0x08034A70    # (home, n)
CLEAR_FN = 0x0803240C         # (clear, button) - button 0 = SAMPLE (1 = load Init preset!)
CLEAR_LEAVE_FN = 0x080314A0   # () - restart listening when memory is empty


def live_status(t):
    mask = L.u32(t, LIVE_MASK)
    sounds = [{"live": L.u8(t, L.SOUND_BASE + n * L.SOUND_STRIDE + LIVE_OFF),
               "empty": L.u32(t, L.AUDIO_LEN + n * 0x10) == 0} for n in range(8)]
    return {"mask": mask, "mode": L.u8(t, REC_MODE), "sounds": sounds}


def phase(mode, state, take):
    """The recorder in words: sampler idle / listen / armed / rec / stop / pending; looper
    loop (recording) / frozen / wait (auto-frozen) / pending."""
    pending = state == 0 and take >= TAKE_MIN
    if pending:
        return "pending"
    if mode == 2:
        return {0: "frozen", 1: "wait", 4: "frozen"}.get(state, "loop")
    return {0: "idle", 5: "armed", 6: "rec", 7: "rec"}.get(state, "listen")


def rec_status(t):
    mode, state, take = L.u8(t, REC_MODE), L.i32(t, REC_STATE), L.i32(t, REC_TAKE)
    return {"mode": mode, "state": state, "phase": phase(mode, state, take),
            "take": take, "fill": L.i32(t, REC_FILL), "size": L.i32(t, REC_SIZE),
            "home": L.u32(t, PAGE) == HOME, "sd": L.u32(t, L.SD_STATE),
            "queued": L.u32(t, SAVE_REQ) != 0, "blink": L.i32(t, HOME_BLINK)}


def rec_snapshot(t):
    """The recorder for /state (+ the sounds a take can go to: no sample, not Live)."""
    blk = bytes(t.read_memory_block8(REC_MODE, SLOTS_END - REC_MODE))
    i32 = lambda a: int.from_bytes(blk[a - REC_MODE:a - REC_MODE + 4], "little", signed=True)  # noqa: E731
    mode, state, take = blk[0], i32(REC_STATE), i32(REC_TAKE)
    mask = L.u32(t, LIVE_MASK)
    return {"mode": mode, "state": state, "phase": phase(mode, state, take), "take": take,
            "fill": i32(REC_FILL), "size": i32(REC_SIZE),
            "free": [n for n in range(8) if not (mask >> n & 1 or i32(L.AUDIO_LEN + n * 0x10))]}


def rec_ready(st, save=False):
    if not st["home"]:
        raise ValueError("module not on its home page")
    if st["sd"] != 0 or st["queued"]:
        raise ValueError("SD busy" if st["sd"] in (0, 1) else "SD error / no card")
    if save and st["blink"] != 0:
        raise ValueError("just saved - try again")


def rec_do(t, action, n=None):
    """One recorder action (see the module doc); raises ValueError (nothing done) if the
    recorder isn't in the state for it."""
    st = rec_status(t)
    ph, looper = st["phase"], st["mode"] == 2
    if action == "press":                     # start / stop / disarm; looper freeze / unfreeze
        rec_ready(st)
        if ph == "pending":
            raise ValueError("a take is waiting: save, assign or discard it")
        call(t, SAMPLE_CLICK_FN, (HOME, 0))
    elif action == "save":
        rec_ready(st, save=True)
        if ph != "pending":
            raise ValueError("nothing to save")
        call(t, SAMPLE_CLICK_FN, (HOME, 0))
    elif action == "grab":                    # sampler: last 32 s; looper: freeze + the loop
        rec_ready(st)
        if ph == "pending" or not looper and st["state"] not in (1, 3):
            raise ValueError("nothing to grab now" if ph != "pending" else "a take is waiting")
        call(t, SAMPLE_LONG_FN, (HOME, 0))
    elif action == "assign":
        rec_ready(st, save=True)
        if n not in range(8):
            raise ValueError("sound must be 0-7")
        if ph != "pending":
            raise ValueError("nothing to assign")
        if L.u32(t, LIVE_MASK) >> n & 1 or L.u32(t, L.AUDIO_LEN + n * 0x10):
            raise ValueError("S%d isn't empty" % (n + 1))
        call(t, SOUND_DOWN_FN, (HOME, n))
    elif action == "discard":
        rec_ready(st)
        if ph != "pending":
            raise ValueError("nothing to discard")
        if L.u32(t, CLEAR + 4) == 0:          # (+4 == button: that call would only reset it)
            raise ValueError("clear page busy - try again")
        t.write_memory(CLEAR + 8, 0)          # SAMPLE armed, as after its 1st press
        call(t, CLEAR_FN, (CLEAR, 0))
        call(t, CLEAR_LEAVE_FN, ())
    else:
        raise ValueError("unknown recorder action %r" % action)


def call(t, func, args):
    xpsr = L.wait_idle_and_halt(t)
    if not xpsr:
        raise RuntimeError("couldn't catch the CPU in the idle loop - nothing called")
    L.call_returning_to_idle(t, xpsr, func, args)


def set_live(t, n, on):
    """Sound n (0-7) -> Live (on) / sample (off), as the panel's toggle. No-op if already."""
    if n not in range(8):
        raise ValueError("sound must be 0-7")
    rec = L.SOUND_BASE + n * L.SOUND_STRIDE + LIVE_REC
    if L.u32(t, rec) != LIVE_VPTR:
        raise ValueError("sound %d: Live record not where expected - nothing called" % (n + 1))
    v = 1 if on else 0
    if L.u8(t, rec + 0x15) == v:
        return
    sd = L.u32(t, L.SD_STATE)
    if sd != 0:
        raise ValueError("SD busy" if sd == 1 else "SD error / no card")
    empty = L.u32(t, L.AUDIO_LEN + n * 0x10) == 0
    if v and empty:
        call(t, LIVE_DEFAULTS_FN, (n, 1))     # (sets the flag through the setter too)
    call(t, LIVE_SET_FN, (rec, v))
    if not v and empty:
        call(t, LIVE_DEFAULTS_FN, (n, 0))


def main():
    ap = argparse.ArgumentParser(description="Live Sounds over SWD (docs/RECORDER.md).")
    ap.add_argument("--live", nargs=2, metavar=("SOUND", "on|off"),
                    help="sound 1-8 -> Live on / off (panel-equivalent)")
    ap.add_argument("--rec", choices=("press", "save", "grab", "assign", "discard"),
                    help="recorder action (docs/RECORDER.md)")
    ap.add_argument("--sound", type=int, choices=range(1, 9), metavar="1-8", help="--rec assign")
    ap.add_argument("--swd", choices=("stlink", "pico"), default="stlink",
                    help="pico = through GRAINVIEW's USB (pico/main.py running)")
    a = ap.parse_args()
    if a.swd == "pico":
        import gv_pico
        link = gv_pico.PicoLink(None, log=lambda *x: None)
        for _ in range(50):
            if link.ser is not None:
                break
            time.sleep(0.1)
        t, session = gv_pico.PicoTarget(link), None
        t.connect()                           # (the Pico keeps polling afterwards)
    else:
        session = L.connect(4_000_000)
        t = session.target
    try:
        if session is not None and not L.fw_ok(t):   # (the Pico checks it itself and
                                                      # refuses writes / halts otherwise)
            raise SystemExit("not Multigrain %s firmware - hands off" % L.FW_VERSION)
        if a.live:
            n, v = int(a.live[0]) - 1, a.live[1].lower()
            if v not in ("on", "off"):
                raise SystemExit("on or off")
            set_live(t, n, v == "on")
            time.sleep(0.1)
        if a.rec:
            rec_do(t, a.rec, a.sound - 1 if a.sound else None)
            time.sleep(0.1)
        st = live_status(t)
        print("recorder mode %d (%s), live mask 0x%02x" % (
            st["mode"], {0: "sample", 1: "resample", 2: "looper"}.get(st["mode"], "?"), st["mask"]))
        for n, s in enumerate(st["sounds"]):
            print("  S%d  %s%s" % (n + 1, "LIVE  " if s["live"] else "sample",
                                  "  (empty)" if s["empty"] else ""))
        r = rec_status(t)
        print("recorder: %s (state %d), take %.2f s, memory %.1f / %.1f s, home page %s, "
              "sd %d, queued %s, blink %d" % (
                  r["phase"], r["state"], r["take"] / REC_RATE, r["fill"] / REC_RATE,
                  r["size"] / REC_RATE, r["home"], r["sd"], r["queued"], r["blink"]))
    finally:
        if session is not None:
            session.close()


if __name__ == "__main__":
    main()
