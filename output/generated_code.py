
#!/usr/bin/env python3
"""
Multiplication table generator.

By default the program prints the multiplication table of 2 (from 1×2 up to 10×2).
The range and the multiplier can be customised via command‑line arguments.

Usage examples
--------------
$ python table_of_two.py               # prints 2×1 … 2×10
$ python table_of_two.py --limit 5     # prints 2×1 … 2×5
$ python table_of_two.py --start 3 --limit 7
$ python table_of_two.py --multiplier 7 --limit 12
"""

import argparse
import sys
from typing import Iterable, List, Optional

__all__ = ["generate_table", "parse_args", "main"]


def _positive_int(value: str) -> int:
    """Argparse type that ensures the value is a positive integer (>= 1)."""
    try:
        iv = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid integer value: {value!r}") from exc
    if iv < 1:
        raise argparse.ArgumentTypeError("must be a positive integer (>= 1)")
    return iv


def generate_table(
    multiplier: int,
    start: int = 1,
    limit: int = 10,
) -> Iterable[str]:
    """
    Generate a multiplication table.

    Args:
        multiplier: The number whose table is generated (e.g., 2).
        start: The first multiplicand (must be >= 1).
        limit: The last multiplicand (must be >= start).

    Yields:
        Formatted strings, each representing one line of the table.

    Raises:
        ValueError: If ``start`` or ``limit`` are not positive integers,
                    or if ``limit`` is smaller than ``start``.
    """
    if start < 1:
        raise ValueError("`start` must be a positive integer.")
    if limit < 1:
        raise ValueError("`limit` must be a positive integer.")
    if limit < start:
        raise ValueError("`limit` must be greater than or equal to `start`.")

    for i in range(start, limit + 1):
        yield f"{multiplier} x {i} = {multiplier * i}"


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command‑line arguments."""
    parser = argparse.ArgumentParser(
        description="Print the multiplication table of a given number (default 2)."
    )
    parser.add_argument(
        "--multiplier",
        type=_positive_int,
        default=2,
        help="Number whose multiplication table is printed (default: 2).",
    )
    parser.add_argument(
        "--start",
        type=_positive_int,
        default=1,
        help="First multiplicand (default: 1). Must be >= 1.",
    )
    parser.add_argument(
        "--limit",
        type=_positive_int,
        default=10,
        help="Last multiplicand (default: 10). Must be >= start.",
    )
    args = parser.parse_args(argv)

    # Ensure logical relationship between start and limit
    if args.limit < args.start:
        parser.error("`--limit` must be greater than or equal to `--start`.")
    return args


def main() -> None:
    """Entry point of the script."""
    args = parse_args()
    try:
        table = generate_table(
            multiplier=args.multiplier, start=args.start, limit=args.limit
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)

    for line in table:
        print(line)


if __name__ == "__main__":
    main()
