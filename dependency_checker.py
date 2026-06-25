# -*- coding: utf-8 -*-
"""
Dependency checker for QuODK plugin. Written by Claude but badly (not actually working in Windows),
so hacked even more severely to provide just instructions
Provides platform-independent package checking and instructions to install manually
"""

import sys
import subprocess
import platform

# Required packages with minimum versions
REQUIRED_PACKAGES = {
    'pandas': '1.3.0',
    'requests': '2.25.0',
    'cryptography': '45.0.0'
}


def check_package(package_name, min_version=None):
    """
    Check if a package is installed and optionally verify version.

    Args:
        package_name: Name of package to check
        min_version: Minimum version required (optional)

    Returns:
        tuple: (is_installed: bool, installed_version: str or None)
    """
    try:
        # Try using importlib.metadata (Python 3.8+)

        from importlib import metadata

        version = metadata.version(package_name)

        if min_version:
            # Check version if specified
            try:
                from packaging import version as pkg_version
                if pkg_version.parse(version) < pkg_version.parse(min_version):
                    return False, version
            except ImportError:
                # packaging not available, do simple string comparison
                if version < min_version:
                    return False, version

        return True, version
    except metadata.PackageNotFoundError:
        return False, None
    except Exception:
        # Any other error, assume not installed
        return False, None


def get_missing_packages():
    """
    Check all required packages and return list of missing ones.

    Returns:
        list: List of dicts with package info:
              [{'name': 'pandas', 'min_version': '1.3.0', 'current': None}, ...]
    """
    missing = []

    for package, min_version in REQUIRED_PACKAGES.items():
        is_installed, current_version = check_package(package, min_version)

        if not is_installed:
            missing.append({
                'name': package,
                'min_version': min_version,
                'current': current_version
            })

    return missing


def get_manual_install_instructions(packages):
    """
    Generate platform-specific manual installation instructions.

    Args:
        packages: List of package dicts with 'name' and 'min_version'

    Returns:
        str: Multi-line instructions for manual installation
    """
    system = platform.system()
    package_list = ' '.join([p['name'] for p in packages])

    if system == 'Windows':
        return f"""Manual Installation Instructions (Windows):

Method 1 - OSGeo4W Shell (Recommended):
1. Open OSGeo4W Shell as Administrator
   (Right-click OSGeo4W Shell → Run as Administrator)
2. Run these commands:
   py3_env
   python3 -m pip install --user {package_list}
3. Restart QGIS

Method 2 - Command Prompt:
1. Open Command Prompt as Administrator
2. Navigate to QGIS Python directory:
   cd "C:\\Program Files\\QGIS 3.xx\\apps\\Python39"
   (Adjust version numbers as needed)
3. Run:
   python.exe -m pip install --user {package_list}
4. Restart QGIS

Method 3 - QGIS Python Console:
1. Open QGIS
2. Go to Plugins → Python Console
3. Run:
   import subprocess, sys
   subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', '{package_list}'])
4. Restart QGIS
"""

    elif system == 'Darwin':  # macOS
        return f"""Manual Installation Instructions (macOS):

Method 1 - Terminal (Recommended):
1. Open Terminal
2. Run this command:
   pip3 install --user {package_list}
3. Restart QGIS

Method 2 - QGIS Python:
If QGIS uses its own Python installation:
1. Find QGIS Python path (usually):
   /Applications/QGIS.app/Contents/MacOS/bin/python3
2. Run:
   /Applications/QGIS.app/Contents/MacOS/bin/python3 -m pip install --user {package_list}
3. Restart QGIS

Method 3 - QGIS Python Console:
1. Open QGIS
2. Go to Plugins → Python Console
3. Run:
   import subprocess, sys
   subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', '{package_list}'])
4. Restart QGIS
"""

    else:  # Linux
        return f"""Manual Installation Instructions (Linux):

Method 1 - pip (Recommended):
1. Open Terminal
2. Run this command:
   pip3 install --user {package_list}

   If you need system-wide installation:
   sudo pip3 install {package_list}
3. Restart QGIS

Method 2 - System Package Manager:
Debian/Ubuntu:
   sudo apt update
   sudo apt install python3-pandas python3-requests python3-cryptography

Fedora/RHEL:
   sudo dnf install python3-pandas python3-requests python3-cryptography

Arch Linux:
   sudo pacman -S python-pandas python-requests python-cryptography

Method 3 - QGIS Python Console:
1. Open QGIS
2. Go to Plugins → Python Console
3. Run:
   import subprocess, sys
   subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', '{package_list}'])
4. Restart QGIS
"""


def check_dependencies():
    """
    Main entry point: Check all dependencies.

    Returns:
        list: Missing packages (empty list if all installed)
    """
    return get_missing_packages()
