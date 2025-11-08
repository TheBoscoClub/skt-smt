# Installation script for Input Testing Utility Suite v2.0
# PowerShell Script

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Input Testing Utility Suite v2.0 Installation" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
    Write-Host ""
}
catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.7 or higher from https://www.python.org/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$versionCheck = python -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python 3.7 or higher is required" -ForegroundColor Red
    Write-Host "Please upgrade your Python installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Python version is compatible" -ForegroundColor Green
Write-Host ""

# Ask user for installation method
Write-Host "Installation Options:" -ForegroundColor Cyan
Write-Host "1. Install in virtual environment (Recommended)" -ForegroundColor White
Write-Host "2. Install globally" -ForegroundColor White
Write-Host ""
$choice = Read-Host "Enter your choice (1 or 2)"

if ($choice -eq "1") {
    # Virtual environment installation
    Write-Host ""
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }

    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1

    Write-Host "Upgrading pip..." -ForegroundColor Yellow
    python -m pip install --upgrade pip

    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }

    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "Installation Complete!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "To use the utilities:" -ForegroundColor Cyan
    Write-Host "1. Activate the virtual environment: .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "2. Run mouse tester: python smt-2.0.py" -ForegroundColor White
    Write-Host "3. Run keyboard tester: python skt-2.0.py" -ForegroundColor White
    Write-Host "4. Press ESC to stop testing" -ForegroundColor White
    Write-Host ""
    Write-Host "To deactivate: deactivate" -ForegroundColor Yellow
    Write-Host ""
}
elseif ($choice -eq "2") {
    # Global installation
    Write-Host ""
    Write-Host "Upgrading pip..." -ForegroundColor Yellow
    python -m pip install --upgrade pip

    Write-Host "Installing dependencies globally..." -ForegroundColor Yellow
    pip install -r requirements.txt

    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }

    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "Installation Complete!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "To use the utilities:" -ForegroundColor Cyan
    Write-Host "- Run mouse tester: python smt-2.0.py" -ForegroundColor White
    Write-Host "- Run keyboard tester: python skt-2.0.py" -ForegroundColor White
    Write-Host "- Press ESC to stop testing" -ForegroundColor White
    Write-Host ""
}
else {
    Write-Host "Invalid choice. Installation cancelled." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Read-Host "Press Enter to exit"
