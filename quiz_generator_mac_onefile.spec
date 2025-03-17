# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_all

block_cipher = None

# Collect all modules and data files
all_hiddenimports = []
all_datas = []

# Collect all for key packages
for pkg in ['anthropic', 'mcp', 'openai', 'groq', 'quiz_generator']:
    try:
        pkg_imports, pkg_datas, pkg_binaries = collect_all(pkg)
        all_hiddenimports.extend(pkg_imports)
        all_datas.extend(pkg_datas)
    except Exception as e:
        print(f"Warning: Could not collect all for {pkg}: {e}")

# Add additional data files
additional_data = [
    ('logs', 'logs'),
    ('output', 'output'),
]

a = Analysis(
    ['quiz_generator_server.py'],
    pathex=[],
    binaries=[],
    datas=all_datas + additional_data,
    hiddenimports=all_hiddenimports + [
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
