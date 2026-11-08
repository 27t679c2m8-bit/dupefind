"""Core scanning and hashing logic for dupefind."""

from __future__ import annotations

import hashlib
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable

try:  # optional accelerator, falls back to hashlib
    import xxhash as _xxhash  # type: ignore[import-not-found]
except ImportError:
    _xxhash = None

CHUNK_SIZE = 1024 * 1024
DEFAULT_WORKERS = min(8, (os.cpu_count() or 2))


def _file_hash(path: Path, chunk_size: int = CHUNK_SIZE) -> str:
    """Return a content digest of a file (xxh128 or SHA-256)."""
    if _xxhash is not None:
        digest = _xxhash.xxh128()
        with path.open("rb") as fh:
            while True:
                block = fh.read(chunk_size)
                if not block:
                    break
                digest.update(block)
        return digest.hexdigest()
    hasher = hashlib.sha256()
    with path.open("rb") as fh:
        while True:
            block = fh.read(chunk_size)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


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
    """Walk `root` and group files by (size, content digest) identity.

    Files sharing an inode (hard links) are counted once, so hard-linked
    backups do not show up as duplicates.
    """
    seen_inodes: set[tuple[int, int]] = set()
    by_size: dict[int, list[Path]] = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            path = Path(dirpath) / name
            if exclude is not None and exclude(path):
                continue
            try:
                stat = path.stat()
                if not path.is_file():
                    continue
                inode = (stat.st_dev, stat.st_ino)
                if inode in seen_inodes:
                    continue
                seen_inodes.add(inode)
                size = stat.st_size
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
