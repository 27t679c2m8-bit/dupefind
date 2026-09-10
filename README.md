# dupefind

Fast, dependency-free duplicate file finder.

`dupefind` walks a directory tree, groups files by size and hashes candidate
groups with a full SHA-256 pass, so large trees scan quickly without hashing
every byte twice.

## Install

```bash
pip install dupefind
```

## Usage

```bash
dupefind            # scan current directory
dupefind ~/Downloads
```

## License

MIT
