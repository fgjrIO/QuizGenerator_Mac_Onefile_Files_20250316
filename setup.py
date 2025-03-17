
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
