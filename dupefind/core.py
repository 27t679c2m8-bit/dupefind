"""Core scanning and hashing logic for dupefind."""

from __future__ import annotations

import hashlib
import os
from collections import defaultdict
from pathlib import Path

CHUNK_SIZE = 1024 * 1024


def _file_hash(path: Path, chunk_size: int = CHUNK_SIZE) -> str:
    """Return the SHA-256 hex digest of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            block = fh.read(chunk_size)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def find_duplicates(root: Path, min_size: int = 0) -> dict[str, list[Path]]:
    """Walk `root` and group files by (size, sha256) content identity.

    Files are first grouped by byte size; only groups with two or more
    members are hashed, which keeps large scans fast.
    """
    by_size: dict[int, list[Path]] = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            path = Path(dirpath) / name
            try:
                if not path.is_file():
                    continue
                size = path.stat().st_size
            except OSError:
                continue
            if size >= min_size:
                by_size[size].append(path)

    duplicates: dict[str, list[Path]] = {}
    for paths in by_size.values():
        if len(paths) < 2:
            continue
        by_hash: dict[str, list[Path]] = defaultdict(list)
        for path in paths:
            try:
                by_hash[_file_hash(path)].append(path)
            except OSError:
                continue
        for digest, group in by_hash.items():
            if len(group) > 1:
                duplicates[digest] = sorted(group)
    return duplicates
