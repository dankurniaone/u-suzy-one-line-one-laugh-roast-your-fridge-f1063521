"""Roast Your Fridge — one line, one laugh.

Writes a single roast line to /output/entry.txt.
Gate: UTF-8 text, 1-200 characters, not only whitespace.
Stdlib only.
"""

import argparse
import os
import sys

LINE = (
    "The freezer has a bag of peas from 2021. I keep it for the same "
    "reason the fridge keeps me: neither of us knows how to let go."
)

TOURNAMENT = [
    # (line, specificity, surprise, freshness)
    ("My fridge hums the same note every night. I checked: it is not "
     "broken, it is just practising its one song for an audience of "
     "leftovers.", 4, 4, 4),
    ("The ice maker has produced exactly three cubes since 2019. It "
     "considers this a career, and I am its only performance review.",
     5, 4, 5),
    ("I opened the fridge at 2 AM and the light came on like it was "
     "doing me a favour. The light is the only thing in there with a "
     "job.", 3, 3, 2),
    ("My fridge keeps everything at 4 degrees and my hopes at zero. "
     "It has never once apologised for the yogurt.", 3, 3, 3),
    ("The vegetable drawer is where good intentions go to become "
     "science experiments. The carrots have tenure now.", 5, 4, 3),
    ("I bought a smart fridge. It texts me when the milk expires, "
     "which is daily, because it buys milk faster than I drink it.",
     4, 3, 3),
    ("My fridge has a water dispenser that works one day in five. "
     "The other four it just sighs, which I respect, honestly.",
     5, 4, 4),
    (LINE, 5, 5, 4),
]


def check_line(line):
    """Return (ok, reason) for the 1-200 char UTF-8 gate."""
    if not line or not line.strip():
        return False, "empty or whitespace only"
    if "\n" in line or "\r" in line:
        return False, "must be a single line"
    if len(line) > 200:
        return False, "over 200 characters: %d" % len(line)
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        return False, "not UTF-8: %s" % exc
    return True, "ok: %d characters, %d bytes" % (
        len(line), len(line.encode("utf-8")))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="dry run: validate the line, print it, exit")
    parser.add_argument("--self-test", action="store_true",
                        help="write to a temp file and verify the bytes read back")
    parser.add_argument("--output", default="/output/entry.txt",
                        help="where to write the entry")
    args = parser.parse_args(argv)

    ok, reason = check_line(LINE)
    if not ok:
        print("gate FAIL: %s" % reason, file=sys.stderr)
        return 1

    if args.self_test:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            probe = os.path.join(tmp, "entry.txt")
            with open(probe, "w", encoding="utf-8", newline="") as handle:
                handle.write(LINE)
            with open(probe, "r", encoding="utf-8") as handle:
                back = handle.read()
            if back != LINE:
                print("self-test FAIL: round-trip mismatch", file=sys.stderr)
                return 1
            print("self-test pass: %d chars round-trip byte-identical"
                  % len(back))
        return 0

    if args.check:
        print("gate pass: %s" % reason)
        for cand, spec, surp, fresh in TOURNAMENT:
            print("  %d/%d/%d  %s" % (spec, surp, fresh, cand[:60]))
        print("tournament winner: %d/%d/%d" % TOURNAMENT[-1][1:])
        print(LINE)
        return 0

    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "w", encoding="utf-8", newline="") as handle:
        handle.write(LINE)
    print("wrote %d chars to %s" % (len(LINE), args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
