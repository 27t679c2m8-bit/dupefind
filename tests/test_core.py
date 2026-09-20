"""Unit tests for dupefind.core."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from dupefind.core import find_duplicates


class FindDuplicatesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, relpath: str, data: bytes) -> Path:
        path = self.root / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def test_empty_tree(self) -> None:
        self.assertEqual(find_duplicates(self.root), {})

    def test_identical_files(self) -> None:
        a = self.write("a.txt", b"same content")
        b = self.write("sub/b.txt", b"same content")
        result = find_duplicates(self.root)
        self.assertEqual(len(result), 1)
        group = next(iter(result.values()))
        self.assertEqual(set(group), {a, b})

    def test_different_files_not_reported(self) -> None:
        self.write("a.txt", b"content one")
        self.write("b.txt", b"content two")
        self.assertEqual(find_duplicates(self.root), {})

    def test_min_size_filters_small_files(self) -> None:
        self.write("a.txt", b"tiny")
        self.write("b.txt", b"tiny")
        self.assertEqual(find_duplicates(self.root, min_size=10), {})

    def test_same_size_different_hash(self) -> None:
        self.write("a.txt", b"AAAA")
        self.write("b.txt", b"BBBB")
        self.assertEqual(find_duplicates(self.root), {})


if __name__ == "__main__":
    unittest.main()
