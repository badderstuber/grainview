#!/usr/bin/env python3
"""Multigrain MIDI prober.

Sends MIDI OUT to the module so you can watch its LEDs/behaviour react and
discover which messages it responds to. Pair with mg_monitor.py (run the
monitor in another terminal to capture anything echoed back).

Examples:
    python mg_probe.py --list
    python mg_probe.py --cc-sweep              # sweep every CC 0..127 on ch1
    python mg_probe.py --cc 10 --ramp          # ramp CC#10 0->127->0 slowly
    python mg_probe.py --notes                 # play notes 0..127
    python mg_probe.py --channels              # send a marker CC on every channel
    python mg_probe.py --clock 120             # send MIDI clock at 120 BPM (test SYNC)

Go slow and watch the module. When something moves, note the channel + CC/note.
"""
import argparse, sys, time
import rtmidi


def pick_port(midi_out, want):
    ports = midi_out.get_ports()
    print("Output ports:")
    for i, p in enumerate(ports):
        print(f"  [{i}] {p}")
    if not ports:
        print("\nNo MIDI output ports. Plug in the Multigrain and power it on.")
        sys.exit(1)
    if want:
        for i, p in enumerate(ports):
            if want.lower() in p.lower():
                return i
    for i, p in enumerate(ports):
        if "multigrain" in p.lower() or "intellijel" in p.lower():
            return i
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--ch", type=int, default=1, help="MIDI channel 1-16")
    ap.add_argument("--cc-sweep", action="store_true")
    ap.add_argument("--cc", type=int, help="single CC number to ramp")
    ap.add_argument("--ramp", action="store_true")
    ap.add_argument("--notes", action="store_true")
    ap.add_argument("--channels", action="store_true")
    ap.add_argument("--clock", type=float, metavar="BPM")
    ap.add_argument("--delay", type=float, default=0.25, help="seconds between steps")
    args = ap.parse_args()

    midi_out = rtmidi.MidiOut()
    if args.list:
        pick_port(midi_out, args.port)
        return
    idx = pick_port(midi_out, args.port)
    midi_out.open_port(idx)
    print(f"\nSending to [{idx}] {midi_out.get_ports()[idx]}  ch{args.ch}\n")
    ch = (args.ch - 1) & 0x0F
    d = args.delay

    try:
        if args.cc_sweep:
            print("Sweeping CC 0..127 (each to 127 then 0). Watch the module.")
            for cc in range(128):
                print(f"  CC#{cc} -> 127")
                midi_out.send_message([0xB0 | ch, cc, 127]); time.sleep(d)
                midi_out.send_message([0xB0 | ch, cc, 0]); time.sleep(d / 2)
        elif args.cc is not None and args.ramp:
            print(f"Ramping CC#{args.cc} 0->127->0")
            for v in list(range(0, 128, 4)) + list(range(127, -1, -4)):
                midi_out.send_message([0xB0 | ch, args.cc, v]); time.sleep(0.05)
        elif args.cc is not None:
            midi_out.send_message([0xB0 | ch, args.cc, 127])
            print(f"Sent CC#{args.cc}=127")
        elif args.notes:
            print("Playing notes 0..127")
            for n in range(128):
                print(f"  note {n}")
                midi_out.send_message([0x90 | ch, n, 100]); time.sleep(d)
                midi_out.send_message([0x80 | ch, n, 0]); time.sleep(d / 4)
        elif args.channels:
            print("Sending CC#1=127 on every channel 1..16")
            for c in range(16):
                print(f"  ch{c+1}")
                midi_out.send_message([0xB0 | c, 1, 127]); time.sleep(d)
                midi_out.send_message([0xB0 | c, 1, 0]); time.sleep(d / 2)
        elif args.clock:
            period = 60.0 / args.clock / 24.0  # 24 clocks per quarter note
            print(f"Sending MIDI clock at {args.clock} BPM (Ctrl-C to stop). Enable SYNC on the module.")
            midi_out.send_message([0xFA])  # start
            while True:
                midi_out.send_message([0xF8]); time.sleep(period)
        else:
            ap.print_help()
    except KeyboardInterrupt:
        pass
    finally:
        if args.clock:
            midi_out.send_message([0xFC])  # stop
        midi_out.close_port()
        print("\ndone.")


if __name__ == "__main__":
    main()
