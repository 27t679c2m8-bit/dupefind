# dupefind

Fast, dependency-free duplicate file finder.

`dupefind` walks a directory tree, groups files by size and hashes candidate
groups with a full SHA-256 pass, so large trees scan quickly without hashing
every byte twice.

## Install

```bash
pip install dupefind
```

## Quickstart

```bash
dupefind                       # scan current directory
dupefind ~/Downloads           # scan a directory
dupefind . --min-size 1048576  # only files >= 1 MB
```

## Development

```bash
git clone https://github.com/27t679c2m8-bit/dupefind
cd dupefind
pip install -e .
python -m unittest discover -s tests
```

## License

MIT
