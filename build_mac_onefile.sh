#!/bin/bash
echo "Building Quiz Generator Executable (One-File Version) for macOS..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed or not in PATH."
    echo "Please install Python 3.10 or later and try again."
    exit 1
fi

# Check if required packages are installed
echo "Checking required packages..."
pip3 install -q anthropic mcp openai groq pyinstaller
if [ $? -ne 0 ]; then
    echo "Failed to install required packages."
    exit 1
fi

# Create logs and output directories if they don't exist
mkdir -p logs
mkdir -p output

# Clean up previous build
echo "Cleaning up previous build..."
rm -rf build dist

# Run PyInstaller with the onefile spec
echo "Building executable with PyInstaller (one-file mode)..."
pyinstaller --clean quiz_generator_mac_onefile.spec
if [ $? -ne 0 ]; then
    echo "Failed to build executable."
    exit 1
fi

# Make the executable executable
chmod +x dist/quiz_generator

echo
echo "Build completed successfully!"
echo "The executable is located at dist/quiz_generator"
echo
echo "You can run the application directly with: ./dist/quiz_generator"
echo
