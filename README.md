# dupefind

Fast, dependency-free duplicate file finder.

[![CI](https://github.com/27t679c2m8-bit/dupefind/actions/workflows/ci.yml/badge.svg)](https://github.com/27t679c2m8-bit/dupefind/actions)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

`dupefind` walks a directory tree, groups files by byte size and hashes only
candidate groups with a full SHA-256 pass. Size pre-filtering plus parallel
hashing keeps scans fast even on large trees. Hard-linked files are counted
once.

## Install

```bash
pip install dupefind
```

## Usage

```bash
dupefind                       # scan current directory
dupefind ~/Downloads           # scan a directory
dupefind . --min-size 1048576  # only files >= 1 MB
dupefind . --exclude ".git"    # ignore patterns (repeatable)
dupefind . --quiet             # progress-free output
```

## How it works

1. Walk the tree, collecting file paths grouped by byte size.
2. Discard groups with a single member.
3. Hash remaining files in parallel and group by SHA-256 digest.
4. Report every group with two or more identical files.

## Development

```bash
git clone https://github.com/27t679c2m8-bit/dupefind
cd dupefind
pip install -e .
python -m unittest discover -s tests
```

## License

MIT — see [LICENSE](LICENSE).

## FAQ

**How is dupefind different from fdupes or rmlint?**

dupefind is pure-stdlib Python (no C extensions), ships as a single installable
package, and exposes a machine-readable `--json` mode for scripting — making it
easy to embed in backup and cleanup pipelines on hosts where dedicated C tools
are unavailable.
