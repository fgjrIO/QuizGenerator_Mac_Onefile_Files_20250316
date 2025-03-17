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
pip3 install -q anthropic mcp[cli] openai groq pyinstaller typer
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

# Create a patched version of PyInstaller's build_main.py
echo "Creating a patched version of PyInstaller..."
PYINSTALLER_PATH=$(python3 -c "import PyInstaller; print(PyInstaller.__path__[0])")
BUILD_MAIN_PATH="$PYINSTALLER_PATH/building/build_main.py"

# Create a backup of the original file
BACKUP_PATH="$BUILD_MAIN_PATH.bak"
cp "$BUILD_MAIN_PATH" "$BACKUP_PATH"
echo "Created backup at $BACKUP_PATH"

# Apply the patch using sed
echo "Applying patch to PyInstaller..."
sed -i.bak 's/if re.search(r"[\\\/]" modnm):/if re.search(r"[\\\/]", modnm):/' "$BUILD_MAIN_PATH"

# Run PyInstaller with the onefile spec
echo "Building executable with PyInstaller (one-file mode)..."
pyinstaller --clean quiz_generator_mac_onefile.spec
BUILD_RESULT=$?

# Restore the backup
echo "Restoring PyInstaller backup..."
cp "$BACKUP_PATH" "$BUILD_MAIN_PATH"

# Check if the build was successful
if [ $BUILD_RESULT -ne 0 ]; then
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
