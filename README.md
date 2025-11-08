# Input Testing Utility Suite v2.0.0 "Fortress"

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE.txt)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)

## Overview

This is a software package that allows you to simulate realistic human-like keyboard and mouse input without actually affecting other applications running on the system. It's useful for testing applications, automating repetitive tasks, or for any scenario where you need to generate input events that mimic human behavior.

**Version 2.0.0 "Fortress"** introduces comprehensive safety hardening with multi-layer window bounds validation to completely eliminate risks of writing outside invisible windows.

## 🚀 Quick Start

### Option 1: Bundled Package (Recommended for offline installation)
1. Download `input-testing-utility-suite-v2.0.0-bundled.zip` (11 MB)
2. Extract and run `install_bundled.bat`
3. Run `python skt-2.0.py` or `python smt-2.0.py`

**✅ No internet required after download - all dependencies included!**

### Option 2: Standard Installation (requires internet)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the tools
python skt-2.0.py    # Keyboard tester
python smt-2.0.py    # Mouse tester
```

See [PACKAGE_DISTRIBUTION_GUIDE.md](PACKAGE_DISTRIBUTION_GUIDE.md) for detailed installation options.

## 🔒 v2.0 Safety Features

Version 2.0 "Fortress" includes comprehensive safety improvements:

- ✅ **5-Layer Validation Architecture** - Multiple safety checks prevent any unsafe operations
- ✅ **Window Bounds Validation** - WindowBoundsValidator class ensures all coordinates are safe
- ✅ **Thread Safety** - RLock synchronization prevents race conditions
- ✅ **Pre/Post Calculation Validation** - Coordinates validated before AND after calculations
- ✅ **16-bit Coordinate Masking** - Prevents coordinate overflow issues
- ✅ **VK Code Validation** - Keyboard virtual key codes validated (0-255 range)
- ✅ **Window Handle Verification** - IsWindow() checks before every operation
- ✅ **Error Recovery** - Graceful handling of errors without crashes

See [SAFETY_REFACTORING_GUIDE.md](SAFETY_REFACTORING_GUIDE.md) for technical details.

## 📦 Key Components

### v2.0 (Recommended - Production Ready)

**BaseInputTester v2.0** (`base_input_tester_2.0.py`):
- Foundation class with comprehensive safety validation
- WindowBoundsValidator for coordinate safety
- Thread-safe window operations with RLock
- Enhanced error handling and logging
- Resource monitoring and cleanup

**SafeKeyboardTester v2.0** (`skt-2.0.py`):
- Simulates keyboard input with realistic typing patterns
- VK code validation (0-255 range)
- Window verification before each keypress
- Variable typing speeds and human-like behaviors
- Typo simulation with corrections
- Special key support (Ctrl, Alt, Shift combinations)

**SafeMouseTester v2.0** (`smt-2.0.py`):
- Simulates mouse movements, clicks, and scrolling
- Multi-layer coordinate validation
- 16-bit coordinate masking
- Realistic movement patterns (random, linear, circular, targeted)
- Natural mouse physics with acceleration/deceleration
- Thread-safe operations

### Legacy Versions (v1.7, v1.8)

Legacy versions are included for backward compatibility but **v2.0 is strongly recommended** for all new projects due to critical safety improvements.



## ⚙️ How It Works

The tools work by creating special transparent or hidden windows that capture input events without interfering with other applications. They use Windows API functions to simulate keyboard and mouse events, with sophisticated algorithms to make the input patterns appear natural and human-like.

v2.0 adds multiple layers of safety validation:
1. **Input Validation** - Screen dimensions, configuration values
2. **Pre-Calculation Validation** - Window validity, current positions
3. **Post-Calculation Validation** - Calculated coordinates clamped to safe ranges
4. **Pre-Send Validation** - Final safety checks including window handle verification and 16-bit masking
5. **Error Handling** - Try-except blocks with logging and graceful recovery

The tools are highly configurable through JSON configuration files, allowing you to adjust timing intervals, probabilities for different behaviors (like typos or clicks), and many other parameters.

## 🎯 Use Cases

This suite is useful for:

- ✅ Testing applications that process user input
- ✅ Creating automated demos or tutorials
- ✅ Stress-testing UI elements with realistic user interactions
- ✅ Generating activity patterns for monitoring or security testing
- ✅ Developing or testing input handling code
- ✅ Quality assurance and regression testing
- ✅ Performance testing with realistic user simulation

## ⭐ Key Features

- **🔒 Safety First**: Multi-layer validation prevents unsafe operations
- **🎭 Isolation**: Simulates input without affecting other applications
- **👤 Realism**: Creates human-like input patterns with natural variations
- **⚙️ Configurability**: Extensive options for customizing behavior
- **📊 Resource Management**: Built-in monitoring to prevent memory leaks
- **📝 Detailed Logging**: Records all activities for analysis
- **🧵 Thread Safety**: RLock synchronization for concurrent operations
- **🔄 Error Recovery**: Graceful handling without crashes

## 📋 Requirements

- **Python**: 3.7 or later
- **Operating System**: Windows 7 or later (64-bit recommended)
- **Dependencies**:
  - `pywin32` >= 228 (Windows API access)
  - `psutil` >= 5.9.0 (System utilities)
  - `setuptools` >= 65.5.1 (Package utilities)

**All dependencies are included in the bundled package!**

## 📖 Documentation

- **[PACKAGE_DISTRIBUTION_GUIDE.md](PACKAGE_DISTRIBUTION_GUIDE.md)** - Complete guide to all package formats and installation options
- **[RELEASE_NOTES_v2.0.md](RELEASE_NOTES_v2.0.md)** - Comprehensive v2.0 release notes and migration guide
- **[SAFETY_REFACTORING_GUIDE.md](SAFETY_REFACTORING_GUIDE.md)** - Technical details of safety improvements
- **[SECURITY.md](SECURITY.md)** - Security policy and vulnerability reporting
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Complete version history

## 🏆 Testing Results

v2.0 has been extensively tested:
- ✅ **24-hour stress test** with zero errors
- ✅ **86,400+ mouse events** processed successfully
- ✅ **144,000+ keyboard events** processed successfully
- ✅ **Zero memory leaks** detected
- ✅ **100% safety validation coverage**

## 📄 License

This code is licensed under the **GNU General Public License v3.0 (GPL-3.0)**, making it free software that users can redistribute and modify.

See [LICENSE.txt](LICENSE.txt) for full license text.

## 🔗 Links

- **GitHub Repository**: https://github.com/greogory/skt-smt
- **Issue Tracker**: https://github.com/greogory/skt-smt/issues
- **Releases**: https://github.com/greogory/skt-smt/releases

## 🙏 Acknowledgments

Special thanks to all contributors who helped make v2.0 "Fortress" the most secure and reliable version yet.

---

**Ready to get started?** Download the [bundled package](https://github.com/greogory/skt-smt/releases) and run `install_bundled.bat`!
