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
import json
import os
import struct
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


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


def _group(offs):
    """Group sorted offsets into contiguous-ish runs (gap <= 3)."""
    runs, s, p = [], offs[0], offs[0]
    for off in offs[1:]:
        if off <= p + 3:
            p = off
        else:
            runs.append((s, p))
            s = p = off
    runs.append((s, p))
    return runs


def _report(addr, before, after, offs):
    offs = sorted(offs)
    runs = _group(offs)
    print(f"\n{len(offs)} byte(s) in {len(runs)} region(s):")
    for s, e in runs:
        wa = addr + s
        w = after[s:e + 4].ljust(4, b"\x00")[:4]
        oa = before[s:e + 4].ljust(4, b"\x00")[:4]
        print(f"  +0x{s:04x}  @0x{wa:08x}  {oa.hex()} -> {w.hex()}   {decode_word(w)}")


def cmd_scan(target, addr, length):
    print(f"Snapshot of {length} bytes @ 0x{addr:08x} ...")
    a = read_bytes(target, addr, length)
    input("Now change exactly ONE parameter on the module, then press Enter...")
    b = read_bytes(target, addr, length)
    changed = [off for off in range(length) if a[off] != b[off]]
    if not changed:
        print("No bytes changed. Try a different region (params may be in DTCM "
              "0x20000000 or SRAM1 0x30000000, not the audio buffers).")
        return
    _report(addr, a, b, changed)
    print("\nNote: in a running region this includes audio/counter noise. "
          "Use --find to filter it out.")


def cmd_find(target, addr, length, rounds, settle):
    """Noise-robust parameter locator.

    Per round: two snapshots while the knob is HELD STILL (bytes that differ =
    noise, discarded), then one after you MOVE the knob (of the still-stable
    bytes, those that changed are candidates). Intersect candidates across
    rounds. Audio/counters can't pass; a stored control value does.
    """
    candidates = None
    before = after = None
    for r in range(rounds):
        print(f"\n[round {r + 1}/{rounds}] Hold the target parameter STILL...")
        a1 = read_bytes(target, addr, length)
        time.sleep(settle)
        a2 = read_bytes(target, addr, length)
        stable = {i for i in range(length) if a1[i] == a2[i]}
        print(f"  filtered {length - len(stable)} noisy byte(s); {len(stable)} stable.")
        input("  Now MOVE that one parameter, then press Enter...")
        b = read_bytes(target, addr, length)
        changed = {i for i in stable if a2[i] != b[i]}
        print(f"  {len(changed)} stable byte(s) changed after the move.")
        candidates = changed if candidates is None else (candidates & changed)
        before, after = a2, b
        print(f"  candidates so far: {len(candidates)}")
        if not candidates:
            print("  Nothing consistent - try another region or hold stiller.")
            return
    print("\n=== Candidate parameter location(s) ===")
    _report(addr, before, after, candidates)
    print("\nStrong candidate(s) for the parameter you moved. Add the address + "
          "type to tools/mg_addrs.json.")


DEFAULT_NAMES = "START,WRAP,SCAN,SHAPE,BLUR,LEVEL,RATE,SIZE,PITCH,TONE,MORPH"


MAP_SETTLE = 1.5   # seconds to let smoothing settle before each snapshot


def _changed_words(a, b, length):
    return {(o // 4) * 4 for o in range(length) if a[o] != b[o]}


def cmd_map(target, addr, length, names, out):
    """Guided per-knob mapping, robust to the scratch register AND smoothing.

    Take a snapshot after each knob move (plus one extra at the end). A knob's
    dedicated slot CHANGES when you move it but is STABLE when you move the NEXT
    knob. The shared scratch and still-settling smoothed copies keep changing on
    the next move too - so (changed now) AND (NOT changed on the next move)
    isolates the real slot.
    """
    print("\nGuided mapping. For EACH parameter: move ONLY that knob a BIG amount,")
    print("let go, then press Enter. 's'+Enter skips. Move nothing else.\n")
    snaps = [read_bytes(target, addr, length)]     # S0 baseline
    moved = []
    for name in names:
        r = input(f"  move {name:6} -> Enter (or 's' to skip): ").strip().lower()
        time.sleep(MAP_SETTLE)                      # let smoothing settle first
        snaps.append(read_bytes(target, addr, length))
        moved.append(r != "s")
        if moved[-1]:
            print(f"    {len(_changed_words(snaps[-2], snaps[-1], length))} word(s) changed")
    input("  Finally, nudge ANY knob once more, then Enter (to close out the last): ")
    time.sleep(MAP_SETTLE)
    snaps.append(read_bytes(target, addr, length))

    def score(word):
        f = struct.unpack("<f", word)[0]
        s = 2 if (f == f and abs(f) <= 4.0) else 0
        if word[3] in (0x3e, 0x3f, 0xbe, 0xbf, 0x00, 0x80):
            s += 1
        return s

    assigned, mapping = set(), []
    for i, name in enumerate(names, start=1):
        if not moved[i - 1]:
            continue
        changed = _changed_words(snaps[i - 1], snaps[i], length)
        nxt = _changed_words(snaps[i], snaps[i + 1], length)
        cands = [w for w in (changed - nxt) if w not in assigned]
        if not cands:
            print(f"  {name:6}: no stable slot found (try again, bigger move)")
            continue
        cur = snaps[i]
        best = max(cands, key=lambda w: score(cur[w:w + 4].ljust(4, b"\x00")[:4]))
        assigned.add(best)
        word = cur[best:best + 4].ljust(4, b"\x00")[:4]
        f = struct.unpack("<f", word)[0]
        u = struct.unpack("<I", word)[0]
        a = addr + best
        typ, lo, hi = "f32", 0, 1
        if not (f == f and abs(f) <= 1e6):
            if u < 256:
                typ, hi = "u8", 7
        if typ == "f32" and f < -0.001:
            lo = -1
        mapping.append({"name": name, "addr": f"0x{a:08x}", "type": typ,
                        "min": lo, "max": hi})
        extra = f"  ({len(cands)} candidates)" if len(cands) > 1 else ""
        print(f"  {name:6} = 0x{a:08x}  now={f:.4f}  type={typ}{extra}")

    if out and mapping:
        with open(out, "w") as fo:
            json.dump(mapping, fo, indent=2)
        print(f"\nWrote {len(mapping)} params -> {out}")
        print("Verify with: tools/venv/bin/python tools/mg_mirror.py")
    return mapping


def main():
    ap = argparse.ArgumentParser(description="Read live Multigrain RAM over SWD (no halt).")
    ap.add_argument("addr", nargs="?", type=parse_addr, help="address (hex 0x.. or dec)")
    ap.add_argument("-n", "--count", type=int, default=4, help="bytes to read (default 4)")
    ap.add_argument("--float", action="store_true", help="also show float32 for the first word")
    ap.add_argument("--watch", type=float, metavar="SEC", help="poll every SEC, highlight changes")
    ap.add_argument("--scan", nargs=2, metavar=("ADDR", "LEN"),
                    help="diff a region before/after you move one knob")
    ap.add_argument("--find", nargs=2, metavar=("ADDR", "LEN"),
                    help="noise-robust param locate (filters audio) across rounds")
    ap.add_argument("--rounds", type=int, default=2, help="--find rounds (default 2)")
    ap.add_argument("--settle", type=float, default=0.4,
                    help="--find seconds between the two 'held still' snapshots")
    ap.add_argument("--map", nargs=2, metavar=("ADDR", "LEN"),
                    help="guided per-knob mapping -> writes --out json")
    ap.add_argument("--names", default=DEFAULT_NAMES,
                    help="comma-separated knob names for --map")
    ap.add_argument("--out", default=os.path.join(HERE, "mg_addrs.json"),
                    help="--map output file (default tools/mg_addrs.json)")
    ap.add_argument("--probes", action="store_true", help="list connected probes and exit")
    ap.add_argument("--freq", type=int, default=4_000_000, help="SWD clock Hz (default 4e6)")
    args = ap.parse_args()

    if args.probes:
        list_probes()
        return

    if not args.scan and not args.find and not args.map and args.addr is None:
        ap.error("give an address, or --scan/--find/--map ADDR LEN, or --probes")

    session = connect(args.freq)
    try:
        target = session.target
        if args.map:
            names = [n.strip() for n in args.names.split(",") if n.strip()]
            cmd_map(target, parse_addr(args.map[0]), parse_addr(args.map[1]),
                    names, args.out)
            return
        if args.find:
            cmd_find(target, parse_addr(args.find[0]), parse_addr(args.find[1]),
                     args.rounds, args.settle)
            return
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
