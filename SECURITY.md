# Security Policy

## Supported Versions

The following versions of Input Testing Utility Suite are currently supported with security updates:

| Version | Supported          | Security Updates |
| ------- | ------------------ | ---------------- |
| 2.0.x   | :white_check_mark: | Yes              |
| 1.8.x   | :white_check_mark: | Critical only    |
| 1.7.x   | :white_check_mark: | Critical only    |
| < 1.7   | :x:                | No               |

**Recommendation:** Always use the latest version (2.0.x) for the best security and safety features.

---

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please report it responsibly.

### How to Report

**DO NOT** open a public issue for security vulnerabilities.

Instead, please report security vulnerabilities through one of these methods:

1. **GitHub Security Advisories** (Preferred)
   - Navigate to the [Security tab](https://github.com/greogory/skt-smt/security)
   - Click "Report a vulnerability"
   - Fill out the form with details

2. **Private Communication**
   - Email: [Create a private security advisory on GitHub]
   - Include "SECURITY" in the subject line
   - Provide detailed information (see below)

### What to Include

Please include the following information in your report:

- **Description:** Clear description of the vulnerability
- **Impact:** Potential impact and severity
- **Reproduction:** Step-by-step instructions to reproduce
- **Affected Versions:** Which versions are affected
- **Proposed Fix:** If you have a suggested fix (optional)
- **Your Contact:** How we can reach you for follow-up

### Example Report

```
Subject: SECURITY - [Brief Description]

Description:
[Detailed description of the vulnerability]

Impact:
[What an attacker could do, who is affected]

Steps to Reproduce:
1. [Step 1]
2. [Step 2]
3. [Result]

Affected Versions:
v2.0.0, v1.8.0, etc.

Proposed Fix (if any):
[Your suggested solution]
```

---

## Response Timeline

- **Acknowledgment:** Within 48 hours
- **Initial Assessment:** Within 7 days
- **Status Updates:** Every 7 days until resolved
- **Fix Release:** Depends on severity (see below)

### Severity Levels and Response Times

| Severity | Response Time | Fix Release Target |
|----------|--------------|-------------------|
| Critical | Immediate    | 1-7 days          |
| High     | 24 hours     | 7-14 days         |
| Medium   | 7 days       | 14-30 days        |
| Low      | 14 days      | Next release      |

---

## Security Update Process

1. **Verification:** We verify the vulnerability
2. **Assessment:** We assess the impact and severity
3. **Fix Development:** We develop and test a fix
4. **Advisory Creation:** We create a security advisory
5. **Coordinated Disclosure:** We coordinate release timing with you
6. **Public Release:** We release the fix and advisory
7. **Credit:** We credit you (unless you prefer anonymity)

---

## Security Features in v2.0

Version 2.0 includes comprehensive security hardening:

### Window Bounds Safety
- **Multi-layer validation** prevents out-of-bounds operations
- **Thread-safe operations** eliminate race conditions
- **Coordinate validation** at 5 layers
- **Window handle verification** before all operations

### Code Security
- **Input validation** on all user inputs
- **Defensive programming** patterns throughout
- **Error handling** prevents information disclosure
- **No known vulnerabilities** in current release

### Dependency Security
- **Minimal dependencies** (only 3 required)
- **Vetted packages** (pywin32, psutil, setuptools)
- **Regular updates** via Dependabot
- **Vulnerability scanning** enabled

---

## Security Best Practices for Users

### Installation Security

1. **Verify Source:**
   - Download only from official GitHub releases
   - Verify release signatures (when available)
   - Check file hashes against published checksums

2. **Use Virtual Environments:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Keep Updated:**
   - Subscribe to security advisories
   - Update to latest version promptly
   - Review CHANGELOG.md for security fixes

### Usage Security

1. **Legitimate Testing Only:**
   - Only test on systems you own or have permission to test
   - Do not use to circumvent security measures
   - Respect privacy and data protection laws

2. **Secure Configuration:**
   - Review configuration files before use
   - Don't store sensitive data in config files
   - Use appropriate file permissions

3. **Log Security:**
   - Protect log files (may contain sensitive data)
   - Review logs regularly
   - Delete logs when no longer needed

### Development Security

1. **Code Review:**
   - Review all changes before merging
   - Use signed commits
   - Follow secure coding practices

2. **Dependency Management:**
   - Keep dependencies updated
   - Review dependency changes
   - Use Dependabot alerts

---

## Known Security Considerations

### By Design Limitations

1. **Windows API Usage:**
   - Requires pywin32 (trusted package)
   - Uses Windows message API
   - Limited to Windows platform

2. **Window Operations:**
   - Creates hidden/transparent windows
   - Sends simulated input events
   - Requires appropriate permissions

3. **Logging:**
   - Logs may contain test data
   - Store logs securely
   - Clean up logs regularly

### Not Vulnerabilities

The following are **not** security vulnerabilities:

- Intended functionality (simulating input)
- Logging of test data
- Requirement for Windows platform
- Use of Windows API functions
- Creation of hidden windows (intended behavior)

---

## Security Disclosure History

### v2.0.0 (2025-11-08)
- **Enhancement:** Complete safety refactoring
- **Fixed:** Window bounds validation (proactive)
- **Fixed:** Race conditions in window operations (proactive)
- **Fixed:** Thread safety issues (proactive)
- **Fixed:** Coordinate validation gaps (proactive)
- **Status:** No known vulnerabilities

### v1.8.0
- **Status:** No security vulnerabilities reported

### v1.7.0
- **Status:** No security vulnerabilities reported

---

## Responsible Disclosure

We believe in responsible disclosure and will:

- Work with you to understand and verify the vulnerability
- Keep you informed throughout the process
- Credit you in the security advisory (unless you prefer anonymity)
- Coordinate disclosure timing with you
- Not take legal action against good-faith security researchers

---

## Bug Bounty Program

Currently, we do not have a formal bug bounty program. However, we:

- Appreciate responsible disclosure
- Credit researchers in advisories
- Consider this for future implementation

---

## Security Contact

For security-related questions (non-vulnerabilities):
- Open a discussion in GitHub Discussions
- Tag with "security" label

For vulnerability reports:
- Use GitHub Security Advisories
- See "Reporting a Vulnerability" section above

---

## Compliance and Standards

### Security Standards Followed:

- **OWASP Top 10** awareness in development
- **CWE** (Common Weakness Enumeration) mitigation
- **NIST** Secure Software Development Framework principles
- **Secure Coding Practices** (input validation, error handling, etc.)

### Code Security:

- Static analysis with pylint
- Security scanning with CodeQL (when available)
- Dependency scanning with Dependabot
- Regular security reviews

---

## Acknowledgments

We thank the security research community for their efforts in keeping software secure. Special thanks to:

- [Security researchers who report vulnerabilities responsibly]
- The Python security team
- The pywin32 maintainers
- GitHub Security Lab

---

## Updates to This Policy

This security policy may be updated periodically. Changes will be:
- Documented in git history
- Announced in release notes
- Posted in security advisories (if significant)

**Last Updated:** 2025-11-08
**Version:** 1.0.0

---

## Additional Resources

- [SECURITY_CONFIGURATION_CHECKLIST.md](.github/SECURITY_CONFIGURATION_CHECKLIST.md) - Repository security setup
- [SAFETY_REFACTORING_GUIDE.md](SAFETY_REFACTORING_GUIDE.md) - v2.0 safety improvements
- [CHANGELOG.md](CHANGELOG.md) - Security fixes and updates
- [GitHub Security Docs](https://docs.github.com/en/code-security)

---

**Remember:** Security is a shared responsibility. Thank you for helping keep Input Testing Utility Suite secure!
