"""Unit tests for dupefind.cli."""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from dupefind.cli import main


class CliTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_cli(self, *args: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(list(args) + [str(self.root), "--quiet"])
        return code, out.getvalue(), err.getvalue()

    def test_no_duplicates_exit_code(self) -> None:
        (self.root / "a.txt").write_bytes(b"only")
        code, out, _ = self.run_cli()
        self.assertEqual(code, 0)
        self.assertIn("no duplicates", out + _)

    def test_json_output_shape(self) -> None:
        (self.root / "a.txt").write_bytes(b"dup")
        (self.root / "b.txt").write_bytes(b"dup")
        code, out, _ = self.run_cli("--json")
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(len(payload), 1)
        self.assertIn("sha256", payload[0])
        self.assertEqual(len(payload[0]["files"]), 2)

    def test_exit_code_ok_with_duplicates(self) -> None:
        (self.root / "a.txt").write_bytes(b"dup")
        (self.root / "b.txt").write_bytes(b"dup")
        code, _, _ = self.run_cli()
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
