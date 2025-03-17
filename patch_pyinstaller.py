#!/usr/bin/env python3
"""
Patch PyInstaller build_main.py to fix a syntax error in Python 3.13
"""

import os
import sys
import PyInstaller

# Get the path to the PyInstaller build_main.py file
pyinstaller_path = PyInstaller.__path__[0]
build_main_path = os.path.join(pyinstaller_path, "building", "build_main.py")

print(f"Patching PyInstaller build_main.py at: {build_main_path}")

# Read the file line by line
with open(build_main_path, 'r') as f:
    lines = f.readlines()

# Find and replace the problematic line with the exact pattern
patched = False
for i, line in enumerate(lines):
    if 'if re.search(r"[\\\\/]" modnm):' in line:
        print(f"Found problematic line at line {i+1}: {line.strip()}")
        lines[i] = line.replace('if re.search(r"[\\\\/]" modnm):', 'if re.search(r"[\\\\/]", modnm):')
        patched = True
        print(f"Patched to: {lines[i].strip()}")
        break

if not patched:
    print("Problematic line not found. Let's try a different approach.")
    
    # Try a different approach by reading the whole file
    with open(build_main_path, 'r') as f:
        content = f.read()
    
    # Replace the problematic pattern
    new_content = content.replace('if re.search(r"[\\\\/]" modnm):', 'if re.search(r"[\\\\/]", modnm):')
    
    if content == new_content:
        print("Pattern still not found. Manual intervention may be required.")
        sys.exit(1)
    else:
        print("Found and replaced the pattern in the file content.")
        patched = True
        
        # Write the patched content
        try:
            with open(build_main_path, 'w') as f:
                f.write(new_content)
            print("Successfully patched PyInstaller build_main.py")
        except PermissionError:
            print("Permission denied. Try running with sudo.")
            sys.exit(1)

if not patched:
    print("Failed to patch the file.")
    sys.exit(1)
else:
    print("Patch completed successfully.")
