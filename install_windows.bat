@echo off
REM Installation script for Input Testing Utility Suite v2.0
REM Windows Batch Script

echo ================================================
echo Input Testing Utility Suite v2.0 Installation
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check Python version
echo Checking Python version...
python -c "import sys; exit(0 if sys.version_info >= (3, 7) else 1)"
if errorlevel 1 (
    echo ERROR: Python 3.7 or higher is required
    echo Please upgrade your Python installation
    pause
    exit /b 1
)

echo Python version is compatible
echo.

REM Ask user for installation method
echo Installation Options:
echo 1. Install in virtual environment (Recommended)
echo 2. Install globally
echo.
set /p choice="Enter your choice (1 or 2): "

if "%choice%"=="1" goto venv_install
if "%choice%"=="2" goto global_install

echo Invalid choice. Using virtual environment installation.
goto venv_install

:venv_install
echo.
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo To use the utilities:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run mouse tester: python smt-2.0.py
echo 3. Run keyboard tester: python skt-2.0.py
echo 4. Press ESC to stop testing
echo.
echo To deactivate: deactivate
echo.
pause
goto end

:global_install
echo.
echo Installing dependencies globally...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo To use the utilities:
echo - Run mouse tester: python smt-2.0.py
echo - Run keyboard tester: python skt-2.0.py
echo - Press ESC to stop testing
echo.
pause
goto end

:end
echo Installation script finished.
