#!/usr/bin/env python3
"""
Build script for Quiz Generator Mac executable using py2app
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return its output"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False, result.stderr
    return True, result.stdout

def main():
    print("Building Quiz Generator Executable for macOS using py2app...")
    
    # Create logs and output directories if they don't exist
    os.makedirs("logs", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # Clean up previous build
    print("Cleaning up previous build...")
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)
    
    # Install required packages
    print("Installing required packages...")
    success, output = run_command([sys.executable, "-m", "pip", "install", "-q", "anthropic", "mcp[cli]", "openai", "groq", "py2app", "typer"])
    if not success:
        print("Failed to install required packages.")
        return 1
    
    # Create setup.py for py2app
    print("Creating setup.py for py2app...")
    setup_py_content = """
from setuptools import setup

APP = ['quiz_generator_server.py']
DATA_FILES = [
    ('logs', []),
    ('output', []),
]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['anthropic', 'mcp', 'openai', 'groq', 'typer', 'quiz_generator'],
    'includes': ['json', 'logging', 'os', 'webbrowser', 'datetime', 'subprocess', 're', 'sys', 'ctypes'],
    'iconfile': None,
    'plist': {
        'CFBundleName': 'Quiz Generator',
        'CFBundleDisplayName': 'Quiz Generator',
        'CFBundleIdentifier': 'com.quizgenerator',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
"""
    
    with open("setup.py", "w") as f:
        f.write(setup_py_content)
    
    # Run py2app
    print("Building executable with py2app...")
    success, output = run_command([sys.executable, "setup.py", "py2app"])
    if not success:
        print("Failed to build executable.")
        return 1
    
    # Create a single-file executable wrapper
    print("Creating a single-file executable wrapper...")
    wrapper_content = """#!/bin/bash
# Quiz Generator single-file executable wrapper

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the app bundle
"$DIR/dist/quiz_generator_server.app/Contents/MacOS/quiz_generator_server" "$@"
"""
    
    with open("dist/quiz_generator", "w") as f:
        f.write(wrapper_content)
    
    # Make the wrapper executable
    os.chmod("dist/quiz_generator", 0o755)
    
    print("\nBuild completed successfully!")
    print("The executable is located at dist/quiz_generator")
    print("The app bundle is located at dist/quiz_generator_server.app")
    print("\nYou can run the application directly with: ./dist/quiz_generator")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
