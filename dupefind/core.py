"""Core scanning and hashing logic for dupefind."""

from __future__ import annotations

import hashlib
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable

CHUNK_SIZE = 1024 * 1024
DEFAULT_WORKERS = min(8, (os.cpu_count() or 2))


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


def _hash_group(paths: list[Path]) -> dict[str, list[Path]]:
    """Group same-size paths by digest, skipping unreadable files."""
    by_hash: dict[str, list[Path]] = defaultdict(list)
    with ThreadPoolExecutor(max_workers=DEFAULT_WORKERS) as pool:
        for path, digest in zip(paths, pool.map(_file_hash, paths)):
            by_hash[digest].append(path)
    return by_hash


def find_duplicates(
    root: Path,
    min_size: int = 0,
    exclude: Callable[[Path], bool] | None = None,
) -> dict[str, list[Path]]:
    """Walk `root` and group files by (size, sha256) content identity."""
    by_size: dict[int, list[Path]] = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            path = Path(dirpath) / name
            if exclude is not None and exclude(path):
                continue
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
        for digest, group in _hash_group(paths).items():
            if len(group) > 1:
                duplicates[digest] = sorted(group)
    return duplicates
