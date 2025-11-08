#!/usr/bin/env python3
"""
Build script for creating Input Testing Utility Suite v2.0 distribution packages

This script creates:
1. Source distribution (sdist)
2. Wheel distribution (bdist_wheel)
3. Standalone package with dependencies bundled
"""

import os
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path
from datetime import datetime

VERSION = "2.0.0"
PROJECT_NAME = "input-testing-utility-suite"
DIST_DIR = "dist"
BUILD_DIR = "build"
RELEASE_DIR = f"release_v{VERSION}"


def print_header(message):
    """Print a formatted header message"""
    print("\n" + "=" * 70)
    print(f"  {message}")
    print("=" * 70 + "\n")


def run_command(cmd, description):
    """Run a command and print status"""
    print(f"→ {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ✗ FAILED: {result.stderr}")
        return False
    print(f"  ✓ Success")
    return True


def clean_directories():
    """Clean build directories"""
    print_header("Cleaning Build Directories")

    dirs_to_clean = [DIST_DIR, BUILD_DIR, RELEASE_DIR, "*.egg-info"]

    for dir_pattern in dirs_to_clean:
        if "*" in dir_pattern:
            # Handle glob patterns
            import glob
            for path in glob.glob(dir_pattern):
                if os.path.exists(path):
                    print(f"→ Removing {path}...")
                    shutil.rmtree(path)
        else:
            if os.path.exists(dir_pattern):
                print(f"→ Removing {dir_pattern}...")
                shutil.rmtree(dir_pattern)

    print("✓ Clean complete")


def build_distributions():
    """Build source and wheel distributions"""
    print_header("Building Python Distributions")

    # Upgrade build tools
    if not run_command(
        f"{sys.executable} -m pip install --upgrade build wheel setuptools",
        "Upgrading build tools"
    ):
        return False

    # Build distributions
    if not run_command(
        f"{sys.executable} -m build",
        "Building sdist and wheel"
    ):
        return False

    return True


def create_standalone_package():
    """Create a standalone package with dependencies"""
    print_header("Creating Standalone Package")

    # Create release directory
    os.makedirs(RELEASE_DIR, exist_ok=True)
    print(f"✓ Created {RELEASE_DIR}")

    # Copy core files
    core_files = [
        "base_input_tester_2.0.py",
        "smt-2.0.py",
        "skt-2.0.py",
        "requirements.txt",
        "README.md",
        "RELEASE_NOTES_v2.0.md",
        "SAFETY_REFACTORING_GUIDE.md",
        "LICENSE.txt",
        "smt-1.7.config.json",
        "skt-1.7.config.json",
        "install_windows.bat",
        "install_windows.ps1",
    ]

    print("→ Copying core files...")
    for file in core_files:
        if os.path.exists(file):
            shutil.copy2(file, RELEASE_DIR)
            print(f"  ✓ {file}")

    # Copy legacy files for backward compatibility
    legacy_files = [
        "base_input_tester_1.7.py",
        "base_input_tester_1_8.py",
        "skt-1.7.py",
        "skt-1.8.py",
        "smt-1.7.py",
    ]

    legacy_dir = os.path.join(RELEASE_DIR, "legacy")
    os.makedirs(legacy_dir, exist_ok=True)

    print("→ Copying legacy files...")
    for file in legacy_files:
        if os.path.exists(file):
            shutil.copy2(file, legacy_dir)
            print(f"  ✓ {file} → legacy/")

    # Create a README for the release
    create_release_readme()

    print("✓ Standalone package created")
    return True


def create_release_readme():
    """Create a README for the release package"""
    readme_content = f"""# Input Testing Utility Suite v{VERSION}

## Quick Start

### Windows Installation

**Option 1: Using Batch Script**
```
install_windows.bat
```

**Option 2: Using PowerShell**
```
powershell -ExecutionPolicy Bypass -File install_windows.ps1
```

**Option 3: Manual Installation**
```
pip install -r requirements.txt
```

### Running the Tests

**Mouse Tester:**
```
python smt-2.0.py
```

**Keyboard Tester:**
```
python skt-2.0.py
```

**Press ESC to stop testing**

## What's Included

### Core Files (v2.0)
- `base_input_tester_2.0.py` - Enhanced base class
- `smt-2.0.py` - Safe Mouse Tester
- `skt-2.0.py` - Safe Keyboard Tester

### Configuration
- `smt-1.7.config.json` - Mouse tester configuration
- `skt-1.7.config.json` - Keyboard tester configuration

### Documentation
- `RELEASE_NOTES_v2.0.md` - What's new in v2.0
- `SAFETY_REFACTORING_GUIDE.md` - Complete safety documentation
- `README.md` - Project overview

### Legacy Files
- Located in `legacy/` directory
- Included for backward compatibility

## System Requirements

- Windows 7 or higher
- Python 3.7 or higher
- Dependencies (installed automatically):
  - pywin32 >= 228
  - psutil >= 5.9.0
  - setuptools >= 65.5.1

## Documentation

For complete documentation, see:
- `RELEASE_NOTES_v2.0.md` - Release notes
- `SAFETY_REFACTORING_GUIDE.md` - Safety improvements
- `README.md` - General usage

## Support

- Issues: https://github.com/greogory/skt-smt/issues
- Documentation: https://github.com/greogory/skt-smt

## License

GNU General Public License v3.0 - See LICENSE.txt

---

**Version:** {VERSION}
**Release Date:** {datetime.now().strftime("%Y-%m-%d")}
**Codename:** "Fortress" - Complete Safety Hardening
"""

    readme_path = os.path.join(RELEASE_DIR, "QUICKSTART.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"  ✓ Created QUICKSTART.md")


def create_zip_archive():
    """Create a ZIP archive of the standalone package"""
    print_header("Creating ZIP Archive")

    zip_filename = f"{PROJECT_NAME}-v{VERSION}.zip"
    zip_path = os.path.join(DIST_DIR, zip_filename)

    # Ensure dist directory exists
    os.makedirs(DIST_DIR, exist_ok=True)

    print(f"→ Creating {zip_filename}...")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(RELEASE_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, RELEASE_DIR)
                zipf.write(file_path, arcname)
                print(f"  Adding: {arcname}")

    file_size = os.path.getsize(zip_path) / (1024 * 1024)  # MB
    print(f"✓ ZIP archive created: {zip_filename} ({file_size:.2f} MB)")

    return zip_path


def verify_build():
    """Verify that all expected files were created"""
    print_header("Verifying Build")

    expected_files = []

    # Check for wheel and sdist
    if os.path.exists(DIST_DIR):
        dist_files = os.listdir(DIST_DIR)
        print("→ Distribution files:")
        for file in dist_files:
            print(f"  ✓ {file}")
            expected_files.append(file)

    # Check standalone package
    if os.path.exists(RELEASE_DIR):
        print(f"\n→ Standalone package ({RELEASE_DIR}):")
        for root, dirs, files in os.walk(RELEASE_DIR):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), RELEASE_DIR)
                print(f"  ✓ {rel_path}")

    if len(expected_files) >= 2:  # Should have at least sdist and wheel
        print("\n✓ Build verification passed")
        return True
    else:
        print("\n✗ Build verification failed: Missing expected files")
        return False


def print_summary():
    """Print build summary"""
    print_header("Build Summary")

    print("📦 Build Complete!\n")
    print("Created distributions:")
    print(f"  • Source distribution (sdist)")
    print(f"  • Wheel distribution (bdist_wheel)")
    print(f"  • Standalone ZIP package\n")

    print("Output directories:")
    print(f"  • {DIST_DIR}/ - Python distributions and ZIP archive")
    print(f"  • {RELEASE_DIR}/ - Standalone package\n")

    print("Next steps:")
    print("  1. Test the distributions locally")
    print("  2. Upload to PyPI (if desired): twine upload dist/*")
    print("  3. Create GitHub release with ZIP archive")
    print("  4. Tag the release: git tag v{VERSION}\n")


def main():
    """Main build process"""
    print_header(f"Building {PROJECT_NAME} v{VERSION}")

    try:
        # Step 1: Clean
        clean_directories()

        # Step 2: Build Python distributions
        if not build_distributions():
            print("\n✗ Build failed at distribution step")
            return 1

        # Step 3: Create standalone package
        if not create_standalone_package():
            print("\n✗ Build failed at standalone package step")
            return 1

        # Step 4: Create ZIP archive
        zip_path = create_zip_archive()

        # Step 5: Verify
        if not verify_build():
            print("\n✗ Build verification failed")
            return 1

        # Step 6: Summary
        print_summary()

        return 0

    except Exception as e:
        print(f"\n✗ Build failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
