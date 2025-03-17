#!/bin/bash
echo "Creating Mac One-File Package..."
echo

# Check if the executable exists
if [ ! -f "dist/quiz_generator" ]; then
    echo "The dist/quiz_generator file does not exist."
    echo "Please run build_mac_onefile.sh first."
    exit 1
fi

# Create a timestamp for the release
timestamp=$(date +"%Y%m%d")

# Create a package directory
package_dir="QuizGenerator_Mac_Onefile_${timestamp}"
if [ -d "$package_dir" ]; then
    echo "Cleaning up existing package directory..."
    rm -rf "$package_dir"
fi
mkdir -p "$package_dir"
mkdir -p "$package_dir/logs"
mkdir -p "$package_dir/output"

# Copy files to the package directory
echo "Copying files to package directory..."
cp "dist/quiz_generator" "$package_dir/"
cp "README_MAC.md" "$package_dir/README.md"
cp "LICENSE" "$package_dir/"

# Create a simple run script
echo "Creating run script..."
cat > "$package_dir/run_quiz_generator.sh" << 'EOF'
#!/bin/bash
echo "Starting Quiz Generator..."
echo
echo "This application requires API keys for at least one of the following services:"
echo "- Anthropic (ANTHROPIC_API_KEY)"
echo "- OpenAI (OPENAI_API_KEY)"
echo "- GROQ (GROQ_API_KEY)"
echo "- OpenRouter (OPENROUTER_API_KEY)"
echo "- Ollama (local installation)"
echo
echo "If you don't have any API keys set up, the application will guide you through the setup process."
echo
echo "Press any key to continue..."
read -n 1 -s

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Run the executable
"$SCRIPT_DIR/quiz_generator"
EOF

# Make the scripts executable
chmod +x "$package_dir/quiz_generator"
chmod +x "$package_dir/run_quiz_generator.sh"

# Create a ZIP file
echo "Creating ZIP file..."
zip -r "${package_dir}.zip" "$package_dir"

if [ $? -ne 0 ]; then
    echo "Failed to create ZIP file."
    echo "You can still find the package in $package_dir"
    exit 1
fi

# Clean up the package directory
rm -rf "$package_dir"

echo
echo "Mac one-file package created successfully!"
echo "The package is located at ${package_dir}.zip"
echo
echo "To use this package on a Mac:"
echo "1. Extract the ZIP file"
echo "2. Open Terminal and navigate to the extracted directory"
echo "3. Run: ./run_quiz_generator.sh"
echo "   or directly run: ./quiz_generator"
echo
