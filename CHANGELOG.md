# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - 2026-09-25

### Added

- Recursive directory scan with size pre-filtering
- SHA-256 content hashing of candidate groups
- CLI with `--min-size` and `--version` flags
- Unit test suite and GitHub Actions CI

## [0.2.0] - 2026-10-12

### Added

- Parallel hashing across candidate groups
- Repeatable `--exclude GLOB` flag for skipping files/directories

### Fixed

- Stable directory traversal order for reproducible output

## [0.3.0] - 2026-11-03

### Added

- `--quiet` flag to suppress progress output
- `--json` flag for machine-readable results
- Hard-link deduplication via inode tracking

### Changed

- Progress line now prints the scanned root before walking
