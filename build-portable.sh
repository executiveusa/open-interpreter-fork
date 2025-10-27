#!/bin/bash

# Build script for creating a portable version of Open Interpreter with UI-TARS support

echo "Building portable Open Interpreter with UI-TARS support..."

# Create build directory
BUILD_DIR="open-interpreter-portable"
mkdir -p $BUILD_DIR

# Create virtual environment
python -m venv $BUILD_DIR/venv

# Activate virtual environment
source $BUILD_DIR/venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Open Interpreter with UI-TARS support
pip install ".[ui-tars,server,local]"

# Create startup script
cat > $BUILD_DIR/start.sh << 'EOF'
#!/bin/bash
# Startup script for portable Open Interpreter

# Activate virtual environment
source venv/bin/activate

# Start Open Interpreter server
interpreter --server
EOF

# Make startup script executable
chmod +x $BUILD_DIR/start.sh

# Create Windows batch file
cat > $BUILD_DIR/start.bat << 'EOF'
@echo off
REM Startup script for portable Open Interpreter on Windows

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start Open Interpreter server
interpreter --server
EOF

# Create README
cat > $BUILD_DIR/README.md << 'EOF'
# Portable Open Interpreter with UI-TARS

This is a portable installation of Open Interpreter with UI-TARS support for enhanced browser control.

## System Requirements

- Python 3.9 or higher
- At least 15GB free disk space
- For GPU support: CUDA-compatible NVIDIA GPU

## Installation

This package is pre-configured. Simply run the appropriate startup script for your platform.

## Usage

### Linux/macOS:
```bash
./start.sh
```

### Windows:
```cmd
start.bat
```

## Access

Once started, the server will be available at http://localhost:8000

## Notes

- The UI-TARS model will be downloaded on first use (approximately 13GB)
- Ensure sufficient disk space is available
- For GPU support, ensure CUDA drivers are properly installed
EOF

echo "Portable build complete! Find it in the $BUILD_DIR directory."