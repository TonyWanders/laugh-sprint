#!/usr/bin/env python3
"""Write one original funny line about everyday life to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The line is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, prints exactly the
line itself to stdout with no trailing newline and no extra output,
and reads the file back to confirm it holds exactly the line. It
enforces the competition gate: 1 to 200 characters, not only white
space.
"""

import os
import sys
from pathlib import Path

LINE = "My phone says I walked 10,000 steps today, mostly pacing while waiting for a text that just said 'k'."

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 200 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"line is {chars} characters, outside 1-200")
    if not text.strip():
        raise ValueError("line is only white space")
    return chars


def main() -> int:
    try:
        validate(LINE)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(LINE, encoding="utf-8")
    if path.read_text(encoding="utf-8") != LINE:
        print("written file does not match the line", file=sys.stderr)
        return 1
    sys.stdout.write(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
