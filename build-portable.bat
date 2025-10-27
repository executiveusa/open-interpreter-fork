@echo off
REM Build script for creating a portable version of Open Interpreter with UI-TARS support

echo Building portable Open Interpreter with UI-TARS support...

REM Create build directory
set BUILD_DIR=open-interpreter-portable
mkdir %BUILD_DIR%

REM Create virtual environment
python -m venv %BUILD_DIR%\venv

REM Activate virtual environment
call %BUILD_DIR%\venv\Scripts\activate.bat

REM Upgrade pip
pip install --upgrade pip

REM Install Open Interpreter with UI-TARS support
pip install ".[ui-tars,server,local]"

REM Create startup script
echo @echo off > %BUILD_DIR%\start.bat
echo REM Startup script for portable Open Interpreter >> %BUILD_DIR%\start.bat
echo. >> %BUILD_DIR%\start.bat
echo REM Activate virtual environment >> %BUILD_DIR%\start.bat
echo call venv\Scripts\activate.bat >> %BUILD_DIR%\start.bat
echo. >> %BUILD_DIR%\start.bat
echo REM Start Open Interpreter server >> %BUILD_DIR%\start.bat
echo interpreter --server >> %BUILD_DIR%\start.bat

REM Create PowerShell script
echo # Startup script for portable Open Interpreter > %BUILD_DIR%\start.ps1
echo # Activate virtual environment >> %BUILD_DIR%\start.ps1
echo .\venv\Scripts\Activate.ps1 >> %BUILD_DIR%\start.ps1
echo # Start Open Interpreter server >> %BUILD_DIR%\start.ps1
echo interpreter --server >> %BUILD_DIR%\start.ps1

REM Create README
echo # Portable Open Interpreter with UI-TARS > %BUILD_DIR%\README.md
echo. >> %BUILD_DIR%\README.md
echo This is a portable installation of Open Interpreter with UI-TARS support for enhanced browser control. >> %BUILD_DIR%\README.md
echo. >> %BUILD_DIR%\README.md
echo ## System Requirements >> %BUILD_DIR%\README.md
echo. >> %BUILD_DIR%\README.md
echo - Python 3.9 or higher >> %BUILD_DIR%\README.md
echo - At least 15GB free disk space >> %BUILD_DIR%\README.md
echo - For GPU support: CUDA-compatible NVIDIA GPU >> %BUILD_DIR%\README.md
echo. >> %BUILD_DIR%\README.md
echo ## Installation >> %BUILD_DIR%\README.md
echo. >> %BUILD_DIR%\README.md
echo This package is pre-configured. Simply run the appropriate startup script for your platform. >> %BUILD_DIR%\README.md
echo. >> %BUILD_DIR%\README.md
echo ## Usage >> %BUILD_DIR%\README.md
echo. >> %BUILD_DIR%\README.md
echo ### Windows Command Prompt: >> %BUILD_DIR%\README.md
echo ```cmd >> %BUILD_DIR%\README.md
echo start.bat >> %BUILD_DIR%\README.md
echo ``` >> %BUILD_DIR%\README.md
echo. >> %BUILD_DIR%\README.md
echo ### Windows PowerShell: >> %BUILD_DIR%\README.md
echo ```powershell >> %BUILD_DIR%\README.md
echo .\start.ps1 >> %BUILD_DIR%\README.md
echo ``` >> %BUILD_DIR%\README.md
echo. >> %BUILD_DIR%\README.md
echo ## Access >> %BUILD_DIR%\README.md
echo. >> %BUILD_DIR%\README.md
echo Once started, the server will be available at http://localhost:8000 >> %BUILD_DIR%\README.md
echo. >> %BUILD_DIR%\README.md
echo ## Notes >> %BUILD_DIR%\README.md
echo. >> %BUILD_DIR%\README.md
echo - The UI-TARS model will be downloaded on first use (approximately 13GB) >> %BUILD_DIR%\README.md
echo - Ensure sufficient disk space is available >> %BUILD_DIR%\README.md
echo - For GPU support, ensure CUDA drivers are properly installed >> %BUILD_DIR%\README.md

echo.
echo Portable build complete! Find it in the %BUILD_DIR% directory.