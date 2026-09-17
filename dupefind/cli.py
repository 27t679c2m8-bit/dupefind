"""Command-line interface for dupefind."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .core import find_duplicates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dupefind",
        description="Find duplicate files by content hash.",
    )
    parser.add_argument(
        "path", type=Path, nargs="?", default=Path("."),
        help="directory to scan (default: current directory)",
    )
    parser.add_argument(
        "--min-size", type=int, default=0,
        help="only consider files at least this many bytes",
    )
    parser.add_argument(
        "--version", action="version", version=f"dupefind {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    duplicates = find_duplicates(args.path, min_size=args.min_size)
    if not duplicates:
        print("no duplicates found", file=sys.stderr)
        return 0
    for index, (digest, group) in enumerate(sorted(duplicates.items()), 1):
        print(f"#{index} ({digest[:12]}…, {len(group)} files)")
        for path in group:
            print(f"  {path}")
    return 0
