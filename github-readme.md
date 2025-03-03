# SKT-SMT: Input Testing Utility Suite

## Overview

The Input Testing Utility Suite is a comprehensive set of tools designed to simulate human-like keyboard and mouse interactions within an isolated environment. This suite allows you to generate realistic typing patterns, mouse movements, and clicks without interfering with other programs on your system.

## Key Components

The suite consists of three main components:

1. **BaseInputTester** - The foundation class that provides common functionality for all testing tools
2. **SafeKeyboardTester (SKT)** - An advanced utility for keyboard input simulation
3. **SafeMouseTester (SMT)** - An advanced utility for mouse input simulation

## Features

- **Isolated Testing Environment**: All input events occur in special windows that don't interfere with your other applications
- **Realistic Human-Like Behavior**: Sophisticated algorithms create input patterns that closely mimic actual human behavior
- **Highly Configurable**: Extensive configuration options let you customize every aspect of the simulation
- **Resource Efficient**: Built-in monitoring and cleanup routines prevent resource leaks during extended testing
- **Detailed Logging**: Comprehensive logging of all activities for analysis and troubleshooting

## Keyboard Testing Features

- Multiple typing patterns (common words, random words, sentences, code snippets)
- Variable typing speeds
- Realistic typos with corrections
- Natural pauses between keystrokes
- Special key press simulation

## Mouse Testing Features

- Multiple movement patterns (random, linear, circular, targeted)
- Natural acceleration and deceleration
- Click, double-click, and scroll simulation
- Configurable movement physics
- Target-based movement simulation

## System Requirements

- Windows operating system
- Python 3.6 or higher
- Required Python packages:
  - win32api, win32gui, win32con (from pywin32)
  - psutil
  - ctypes (standard library)

## Quick Start

1. Install required packages:
   ```
   pip install pywin32 psutil
   ```

2. Run the keyboard tester:
   ```
   python skt-1.7.py
   ```

3. Run the mouse tester:
   ```
   python smt-1.7.py
   ```

4. To stop any test, press the **Escape** key.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0).

## Documentation

For more detailed information, please refer to the User Manual included in this repository.
