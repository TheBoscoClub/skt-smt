"""
Setup script for Input Testing Utility Suite v2.0
"""

from setuptools import setup, find_packages
import os

# Read the long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="input-testing-utility-suite",
    version="2.0.0",
    author="Input Testing Utility Suite Contributors",
    author_email="",
    description="Safe keyboard and mouse input testing utilities with comprehensive window bounds validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/greogory/skt-smt",
    project_urls={
        "Bug Tracker": "https://github.com/greogory/skt-smt/issues",
        "Documentation": "https://github.com/greogory/skt-smt",
        "Source Code": "https://github.com/greogory/skt-smt",
        "Release Notes": "https://github.com/greogory/skt-smt/blob/main/RELEASE_NOTES_v2.0.md",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Human Interface Device (HID)",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
        "Environment :: Console",
    ],
    keywords="testing, input, keyboard, mouse, automation, windows, safety, validation",
    packages=find_packages(),
    py_modules=[
        "base_input_tester_2_0",
        "skt-2.0",
        "smt-2.0",
        # Legacy modules for backward compatibility
        "base_input_tester_1.7",
        "base_input_tester_1_8",
        "skt-1.7",
        "skt-1.8",
        "smt-1.7",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "safe-mouse-tester=smt-2.0:main",
            "safe-keyboard-tester=skt-2.0:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "*.json",
            "*.md",
            "*.txt",
            "*.odt",
            "*.README",
        ],
    },
    zip_safe=False,
    platforms=["Windows"],
    license="GPL-3.0",
    license_files=["LICENSE.txt", "skmt.LICENSE"],
)
