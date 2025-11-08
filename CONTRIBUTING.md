# Contributing to Input Testing Utility Suite

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Security Guidelines](#security-guidelines)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Commit Message Guidelines](#commit-message-guidelines)

---

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Windows OS (for testing)
- Basic understanding of Windows API (for advanced contributions)

### Quick Start

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/skt-smt.git
   cd skt-smt
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

---

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- 🐛 **Bug Fixes** - Fix issues in existing code
- ✨ **New Features** - Add new functionality
- 📚 **Documentation** - Improve or add documentation
- 🧪 **Tests** - Add or improve test coverage
- 🔒 **Security** - Security improvements and fixes
- ♻️ **Refactoring** - Code quality improvements
- 🎨 **UI/UX** - Configuration or logging improvements

### Finding Issues

- Check the [Issues](https://github.com/greogory/skt-smt/issues) page
- Look for issues labeled `good first issue` or `help wanted`
- Read through the [SECURITY.md](SECURITY.md) for security-related work

---

## Development Setup

### Installation for Development

```bash
# Clone the repository
git clone https://github.com/greogory/skt-smt.git
cd skt-smt

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 pylint mypy bandit
```

### Project Structure

```
skt-smt/
├── base_input_tester_2.0.py  # Base class
├── smt-2.0.py                 # Mouse tester
├── skt-2.0.py                 # Keyboard tester
├── requirements.txt           # Dependencies
├── setup.py                   # Package configuration
├── tests/                     # Test files (if adding tests)
├── .github/                   # GitHub workflows and configs
└── docs/                      # Documentation
```

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length:** Maximum 127 characters
- **Indentation:** 4 spaces (no tabs)
- **Docstrings:** Google style
- **Type hints:** Encouraged for new code

### Code Formatting

Use `black` for automatic formatting:

```bash
black *.py
```

### Linting

Run linters before committing:

```bash
# Flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --max-complexity=15 --max-line-length=127 --statistics

# Pylint
pylint *.py

# Security check with Bandit
bandit -r . -f txt
```

### Type Checking

Use `mypy` for type checking:

```bash
mypy *.py
```

---

## Security Guidelines

### Security is Our Priority

- **Never commit secrets** (API keys, passwords, tokens)
- **Validate all inputs** before processing
- **Use defensive programming** patterns
- **Follow least privilege** principle
- **Review security implications** of all changes

### Security Checklist

Before submitting a PR, verify:

- [ ] No hardcoded credentials or secrets
- [ ] Input validation on all user inputs
- [ ] No SQL injection vulnerabilities (N/A for this project)
- [ ] No command injection vulnerabilities
- [ ] Proper error handling (no information disclosure)
- [ ] Dependencies are up-to-date
- [ ] Security best practices followed
- [ ] Documentation includes security considerations

### Reporting Security Issues

**DO NOT** report security vulnerabilities in public issues.

See [SECURITY.md](SECURITY.md) for responsible disclosure process.

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_mouse.py
```

### Writing Tests

- Place tests in `tests/` directory
- Use descriptive test names: `test_<functionality>_<scenario>()`
- Include docstrings explaining what is tested
- Test both success and failure cases
- Test edge cases and boundary conditions

### Test Coverage

- Aim for 80%+ code coverage
- All new features must have tests
- Bug fixes should include regression tests

---

## Pull Request Process

### Before Submitting

1. **Update your branch:**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Run all checks:**
   ```bash
   black *.py
   flake8 .
   pylint *.py
   pytest
   bandit -r .
   ```

3. **Update documentation:**
   - Update docstrings
   - Update README if needed
   - Add CHANGELOG entry

### PR Submission

1. **Create descriptive PR title:**
   - Use conventional commits format
   - Example: `feat: add circular mouse movement pattern`
   - Example: `fix: resolve coordinate overflow in mouse tester`
   - Example: `docs: update safety refactoring guide`

2. **Fill out PR template:**
   - Describe the changes
   - Reference related issues
   - List testing performed
   - Note breaking changes (if any)

3. **Ensure CI passes:**
   - All tests must pass
   - Linting must pass
   - Security scans must pass
   - No merge conflicts

4. **Request review:**
   - Wait for maintainer review
   - Address feedback promptly
   - Make requested changes

### PR Requirements

- [ ] Code follows style guide
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Commit messages follow guidelines
- [ ] All CI checks pass
- [ ] No merge conflicts
- [ ] Signed commits (if required)

---

## Commit Message Guidelines

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions/changes
- `chore`: Maintenance tasks
- `security`: Security improvements
- `deps`: Dependency updates

### Examples

```
feat(mouse): add bezier curve movement pattern

Implement quadratic Bezier curves for more realistic
targeted mouse movements with configurable control points.

Closes #123
```

```
fix(keyboard): validate VK codes before sending

Add validation to ensure virtual key codes are in valid
range (0-255) before sending to prevent errors.

This prevents crashes when invalid characters are used.
```

```
security(window): add thread-safe window operations

Implement RLock for all window operations to prevent
race conditions during concurrent access.

BREAKING CHANGE: window_lock attribute added to base class
```

### Commit Signing

If repository requires signed commits:

```bash
# Configure git signing
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true

# Sign a commit
git commit -S -m "your message"
```

---

## Review Process

### Timeline

- **Initial review:** Within 7 days
- **Follow-up:** Within 3 days of changes
- **Merge:** After approval and CI passes

### Review Criteria

Reviewers will check:

- Code quality and style
- Test coverage
- Documentation completeness
- Security implications
- Performance impact
- Breaking changes

### Addressing Feedback

- Respond to all comments
- Make requested changes
- Push updates to the same branch
- Mark conversations as resolved

---

## Release Process

### Version Numbers

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 2.0.1)
- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes (backward compatible)

### Changelog

Update CHANGELOG.md following [Keep a Changelog](https://keepachangelog.com/):

- **Added:** New features
- **Changed:** Changes in existing functionality
- **Deprecated:** Soon-to-be removed features
- **Removed:** Removed features
- **Fixed:** Bug fixes
- **Security:** Security improvements

---

## Documentation

### Documentation Standards

- **Clear and concise:** Easy to understand
- **Examples:** Include code examples
- **Complete:** Cover all use cases
- **Current:** Keep updated with code changes
- **Accessible:** Use simple language

### Types of Documentation

1. **Code comments:**
   - Explain complex logic
   - Document non-obvious behavior
   - Use docstrings for functions/classes

2. **README:**
   - Quick start guide
   - Installation instructions
   - Basic usage examples

3. **Guides:**
   - Detailed tutorials
   - Best practices
   - Advanced usage

4. **API documentation:**
   - Function signatures
   - Parameter descriptions
   - Return values
   - Examples

---

## Getting Help

### Resources

- [README.md](README.md) - Project overview
- [SECURITY.md](SECURITY.md) - Security policy
- [SAFETY_REFACTORING_GUIDE.md](SAFETY_REFACTORING_GUIDE.md) - Safety improvements
- [GitHub Issues](https://github.com/greogory/skt-smt/issues) - Bug reports and feature requests
- [GitHub Discussions](https://github.com/greogory/skt-smt/discussions) - Questions and discussions

### Contact

- Open an issue for bugs or features
- Start a discussion for questions
- Check existing issues before creating new ones

---

## Recognition

Contributors are recognized in:

- CHANGELOG.md
- Release notes
- GitHub contributors page
- Special acknowledgments for significant contributions

---

## License

By contributing, you agree that your contributions will be licensed under the GNU General Public License v3.0. See [LICENSE.txt](LICENSE.txt) for details.

---

Thank you for contributing to Input Testing Utility Suite! 🎉

Your efforts help make this project better for everyone.
