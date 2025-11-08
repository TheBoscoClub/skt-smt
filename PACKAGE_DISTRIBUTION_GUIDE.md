# Package Distribution Guide

## Input Testing Utility Suite v2.0.0

This guide explains the different package distribution formats available for the Input Testing Utility Suite.

---

## 📦 Available Package Formats

### 1. Bundled Package (RECOMMENDED for offline installation)
**File:** `input-testing-utility-suite-v2.0.0-bundled.zip` (11 MB)

**What's Included:**
- ✅ All v2.0 Python scripts (skt-2.0.py, smt-2.0.py, base_input_tester_2.0.py)
- ✅ All Python dependencies as wheel files (pywin32, psutil, setuptools)
- ✅ Automated installation script (install_bundled.bat)
- ✅ Complete documentation and license files
- ✅ No internet connection required after download

**Best For:**
- Offline installations
- Air-gapped systems
- Corporate environments with restricted internet access
- Users who want everything in one package

**Installation:**
1. Download and extract the ZIP file
2. Double-click `install_bundled.bat`
3. OR run manually: `pip install --no-index --find-links=wheels -r requirements.txt`

**Requirements:**
- Python 3.7 or later
- Windows operating system

---

### 2. Source Distribution
**File:** `input-testing-utility-suite-2.0.0.tar.gz` (161 KB)

**What's Included:**
- ✅ All source code
- ✅ setup.py for pip installation
- ✅ Documentation and license files
- ❌ Dependencies NOT included (downloads from PyPI during installation)

**Best For:**
- Standard pip installations
- Users with reliable internet access
- PyPI distribution

**Installation:**
```bash
# Install from tar.gz
pip install input-testing-utility-suite-2.0.0.tar.gz

# Or install from PyPI (if published)
pip install input-testing-utility-suite
```

**Requirements:**
- Python 3.7 or later
- Windows operating system
- Internet connection for downloading dependencies

---

### 3. Original Release Package
**File:** `input-testing-utility-suite-v2.0.0.zip` (88 KB)

**What's Included:**
- ✅ All v2.0 and legacy Python scripts
- ✅ Complete documentation
- ✅ Installation scripts (install_windows.bat/ps1)
- ❌ Dependencies NOT included (downloads during installation)

**Best For:**
- Users who want both v2.0 and legacy versions
- Development and testing
- Users with internet access

**Installation:**
1. Download and extract the ZIP file
2. Run `install_windows.bat` or `install_windows.ps1`
3. Follow on-screen prompts

**Requirements:**
- Python 3.7 or later
- Windows operating system
- Internet connection for pip to download dependencies

---

## 🎯 Which Package Should I Choose?

### Choose **Bundled Package** if you:
- Need offline installation
- Work in restricted/corporate environments
- Want all dependencies pre-downloaded
- Have limited or no internet access
- Want the simplest, most reliable installation

### Choose **Source Distribution** if you:
- Have reliable internet access
- Want the smallest download size
- Prefer standard pip workflows
- Are familiar with Python package installation

### Choose **Original Release Package** if you:
- Need both v2.0 and legacy versions
- Want additional documentation
- Are upgrading from v1.7/v1.8
- Have internet access for pip

---

## 📋 Detailed Installation Instructions

### Bundled Package Installation

#### Method 1: Automated Installation (Recommended)
```batch
# Extract the ZIP file
# Navigate to the extracted folder
# Double-click: install_bundled.bat
```

The script will:
1. Check for Python installation
2. Install all dependencies from bundled wheels
3. Verify successful installation
4. Display usage instructions

#### Method 2: Manual Installation
```bash
# Extract the ZIP file
cd input-testing-utility-suite-v2.0.0-bundled

# Install dependencies from bundled wheels (no internet required)
pip install --no-index --find-links=wheels -r requirements.txt

# Run the tools
python skt-2.0.py    # Keyboard tester
python smt-2.0.py    # Mouse tester
```

---

### Source Distribution Installation

#### From Downloaded File
```bash
# Install with dependencies
pip install input-testing-utility-suite-2.0.0.tar.gz

# Or extract and run setup.py
tar -xzf input-testing-utility-suite-2.0.0.tar.gz
cd input-testing-utility-suite-2.0.0
python setup.py install
```

#### From PyPI (if published)
```bash
# Latest version
pip install input-testing-utility-suite

# Specific version
pip install input-testing-utility-suite==2.0.0

# With optional development dependencies
pip install input-testing-utility-suite[dev]
```

---

### Original Release Package Installation

#### Windows Batch Script
```batch
# Extract the ZIP file
# Navigate to the extracted folder
# Double-click: install_windows.bat
```

#### PowerShell Script
```powershell
# Extract the ZIP file
# Right-click install_windows.ps1
# Select "Run with PowerShell"
```

#### Manual Installation
```bash
# Extract the ZIP file
cd input-testing-utility-suite-v2.0.0

# Install dependencies (requires internet)
pip install -r requirements.txt

# Run the tools
python skt-2.0.py    # Keyboard tester v2.0
python smt-2.0.py    # Mouse tester v2.0
python skt-1.8.py    # Keyboard tester v1.8 (legacy)
```

---

## 🔧 Dependencies Included in Bundled Package

### Core Dependencies
| Package | Version | Size | Description |
|---------|---------|------|-------------|
| pywin32 | 311 (Python 3.11) | 9.1 MB | Windows API access (core requirement) |
| psutil | 7.1.3 | 242 KB | System and process utilities |
| setuptools | 80.9.0 | 1.2 MB | Python package utilities |

**Total Dependencies Size:** ~10.5 MB

All wheels are for **Windows x64** and **Python 3.7+** (compatible with Python 3.7-3.11).

---

## 🚀 Building Custom Packages

If you need to create your own bundled package or customize the build:

```bash
# Build all package formats
python build_standalone.py

# This creates:
# 1. dist/input-testing-utility-suite-v2.0.0-bundled.zip
# 2. dist/input-testing-utility-suite-2.0.0.tar.gz
# 3. build_standalone/executables/ (Linux binaries)
```

**Build Requirements:**
- Python 3.7+
- pip
- wheel
- setuptools
- PyInstaller (optional, for executables)

**Note:** The build script runs on any platform but downloads Windows-specific wheels for the bundled package.

---

## 📊 Package Comparison

| Feature | Bundled | Source | Original |
|---------|---------|--------|----------|
| **Size** | 11 MB | 161 KB | 88 KB |
| **Offline Install** | ✅ Yes | ❌ No | ❌ No |
| **Dependencies Included** | ✅ Yes | ❌ No | ❌ No |
| **Internet Required** | ❌ No | ✅ Yes | ✅ Yes |
| **Legacy Versions** | ❌ No | ❌ No | ✅ Yes |
| **Auto Install Script** | ✅ Yes | ❌ No | ✅ Yes |
| **PyPI Compatible** | ❌ No | ✅ Yes | ❌ No |
| **Smallest Download** | ❌ No | ✅ Yes | ⚠️ Medium |
| **Best for Offline** | ✅ Yes | ❌ No | ❌ No |

---

## 🔒 Security Considerations

### All Packages
- All dependencies are downloaded from official PyPI sources
- Packages include GPLv3 license
- Source code is fully auditable
- No telemetry or data collection

### Bundled Package
- Dependencies are pre-downloaded and verified
- Wheel files are official releases from PyPI
- SHA256 checksums available on PyPI for verification
- No code modification from official releases

### Verification
```bash
# Verify wheel integrity (requires internet)
pip download --only-binary :all: pywin32==311
pip download --only-binary :all: psutil==7.1.3

# Compare with bundled wheels
sha256sum wheels/*.whl
```

---

## 🆘 Troubleshooting

### Bundled Package Issues

**Problem:** "Python not found" error
```
Solution: Install Python 3.7+ from python.org
          Add Python to PATH during installation
```

**Problem:** pip install fails
```
Solution: Ensure you're in the extracted folder
          Run: pip install --no-index --find-links=wheels -r requirements.txt
```

**Problem:** Import errors when running scripts
```
Solution: Verify dependencies installed successfully
          Run: pip list | findstr "pywin32 psutil"
```

### Source Distribution Issues

**Problem:** No internet connection
```
Solution: Use the bundled package instead
```

**Problem:** pywin32 installation fails
```
Solution: 1. Ensure you're on Windows
          2. Try: pip install --upgrade pip setuptools
          3. Try: pip install pywin32==311
```

### General Issues

**Problem:** "Access denied" errors
```
Solution: Run command prompt as Administrator
          OR install in user directory: pip install --user
```

**Problem:** Python version mismatch
```
Solution: Check version: python --version
          Ensure Python 3.7 or later
```

---

## 📝 Additional Resources

- **Full Documentation:** [README.md](README.md)
- **Release Notes:** [RELEASE_NOTES_v2.0.md](RELEASE_NOTES_v2.0.md)
- **Safety Guide:** [SAFETY_REFACTORING_GUIDE.md](SAFETY_REFACTORING_GUIDE.md)
- **Security Policy:** [SECURITY.md](SECURITY.md)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **GitHub Repository:** https://github.com/greogory/skt-smt
- **Issue Tracker:** https://github.com/greogory/skt-smt/issues

---

## 📄 License

All packages are distributed under the **GNU General Public License v3.0 (GPL-3.0)**.

See [LICENSE.txt](LICENSE.txt) for full license text.

---

## 🎉 Quick Start Summary

**For most users (offline/corporate):**
1. Download `input-testing-utility-suite-v2.0.0-bundled.zip`
2. Extract and run `install_bundled.bat`
3. Run `python skt-2.0.py` or `python smt-2.0.py`

**For pip users (with internet):**
```bash
pip install input-testing-utility-suite-2.0.0.tar.gz
```

**For developers:**
```bash
git clone https://github.com/greogory/skt-smt.git
cd skt-smt
pip install -r requirements.txt
python skt-2.0.py
```

---

*Last updated: 2025-11-08*
*Version: 2.0.0*
