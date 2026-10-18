"""Command-line interface for dupefind."""

from __future__ import annotations

import argparse
import fnmatch
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
        "--exclude", action="append", default=[],
        metavar="GLOB",
        help="ignore files/directories matching GLOB (repeatable)",
    )
    parser.add_argument(
        "--quiet", action="store_true",
        help="suppress progress output on stderr",
    )
    parser.add_argument(
        "--version", action="version", version=f"dupefind {__version__}",
    )
    return parser


def _excluded(path: Path, patterns: list[str]) -> bool:
    name = path.name
    rel = str(path)
    for pattern in patterns:
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel, pattern):
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.quiet:
        print(f"scanning {args.path} …", file=sys.stderr)
    duplicates = find_duplicates(
        args.path, min_size=args.min_size,
        exclude=lambda p: _excluded(p, args.exclude),
    )
    if not duplicates:
        print("no duplicates found", file=sys.stderr)
        return 0
    for index, (digest, group) in enumerate(sorted(duplicates.items()), 1):
        print(f"#{index} ({digest[:12]}…, {len(group)} files)")
        for path in group:
            print(f"  {path}")
    return 0
