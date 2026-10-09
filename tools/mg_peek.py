#!/usr/bin/env python3
"""mg_peek.py - read the Multigrain's LIVE RAM over SWD via an ST-Link, WITHOUT
halting the running firmware.

The Cortex-M7 debug access port services memory reads in the background through
the AHB-AP, so we attach (no reset, no halt) and the granular engine keeps
running - audio never stops while we observe. This is the foundation of the
"screen" / live-mirror idea: find where a parameter lives in RAM, then poll it.

Hardware hookup. JTRACE is a 1.27mm-pitch ARM CoreSight-20 (Debug+Trace) header
(~13mm long, 2x10). ST-Link V2 clone -> JTRACE; module powered by its rack:
    ST-Link SWDIO -> JTRACE pin 2
    ST-Link SWCLK -> JTRACE pin 4
    ST-Link GND   -> JTRACE pin 3 (or 5)
    (SWO -> pin 6 only if you later want ITM trace; nRESET -> pin 10 if needed)
CoreSight-20 pinout: 1=VTREF 2=SWDIO 3=GND 4=SWCLK 5=GND 6=SWO 9=GNDDetect
10=nRESET 12=TRACECLK 14/16/18/20=TRACEDATA0-3; other odd pins GND.
Do NOT power the module from the ST-Link - it already has rack power. Only if
the probe refuses to detect target voltage, connect ST-Link 3V3 -> JTRACE pin 1
(VTREF). Verify pin 1 ~3.3V and GND pins with a multimeter first.

Usage:
    tools/venv/bin/python tools/mg_peek.py --probes            # list ST-Links
    tools/venv/bin/python tools/mg_peek.py 0x24000000          # one u32
    tools/venv/bin/python tools/mg_peek.py 0x24000000 -n 64    # hexdump 64 bytes
    tools/venv/bin/python tools/mg_peek.py 0x24000000 --float  # as float32
    tools/venv/bin/python tools/mg_peek.py 0x24000000 -n 256 --watch 0.1
    tools/venv/bin/python tools/mg_peek.py --scan 0x24000000 0x8000
        -> snapshot a region, you move ONE knob, Enter, it diffs -> the changed
           offsets are where that parameter lives. (RAM analog of the preset diff.)

Target is left generic ("cortex_m") so no CMSIS pack is needed for read-only
access, and it works whether the MCU is an STM32H753 or H7B52.

STM32H7 RAM regions worth scanning (external SDRAM is where big buffers live):
    0x20000000 DTCM (128K)   0x24000000 AXI-SRAM (512K)
    0x30000000 SRAM1-3       0x38000000 SRAM4
    0x60000000/0xC0000000    external SDRAM (FMC) - check the map
"""
import argparse
import struct
import sys
import time


def parse_addr(s):
    return int(s, 0)


def connect(freq_hz):
    from pyocd.core.helpers import ConnectHelper
    session = ConnectHelper.session_with_chosen_probe(
        blocking=False,
        options={
            "target_override": "cortex_m",   # generic: no pack, read-only safe
            "connect_mode": "attach",        # DON'T reset/halt - keep audio running
            "frequency": freq_hz,
            "resume_on_disconnect": False,
        },
    )
    if session is None:
        sys.exit("No ST-Link found. Plug it in, check wiring, run --probes.")
    session.open()
    return session


def list_probes():
    from pyocd.core.helpers import ConnectHelper
    probes = ConnectHelper.get_all_connected_probes(blocking=False)
    if not probes:
        print("No debug probes found. Is the ST-Link plugged into the Mac?")
        return
    for p in probes:
        print(f"  {p.unique_id}  {p.description}")


def read_bytes(target, addr, n):
    return bytes(target.read_memory_block8(addr, n))


def hexdump(addr, data, prev=None):
    out = []
    for i in range(0, len(data), 16):
        chunk = data[i:i + 16]
        hexs = []
        for j, b in enumerate(chunk):
            changed = prev is not None and (i + j) < len(prev) and prev[i + j] != b
            hexs.append(f"\033[33m{b:02x}\033[0m" if changed else f"{b:02x}")
        asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        out.append(f"{addr + i:08x}  {' '.join(hexs):<48}  {asc}")
    return "\n".join(out)


def decode_word(data):
    u = struct.unpack("<I", data[:4])[0]
    i = struct.unpack("<i", data[:4])[0]
    f = struct.unpack("<f", data[:4])[0]
    return f"u32={u}  (0x{u:08x})  i32={i}  f32={f!r}"


def cmd_scan(target, addr, length):
    print(f"Snapshot of {length} bytes @ 0x{addr:08x} ...")
    a = read_bytes(target, addr, length)
    input("Now change exactly ONE parameter on the module, then press Enter...")
    b = read_bytes(target, addr, length)
    changed = [off for off in range(length) if a[off] != b[off]]
    if not changed:
        print("No bytes changed in this region. Try a different/larger region,")
        print("or the parameter lives elsewhere (scan SDRAM / another SRAM bank).")
        return
    # group contiguous runs
    runs = []
    s = p = changed[0]
    for off in changed[1:]:
        if off <= p + 3:
            p = off
        else:
            runs.append((s, p))
            s = p = off
    runs.append((s, p))
    print(f"\n{len(changed)} byte(s) changed, in {len(runs)} region(s):")
    for s, e in runs:
        wa = addr + s
        w = b[s:e + 4].ljust(4, b"\x00")[:4]
        oa = a[s:e + 4].ljust(4, b"\x00")[:4]
        print(f"  +0x{s:04x}  @0x{wa:08x}  {oa.hex()} -> {w.hex()}   {decode_word(w)}")
    print("\nThat offset is a strong candidate for the parameter you moved.")


def main():
    ap = argparse.ArgumentParser(description="Read live Multigrain RAM over SWD (no halt).")
    ap.add_argument("addr", nargs="?", type=parse_addr, help="address (hex 0x.. or dec)")
    ap.add_argument("-n", "--count", type=int, default=4, help="bytes to read (default 4)")
    ap.add_argument("--float", action="store_true", help="also show float32 for the first word")
    ap.add_argument("--watch", type=float, metavar="SEC", help="poll every SEC, highlight changes")
    ap.add_argument("--scan", nargs=2, metavar=("ADDR", "LEN"),
                    help="diff a region before/after you move one knob")
    ap.add_argument("--probes", action="store_true", help="list connected probes and exit")
    ap.add_argument("--freq", type=int, default=4_000_000, help="SWD clock Hz (default 4e6)")
    args = ap.parse_args()

    if args.probes:
        list_probes()
        return

    if not args.scan and args.addr is None:
        ap.error("give an address, or --scan ADDR LEN, or --probes")

    session = connect(args.freq)
    try:
        target = session.target
        if args.scan:
            cmd_scan(target, parse_addr(args.scan[0]), parse_addr(args.scan[1]))
            return

        if args.watch:
            prev = None
            print(f"Polling 0x{args.addr:08x} ({args.count}B) every {args.watch}s. Ctrl-C to stop.")
            try:
                while True:
                    data = read_bytes(target, args.addr, args.count)
                    sys.stdout.write("\033[H\033[J")  # clear
                    print(hexdump(args.addr, data, prev))
                    if args.count >= 4:
                        print("\n" + decode_word(data))
                    prev = data
                    time.sleep(args.watch)
            except KeyboardInterrupt:
                print("\nstopped.")
            return

        data = read_bytes(target, args.addr, args.count)
        if args.count <= 4:
            print(f"0x{args.addr:08x}: {data.hex()}   {decode_word(data.ljust(4, b'0'))}")
        else:
            print(hexdump(args.addr, data))
            if args.count >= 4:
                print("\nfirst word: " + decode_word(data))
    finally:
        session.close()


if __name__ == "__main__":
    main()
