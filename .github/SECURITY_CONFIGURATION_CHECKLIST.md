# Security Configuration Checklist for skt-smt Repository

This checklist ensures all security rules, branch protections, signing keys, and configurations from hibp-checker are replicated here.

---

## ✅ Repository Security Checklist

### 1. Branch Protection Rules

**Main/Master Branch:**
- [ ] Require pull request reviews before merging
  - Minimum: 1 required approving review
  - Dismiss stale pull request approvals when new commits are pushed
- [ ] Require status checks to pass before merging
  - Require branches to be up to date before merging
  - Status checks: Python tests, Linting, Security scans
- [ ] Require conversation resolution before merging
- [ ] Require signed commits
- [ ] Require linear history
- [ ] Include administrators in restrictions
- [ ] Restrict who can push to matching branches
- [ ] Allow force pushes: **DISABLED**
- [ ] Allow deletions: **DISABLED**

**Development Branches (claude/*, dev/*):**
- [ ] Require pull request reviews (optional, but recommended)
- [ ] Require status checks to pass
- [ ] Require signed commits
- [ ] Allow force pushes: **DISABLED**

**Configuration Path:** Settings → Branches → Branch protection rules

---

### 2. Code Security and Scanning

**Dependabot:**
- [ ] Enable Dependabot alerts
- [ ] Enable Dependabot security updates
- [ ] Enable Dependabot version updates
- [ ] Configure dependabot.yml (see below)

**Code Scanning:**
- [ ] Enable CodeQL analysis
- [ ] Configure code scanning workflow
- [ ] Set up security scanning for Python
- [ ] Enable secret scanning
- [ ] Enable push protection for secrets

**Configuration Path:** Settings → Security & analysis → Code security

---

### 3. Commit Signing

**GPG/SSH Signing:**
- [ ] Require signed commits on protected branches
- [ ] Add GPG/SSH signing keys to GitHub account
- [ ] Configure git to sign commits automatically
- [ ] Verify commit signature verification is enabled

**Local Git Configuration:**
```bash
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

**Configuration Path:** Settings → Branches → Require signed commits

---

### 4. Repository Settings

**General Security:**
- [ ] Disable forking (if private repository)
- [ ] Restrict repository visibility appropriately
- [ ] Enable "Automatically delete head branches"
- [ ] Disable wiki (if not used)
- [ ] Disable projects (if not used)
- [ ] Disable discussions (unless needed)

**Access Control:**
- [ ] Review collaborator access levels
- [ ] Use teams for organization repositories
- [ ] Enable two-factor authentication requirement for collaborators
- [ ] Limit who can create branches
- [ ] Limit who can create tags

**Configuration Path:** Settings → General

---

### 5. GitHub Actions Security

**Workflow Permissions:**
- [ ] Set default workflow permissions to "Read repository contents"
- [ ] Require approval for workflows from outside collaborators
- [ ] Disable actions from unknown publishers
- [ ] Allow only verified actions

**Secrets Management:**
- [ ] Store sensitive data in GitHub Secrets
- [ ] Use environment-specific secrets
- [ ] Rotate secrets regularly
- [ ] Never commit secrets to repository

**Configuration Path:** Settings → Actions → General

---

### 6. Security Policies

**Required Files:**
- [ ] SECURITY.md - Security policy and vulnerability reporting
- [ ] CODE_OF_CONDUCT.md - Code of conduct
- [ ] CONTRIBUTING.md - Contribution guidelines
- [ ] .github/dependabot.yml - Dependabot configuration
- [ ] .github/workflows/codeql.yml - Code scanning workflow

---

### 7. Webhooks and Integrations

**Security Monitoring:**
- [ ] Review and audit all webhooks
- [ ] Enable webhook secret verification
- [ ] Review installed GitHub Apps
- [ ] Remove unused integrations
- [ ] Monitor integration logs

**Configuration Path:** Settings → Webhooks, Settings → Installed GitHub Apps

---

### 8. Advanced Security Features (GitHub Advanced Security)

If using GitHub Advanced Security:
- [ ] Enable secret scanning
- [ ] Enable push protection
- [ ] Configure custom secret scanning patterns
- [ ] Enable dependency review
- [ ] Set up security advisories

**Configuration Path:** Settings → Security & analysis

---

## 📋 Step-by-Step Configuration Guide

### Step 1: Enable Branch Protection (Main Branch)

1. Go to: `Settings → Branches`
2. Click `Add branch protection rule`
3. Branch name pattern: `main` (or `master`)
4. Enable the following:
   - ✅ Require a pull request before merging
     - Required approvals: 1
     - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ Require status checks to pass before merging
     - ✅ Require branches to be up to date before merging
     - Search and add: `Python application`, `Pylint`, `CodeQL`
   - ✅ Require conversation resolution before merging
   - ✅ Require signed commits
   - ✅ Require linear history
   - ✅ Include administrators
   - ✅ Restrict who can push to matching branches (optional)
   - ⛔ Allow force pushes: **Disabled**
   - ⛔ Allow deletions: **Disabled**
5. Click `Create` or `Save changes`

### Step 2: Enable Dependabot

1. Go to: `Settings → Security & analysis`
2. Enable:
   - `Dependabot alerts` → Click `Enable`
   - `Dependabot security updates` → Click `Enable`
3. Create `.github/dependabot.yml` (provided below)
4. Commit and push the file

### Step 3: Enable Code Scanning

1. Go to: `Security → Code scanning`
2. Click `Set up code scanning`
3. Choose `CodeQL Analysis`
4. Select `Advanced` configuration
5. Use the workflow provided below
6. Commit the workflow file

### Step 4: Configure Commit Signing

1. Generate GPG or SSH signing key (if not already done)
2. Add key to GitHub: `Settings → SSH and GPG keys`
3. Configure local git:
   ```bash
   git config --global user.signingkey YOUR_KEY_ID
   git config --global commit.gpgsign true
   git config --global tag.gpgsign true
   ```
4. Test: `git commit -S -m "test signed commit"`

### Step 5: Review Repository Settings

1. Go to: `Settings → General`
2. Features section:
   - ⛔ Disable Wikis (unless needed)
   - ⛔ Disable Issues (or keep enabled)
   - ⛔ Disable Projects (unless needed)
   - ⛔ Disable Discussions (unless needed)
3. Pull Requests section:
   - ✅ Allow squash merging
   - ✅ Allow rebase merging
   - ⛔ Disable merge commits (recommended)
   - ✅ Automatically delete head branches
4. Archives section:
   - ⛔ Do not include Git LFS objects in archives (recommended)

### Step 6: Configure GitHub Actions

1. Go to: `Settings → Actions → General`
2. Actions permissions:
   - Select: `Allow all actions and reusable workflows` or
   - Select: `Allow actions created by GitHub` and `Allow Marketplace verified creators`
3. Workflow permissions:
   - Select: `Read repository contents and packages permissions`
   - ⛔ Disable: `Read and write permissions`
4. Fork pull request workflows:
   - ✅ Require approval for all outside collaborators

---

## 🔒 Security Best Practices Applied

### Implemented Security Measures:

1. **Code Review Required**
   - All changes require review before merging
   - Prevents unauthorized or malicious code

2. **Automated Security Scanning**
   - Dependabot monitors dependencies
   - CodeQL scans for vulnerabilities
   - Secret scanning prevents credential leaks

3. **Signed Commits**
   - Verify authenticity of commits
   - Prevent commit spoofing
   - Maintain chain of trust

4. **Branch Protection**
   - Prevent direct pushes to main
   - Require tests to pass
   - Prevent force pushes and deletions

5. **Least Privilege Access**
   - Limit workflow permissions
   - Restrict branch access
   - Require authentication

---

## 📝 Configuration Files to Add

The following files should be added to the repository (provided separately):

1. `.github/dependabot.yml` - Dependency update configuration
2. `.github/workflows/codeql.yml` - Code security scanning
3. `.github/workflows/security-scan.yml` - Additional security checks
4. `SECURITY.md` - Security policy
5. `CODE_OF_CONDUCT.md` - Code of conduct
6. `CONTRIBUTING.md` - Contribution guidelines

---

## 🔐 Secrets Management

### Repository Secrets to Configure:

If applicable, add these secrets in `Settings → Secrets and variables → Actions`:

- `PYPI_API_TOKEN` - For package publishing (if needed)
- `CODECOV_TOKEN` - For code coverage (if used)
- Any other API keys or credentials

**Important:** Never commit secrets to the repository!

---

## ✅ Verification Checklist

After configuration, verify:

- [ ] Try pushing directly to main → Should be blocked
- [ ] Try pushing unsigned commit → Should be blocked
- [ ] Create PR without reviews → Should not be mergeable
- [ ] Create PR with failing tests → Should not be mergeable
- [ ] Dependabot creates PRs for outdated dependencies
- [ ] Code scanning runs on push
- [ ] Secret scanning detects test secrets

---

## 📞 Support

For questions about security configuration:
- GitHub Docs: https://docs.github.com/en/code-security
- Repository Security: https://docs.github.com/en/code-security/getting-started

---

**Last Updated:** 2025-11-08
**Version:** 1.0
**Repository:** greogory/skt-smt
