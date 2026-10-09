#!/usr/bin/env python3
"""Multigrain MIDI monitor.

Lists MIDI ports, auto-connects to the Multigrain (or a port you name),
and prints every incoming message with a timestamp, decoded.

Usage:
    python mg_monitor.py                 # list ports, then monitor best match
    python mg_monitor.py --port "Multigrain"
    python mg_monitor.py --list          # just list ports and exit
    python mg_monitor.py --no-clock      # hide MIDI clock (0xF8) spam

Move knobs/faders/buttons on the module and watch what it emits.
Ctrl-C to stop; a summary of what was seen is printed on exit.
"""
import argparse, sys, time
from collections import Counter
import rtmidi

CLOCK = 0xF8
STATUS = {
    0x80: "note_off", 0x90: "note_on", 0xA0: "poly_aftertouch",
    0xB0: "control_change", 0xC0: "program_change", 0xD0: "channel_aftertouch",
    0xE0: "pitch_bend",
}
SYSTEM = {
    0xF0: "sysex_start", 0xF1: "mtc_quarter", 0xF2: "song_position",
    0xF3: "song_select", 0xF6: "tune_request", 0xF7: "sysex_end",
    0xF8: "clock", 0xFA: "start", 0xFB: "continue", 0xFC: "stop",
    0xFE: "active_sensing", 0xFF: "reset",
}


def decode(msg):
    if not msg:
        return "(empty)"
    st = msg[0]
    hi, lo = st & 0xF0, st & 0x0F
    if st >= 0xF0:
        name = SYSTEM.get(st, f"system_0x{st:02X}")
        if st == 0xF0:
            return f"SYSEX {' '.join(f'{b:02X}' for b in msg)}"
        return name + (f" {msg[1:]}" if len(msg) > 1 else "")
    name = STATUS.get(hi, f"0x{hi:02X}")
    ch = lo + 1
    data = msg[1:]
    if hi == 0xB0 and len(msg) >= 3:
        return f"ch{ch:<2} control_change  CC#{msg[1]:<3} = {msg[2]}"
    if hi in (0x90, 0x80) and len(msg) >= 3:
        return f"ch{ch:<2} {name:<14} note={msg[1]:<3} vel={msg[2]}"
    if hi == 0xE0 and len(msg) >= 3:
        return f"ch{ch:<2} pitch_bend     {((msg[2] << 7) | msg[1]) - 8192:+d}"
    return f"ch{ch:<2} {name:<14} {data}"


def pick_port(ports, want):
    if want:
        for i, p in enumerate(ports):
            if want.lower() in p.lower():
                return i
        print(f"No port matching {want!r}. Available: {ports}", file=sys.stderr)
        sys.exit(1)
    for i, p in enumerate(ports):
        if "multigrain" in p.lower() or "intellijel" in p.lower():
            return i
    return 0 if ports else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--no-clock", action="store_true")
    args = ap.parse_args()

    midi_in = rtmidi.MidiIn()
    ports = midi_in.get_ports()
    print("Input ports:")
    for i, p in enumerate(ports):
        print(f"  [{i}] {p}")
    if args.list:
        return
    if not ports:
        print("\nNo MIDI input ports. Is the Multigrain plugged in via USB-C and powered?")
        return

    idx = pick_port(ports, args.port)
    print(f"\nMonitoring [{idx}] {ports[idx]}   (Ctrl-C to stop)\n")
    midi_in.open_port(idx)
    midi_in.ignore_types(sysex=False, timing=False, active_sense=False)

    seen = Counter()
    cc_values = {}
    t0 = time.time()
    try:
        while True:
            m = midi_in.get_message()
            if m is None:
                time.sleep(0.001)
                continue
            msg, _ = m
            st = msg[0]
            if st == CLOCK:
                seen["clock"] += 1
                if args.no_clock:
                    continue
            if (st & 0xF0) == 0xB0 and len(msg) >= 3:
                cc_values[msg[1]] = msg[2]
                seen[f"CC#{msg[1]}"] += 1
            else:
                seen[STATUS.get(st & 0xF0, SYSTEM.get(st, hex(st)))] += 1
            print(f"{time.time()-t0:8.3f}  {decode(msg)}")
    except KeyboardInterrupt:
        pass
    finally:
        midi_in.close_port()
        print("\n--- summary ---")
        for k, v in seen.most_common():
            print(f"  {k}: {v}")
        if cc_values:
            print("  last CC values:", dict(sorted(cc_values.items())))


if __name__ == "__main__":
    main()
