"""
Build standalone packages with all dependencies bundled.

This script creates multiple distribution formats:
1. Standalone executables (PyInstaller)
2. Bundled wheels package (offline installation)
3. Complete vendored package
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

VERSION = "2.0.0"
PROJECT_NAME = "input-testing-utility-suite"
BUILD_DIR = Path("build_standalone")
DIST_DIR = Path("dist")


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(f"Warnings: {result.stderr}")
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"❌ Required tool not found")
        return False


def check_dependencies():
    """Check if required build tools are available."""
    print("\n🔍 Checking build dependencies...")

    dependencies = {
        "python": ["python", "--version"],
        "pip": ["pip", "--version"],
    }

    optional = {
        "pyinstaller": ["pyinstaller", "--version"],
        "wheel": ["pip", "show", "wheel"],
    }

    all_ok = True
    for name, cmd in dependencies.items():
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"  ✅ {name} - available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  ❌ {name} - MISSING (required)")
            all_ok = False

    for name, cmd in optional.items():
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"  ✅ {name} - available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"  ⚠️  {name} - not installed (optional)")

    return all_ok


def download_dependencies():
    """Download all dependencies as wheels for offline installation."""
    print("\n📥 Downloading all dependencies...")

    wheels_dir = BUILD_DIR / "wheels"
    wheels_dir.mkdir(parents=True, exist_ok=True)

    # Download dependencies for Windows (both 32 and 64 bit)
    platforms = [
        "win_amd64",
        "win32",
    ]

    python_versions = ["cp37", "cp38", "cp39", "cp310", "cp311"]

    success = run_command(
        [
            "pip", "download",
            "-r", "requirements.txt",
            "--dest", str(wheels_dir),
            "--platform", "win_amd64",
            "--python-version", "3.11",
            "--only-binary", ":all:",
            "--no-deps"
        ],
        "Downloading dependencies (Python 3.11, Windows x64)"
    )

    if not success:
        print("⚠️  Failed to download some dependencies, trying without platform restrictions...")
        run_command(
            [
                "pip", "download",
                "-r", "requirements.txt",
                "--dest", str(wheels_dir),
            ],
            "Downloading dependencies (any platform)"
        )

    # Also download for current platform to ensure completeness
    run_command(
        [
            "pip", "download",
            "-r", "requirements.txt",
            "--dest", str(wheels_dir),
        ],
        "Downloading dependencies (current platform)"
    )

    wheel_files = list(wheels_dir.glob("*.whl")) + list(wheels_dir.glob("*.tar.gz"))
    print(f"\n✅ Downloaded {len(wheel_files)} dependency files to {wheels_dir}")

    return wheels_dir


def create_bundled_package():
    """Create a package with all wheels bundled for offline installation."""
    print("\n📦 Creating bundled wheels package...")

    wheels_dir = download_dependencies()

    # Create package directory
    bundle_dir = BUILD_DIR / f"{PROJECT_NAME}-v{VERSION}-bundled"
    bundle_dir.mkdir(parents=True, exist_ok=True)

    # Copy wheels
    bundle_wheels = bundle_dir / "wheels"
    if bundle_wheels.exists():
        shutil.rmtree(bundle_wheels)
    shutil.copytree(wheels_dir, bundle_wheels)

    # Copy main files
    files_to_copy = [
        "skt-2.0.py",
        "smt-2.0.py",
        "base_input_tester_2.0.py",
        "requirements.txt",
        "README.md",
        "LICENSE.txt",
        "RELEASE_NOTES_v2.0.md",
    ]

    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, bundle_dir)

    # Create installation script
    install_script = bundle_dir / "install_bundled.bat"
    install_script.write_text("""@echo off
REM Install Input Testing Utility Suite from bundled wheels

echo ====================================
echo Input Testing Utility Suite v2.0.0
echo Offline Installation
echo ====================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or later from python.org
    pause
    exit /b 1
)

echo Installing dependencies from bundled wheels...
pip install --no-index --find-links=wheels -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Installation failed
    pause
    exit /b 1
)

echo.
echo ====================================
echo Installation Complete!
echo ====================================
echo.
echo To run the tools:
echo   python skt-2.0.py    (keyboard tester)
echo   python smt-2.0.py    (mouse tester)
echo.
pause
""", encoding="utf-8")

    # Create README for bundled package
    readme = bundle_dir / "INSTALL.txt"
    readme.write_text(f"""
Input Testing Utility Suite v{VERSION} - Bundled Package
{'='*60}

This package includes all Python dependencies bundled for offline installation.

REQUIREMENTS:
- Python 3.7 or later
- Windows operating system

INSTALLATION:
1. Double-click install_bundled.bat
   OR
2. Run manually:
   pip install --no-index --find-links=wheels -r requirements.txt

USAGE:
- Keyboard tester: python skt-2.0.py
- Mouse tester: python smt-2.0.py

WHAT'S INCLUDED:
- All Python scripts
- All dependencies as wheel files
- Documentation
- License files

For more information, see README.md
""", encoding="utf-8")

    # Create ZIP archive
    archive_name = f"{PROJECT_NAME}-v{VERSION}-bundled"
    archive_path = DIST_DIR / archive_name

    DIST_DIR.mkdir(exist_ok=True)

    print(f"\n📦 Creating archive: {archive_path}.zip")
    shutil.make_archive(str(archive_path), "zip", BUILD_DIR, f"{PROJECT_NAME}-v{VERSION}-bundled")

    print(f"✅ Bundled package created: {archive_path}.zip")

    return archive_path


def create_pyinstaller_exe():
    """Create standalone executables using PyInstaller."""
    print("\n🔨 Creating standalone executables with PyInstaller...")

    # Check if PyInstaller is available
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller not installed")
        print("   Install with: pip install pyinstaller")
        return None

    exe_dir = BUILD_DIR / "executables"
    exe_dir.mkdir(parents=True, exist_ok=True)

    scripts = [
        ("skt-2.0.py", "SafeKeyboardTester"),
        ("smt-2.0.py", "SafeMouseTester"),
    ]

    executables = []

    for script, name in scripts:
        print(f"\n🔨 Building {name}...")

        success = run_command(
            [
                "pyinstaller",
                "--onefile",
                "--windowed",
                "--name", name,
                "--distpath", str(exe_dir),
                "--workpath", str(BUILD_DIR / "build"),
                "--specpath", str(BUILD_DIR / "specs"),
                script
            ],
            f"Building {name}.exe"
        )

        if success:
            exe_file = exe_dir / f"{name}.exe"
            if exe_file.exists():
                executables.append(exe_file)
                print(f"✅ Created: {exe_file}")

    if executables:
        # Create package with executables
        exe_package_dir = BUILD_DIR / f"{PROJECT_NAME}-v{VERSION}-executables"
        exe_package_dir.mkdir(parents=True, exist_ok=True)

        # Copy executables
        for exe in executables:
            shutil.copy2(exe, exe_package_dir)

        # Copy documentation
        docs = ["README.md", "LICENSE.txt", "RELEASE_NOTES_v2.0.md"]
        for doc in docs:
            if os.path.exists(doc):
                shutil.copy2(doc, exe_package_dir)

        # Create usage instructions
        usage = exe_package_dir / "USAGE.txt"
        usage.write_text(f"""
Input Testing Utility Suite v{VERSION} - Standalone Executables
{'='*60}

REQUIREMENTS:
- Windows 7 or later (64-bit)
- No Python installation required!

WHAT'S INCLUDED:
- SafeKeyboardTester.exe - Keyboard input testing utility
- SafeMouseTester.exe - Mouse input testing utility

USAGE:
1. Double-click SafeKeyboardTester.exe or SafeMouseTester.exe
2. Follow the on-screen prompts

FEATURES:
- No installation required
- No Python dependencies needed
- Complete safety validation
- Window bounds protection

For detailed documentation, see README.md

NOTE: Windows may show a SmartScreen warning for unsigned executables.
This is normal for new executables. Click "More info" then "Run anyway".
""", encoding="utf-8")

        # Create ZIP archive
        archive_name = f"{PROJECT_NAME}-v{VERSION}-executables"
        archive_path = DIST_DIR / archive_name

        print(f"\n📦 Creating archive: {archive_path}.zip")
        shutil.make_archive(str(archive_path), "zip", BUILD_DIR, f"{PROJECT_NAME}-v{VERSION}-executables")

        print(f"✅ Executable package created: {archive_path}.zip")

        return archive_path

    return None


def create_wheel_package():
    """Create a proper Python wheel package."""
    print("\n🎡 Creating Python wheel package...")

    success = run_command(
        ["pip", "install", "--upgrade", "wheel", "setuptools"],
        "Upgrading wheel and setuptools"
    )

    if not success:
        print("⚠️  Could not upgrade wheel/setuptools, using existing versions")

    # Build wheel
    run_command(
        ["python", "setup.py", "bdist_wheel"],
        "Building wheel package"
    )

    # Build source distribution
    run_command(
        ["python", "setup.py", "sdist"],
        "Building source distribution"
    )

    wheel_files = list(DIST_DIR.glob("*.whl"))
    if wheel_files:
        print(f"\n✅ Created wheel: {wheel_files[-1]}")
        return wheel_files[-1]

    return None


def main():
    """Main build process."""
    print(f"""
{'='*60}
Input Testing Utility Suite v{VERSION}
Standalone Package Builder
{'='*60}
""")

    # Check dependencies
    if not check_dependencies():
        print("\n❌ Missing required dependencies")
        sys.exit(1)

    # Clean previous builds
    if BUILD_DIR.exists():
        print(f"\n🧹 Cleaning previous build directory: {BUILD_DIR}")
        shutil.rmtree(BUILD_DIR)

    BUILD_DIR.mkdir(exist_ok=True)
    DIST_DIR.mkdir(exist_ok=True)

    results = {}

    # Create bundled package (always works)
    print("\n" + "="*60)
    print("OPTION 1: Bundled Wheels Package (Offline Installation)")
    print("="*60)
    try:
        results['bundled'] = create_bundled_package()
    except Exception as e:
        print(f"❌ Failed to create bundled package: {e}")
        results['bundled'] = None

    # Create wheel package
    print("\n" + "="*60)
    print("OPTION 2: Python Wheel Package (PyPI-compatible)")
    print("="*60)
    try:
        results['wheel'] = create_wheel_package()
    except Exception as e:
        print(f"❌ Failed to create wheel package: {e}")
        results['wheel'] = None

    # Create executables (optional)
    print("\n" + "="*60)
    print("OPTION 3: Standalone Executables (No Python Required)")
    print("="*60)
    try:
        results['executables'] = create_pyinstaller_exe()
    except Exception as e:
        print(f"❌ Failed to create executables: {e}")
        results['executables'] = None

    # Summary
    print("\n" + "="*60)
    print("BUILD SUMMARY")
    print("="*60)

    for name, result in results.items():
        if result:
            print(f"✅ {name.title()}: {result}")
        else:
            print(f"❌ {name.title()}: Failed or skipped")

    print(f"\n📂 All packages in: {DIST_DIR.absolute()}")

    # List all files in dist
    print(f"\n📦 Distribution files:")
    for file in sorted(DIST_DIR.glob("*")):
        size = file.stat().st_size / 1024
        print(f"   {file.name} ({size:.1f} KB)")

    print("\n✅ Build process complete!")


if __name__ == "__main__":
    main()
