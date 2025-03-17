# Quiz Generator for macOS

This is the macOS version of the Quiz Generator application. It allows you to create quizzes with various question types on any topic.

## Prerequisites

- macOS 10.14 or later
- Python 3.10 or later

## Installation Options

### Option 1: Standalone Executable (Recommended)

1. Download and extract the standalone executable ZIP file to a location of your choice.
2. Open Terminal and navigate to the extracted directory.
3. Make the executable and run script executable by running:
   ```
   chmod +x quiz_generator run_quiz_generator.sh
   ```
4. Run the application directly:
   ```
   ./quiz_generator
   ```
   Or use the run script:
   ```
   ./run_quiz_generator.sh
   ```

### Option 2: Build from Source

1. Download and extract the source ZIP file to a location of your choice.
2. Open Terminal and navigate to the extracted directory.
3. Make the scripts executable by running:
   ```
   chmod +x build_mac_onefile.sh build_executable.sh run_quiz_generator.sh create_release_package.sh create_mac_onefile_package.sh
   ```

## Building the Executable

### Building a Single-File Executable (Recommended)

1. Open Terminal and navigate to the extracted directory.
2. Run the onefile build script:
   ```
   ./build_mac_onefile.sh
   ```
3. This will create a single-file executable in the `dist` directory.

### Building a Multi-File Executable

1. Open Terminal and navigate to the extracted directory.
2. Run the standard build script:
   ```
   ./build_executable.sh
   ```
3. This will create the executable in the `dist` directory.

## Running the Application

### Running the Single-File Executable

1. After building the executable, you can run it directly:
   ```
   ./dist/quiz_generator
   ```

### Running the Multi-File Executable

1. After building the executable, you can run it using:
   ```
   ./run_quiz_generator.sh
   ```
2. Alternatively, you can directly run the executable:
   ```
   ./dist/quiz_generator
   ```

## API Keys

The application requires at least one of the following API keys:

- Anthropic (ANTHROPIC_API_KEY)
- OpenAI (OPENAI_API_KEY)
- GROQ (GROQ_API_KEY)
- OpenRouter (OPENROUTER_API_KEY)
- Ollama (local installation)

You can set these environment variables in your shell profile (e.g., `~/.zshrc` or `~/.bash_profile`):

```bash
export ANTHROPIC_API_KEY="your-api-key"
export OPENAI_API_KEY="your-api-key"
export GROQ_API_KEY="your-api-key"
export OPENROUTER_API_KEY="your-api-key"
```

## Creating a Distribution Package

### Creating a Single-File Distribution Package (Recommended)

If you want to create a distributable package with the single-file executable:

1. Build the executable first using `./build_mac_onefile.sh`
2. Run the onefile package script:
   ```
   ./create_mac_onefile_package.sh
   ```
3. This will create a ZIP file that contains just the executable and necessary files.

### Creating a Standard Distribution Package

If you want to create a distributable package with the multi-file executable:

1. Build the executable first using `./build_executable.sh`
2. Run the release package script:
   ```
   ./create_release_package.sh
   ```
3. This will create a ZIP file in the `release` directory.

## Troubleshooting

- If you encounter permission issues, make sure the scripts are executable:
  ```
  chmod +x build_executable.sh run_quiz_generator.sh create_release_package.sh
  ```

- If you see "Operation not permitted" errors, you may need to allow Terminal to access files in System Preferences > Security & Privacy > Privacy > Full Disk Access.

- If the application fails to start, check if Python and the required packages are installed:
  ```
  python3 --version
  pip3 install anthropic mcp openai groq pyinstaller
  ```

## Creating a macOS App Bundle (Optional)

If you want to create a proper macOS .app bundle:

1. Edit the `quiz_generator_mac.spec` file
2. Uncomment the BUNDLE section at the bottom of the file
3. Run the build script again:
   ```
   ./build_executable.sh
   ```
4. This will create a `quiz_generator.app` in the `dist` directory
