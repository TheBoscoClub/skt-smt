# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do NOT open a public GitHub issue** for security vulnerabilities
2. Use GitHub's private vulnerability reporting feature
3. Or email the maintainer directly

## GitHub Security Features

| Feature | Status |
|---------|--------|
| **Dependabot vulnerability alerts** | ✅ Enabled |
| **Dependabot security updates** | ✅ Enabled |
| **CodeQL analysis** | ✅ Enabled |
| **Secret scanning** | ✅ Enabled |

## Security Audit Tools

This project contains Python applications for SKT/SMT controller testing.

### Python Code

| Tool | Purpose | Command |
|------|---------|---------|
| **bandit** | Security-focused static analysis | `bandit -r . -x ./.snapshots` |
| **pip-audit** | Dependency vulnerability scanner | `pip-audit` |
| **ruff** | Fast Python linter | `ruff check .` |
| **mypy** | Static type checking | `mypy --ignore-missing-imports .` |

### Documentation

| Tool | Purpose | Command |
|------|---------|---------|
| **markdownlint** | Markdown linting | `markdownlint '**/*.md'` |
| **codespell** | Spell checking | `codespell --skip='.git,.snapshots'` |

### Running a Full Security Audit

```bash
# Python security
bandit -r . -x ./.snapshots -f txt
pip-audit

# Linting
ruff check .

# Check for secrets
grep -rE "(api[_-]?key|password|secret|token).*=" --include="*.py" . | grep -v "example\|test"

# Documentation
markdownlint '**/*.md'
codespell --skip='.git,.snapshots'
```

## CodeQL Alert Status

All CodeQL alerts have been reviewed and resolved:
- **Pythagorean warnings**: Dismissed as false positives - intentional trigonometric calculations for angle/position math
- **Overwritten-inherited-attribute**: Dismissed as false positives - intentional Qt widget attribute overrides for custom styling

---

**Last Updated**: 2026-01-20
