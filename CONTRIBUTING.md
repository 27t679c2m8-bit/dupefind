# Contributing to dupefind

Thanks for taking the time to contribute!

## Getting started

```bash
git clone https://github.com/27t679c2m8-bit/dupefind
cd dupefind
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Running tests

```bash
python -m unittest discover -s tests -v
```

## Style

- Keep the standard library-only dependency policy: `xxhash` is an optional
  accelerator and never required.
- Every new flag needs a test and a CHANGELOG entry.
- Match the existing formatting (PEP 8, 79-col docstrings).

## Issues and pull requests

Small fixes can go straight to a PR. For larger changes, open an issue first
so we can agree on the approach before you invest time.
