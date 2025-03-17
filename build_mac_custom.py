#!/usr/bin/env python3
"""
Custom build script for Quiz Generator Mac executable
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
    print("Building Quiz Generator Executable for macOS...")
    
    # Create logs and output directories if they don't exist
    os.makedirs("logs", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # Clean up previous build
    print("Cleaning up previous build...")
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)
    
    # Install required packages
    print("Installing required packages...")
    success, output = run_command([sys.executable, "-m", "pip", "install", "-q", "anthropic", "mcp[cli]", "openai", "groq", "pyinstaller", "typer"])
    if not success:
        print("Failed to install required packages.")
        return 1
    
    # Create a simple spec file
    print("Creating custom spec file...")
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

import sys
import os

block_cipher = None

# Add additional data files
additional_data = [
    ('logs', 'logs'),
    ('output', 'output'),
]

a = Analysis(
    ['quiz_generator_server.py'],
    pathex=[],
    binaries=[],
    datas=additional_data,
    hiddenimports=[
        'anthropic',
        'mcp',
        'mcp.server.fastmcp',
        'openai',
        'groq',
        'json',
        'logging',
        'os',
        'webbrowser',
        'datetime',
        'subprocess',
        're',
        'sys',
        'ctypes',
        'typer',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Mac-specific configuration for a single-file executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='quiz_generator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=True,  # Enable argv emulation for macOS
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
"""
    
    with open("quiz_generator_custom.spec", "w") as f:
        f.write(spec_content)
    
    # Create a patched version of PyInstaller's build_main.py
    print("Creating a patched version of PyInstaller...")
    
    # Get the path to the PyInstaller build_main.py file
    import PyInstaller
    pyinstaller_path = PyInstaller.__path__[0]
    build_main_path = os.path.join(pyinstaller_path, "building", "build_main.py")
    
    # Create a backup of the original file
    backup_path = build_main_path + ".bak"
    shutil.copy2(build_main_path, backup_path)
    print(f"Created backup at {backup_path}")
    
    # Read the file
    with open(build_main_path, 'r') as f:
        content = f.read()
    
    # Apply the patch directly using string replacement
    patched_content = content.replace(
        'if re.search(r"[\\\\/]" modnm):',
        'if re.search(r"[\\\\/]", modnm):'
    )
    
    # Write the patched file
    with open(build_main_path, 'w') as f:
        f.write(patched_content)
    
    # Run PyInstaller with the custom spec
    print("Building executable with PyInstaller...")
    try:
        success, output = run_command([sys.executable, "-m", "PyInstaller", "--clean", "quiz_generator_custom.spec"])
        if not success:
            print("Failed to build executable.")
            # Restore the backup
            shutil.copy2(backup_path, build_main_path)
            return 1
        
        # Make the executable executable
        os.chmod("dist/quiz_generator", 0o755)
        
        print("\nBuild completed successfully!")
        print("The executable is located at dist/quiz_generator")
        print("\nYou can run the application directly with: ./dist/quiz_generator")
    finally:
        # Restore the backup
        print("Restoring PyInstaller backup...")
        shutil.copy2(backup_path, build_main_path)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
