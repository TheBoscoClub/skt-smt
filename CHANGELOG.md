# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Fixed

## [1.7.1] - 2026-01-13

### Added
- `CHANGELOG.md` for version tracking
- CodeQL semantic code analysis workflow
- Python security and quality workflow (bandit, ruff, pip-audit)
- Daily automated security scans

### Fixed
- Critical fixes from /test audit
- Remove unused variables (codeql.yml comment fix)

### Changed
- Pinned Python 3.14.2 via pyenv for reproducible builds
- Updated .gitignore with local tool config patterns

## [1.7.0] - 2026-01-09

### Added
- `BaseInputTester` (base_input_tester_1.7.py) foundation class
- `SafeKeyboardTester` (skt-1.7.py) with realistic typing patterns
- `SafeMouseTester` (smt-1.7.py) with human-like mouse physics
- Window management and message processing infrastructure
- Resource monitoring and logging capabilities
- JSON configuration file support
- Comprehensive legal disclaimer and ethical use statement

### Features
- Isolated input simulation without affecting other applications
- Human-like typing with variable speeds and occasional typos
- Mouse movement patterns: random, linear, circular, targeted
- Realistic mouse physics with acceleration/deceleration
- Detailed activity logging for analysis
