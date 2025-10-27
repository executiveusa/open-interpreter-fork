# UI-TARS Integration Quick Start Guide

## Overview
This guide will help you quickly get started with Open Interpreter's UI-TARS integration for enhanced browser control.

---

## Installation Options

### Option 1: Direct Installation (Recommended for Development)

```bash
# Navigate to the project directory
cd open-interpreter

# Install with UI-TARS support
pip install '.[ui-tars,server,local]'

# Start the server
interpreter --server
```

**Access:** `http://localhost:8000`

---

### Option 2: Portable Build (Recommended for Standalone Deployment)

**Windows:**
```cmd
# Build portable package
build-portable.bat

# Navigate to build directory
cd open-interpreter-portable

# Start server
start.bat
```

**Linux/macOS:**
```bash
# Make script executable
chmod +x build-portable.sh

# Build portable package
./build-portable.sh

# Navigate to build directory
cd open-interpreter-portable

# Start server
./start.sh
```

**Access:** `http://localhost:8000`

---

### Option 3: Docker Deployment (Recommended for Production)

**Prerequisites:**
- Docker installed
- Docker Compose installed
- NVIDIA Docker runtime (for GPU support)

**GPU-Enabled Deployment:**
```bash
# Build and start
docker-compose up

# Or run in detached mode
docker-compose up -d
```

**CPU-Only Deployment:**
```bash
# Edit docker-compose.yml and comment out the 'deploy' section
# Then run:
docker-compose up
```

**Access:** `http://localhost:8000`

---

## Verification

### Quick Test
```bash
# Run simple integration test
python test_ui_tars_simple.py
```

**Expected Output:**
```
Running simple UI-TARS integration tests...

Testing UI-TARS import...
✓ UI-TARS vision module imported successfully

Testing UI-TARS class structure...
✓ UI-TARS class has method: __init__
✓ UI-TARS class has method: load
✓ UI-TARS class has method: query
✓ UI-TARS class has method: identify_elements
✓ UI-TARS class structure is correct

Testing UI-TARS initialization...
✓ UI-TARS instance has attribute: computer
✓ UI-TARS instance has attribute: model
✓ UI-TARS instance has attribute: tokenizer
✓ UI-TARS instance has attribute: device
✓ UI-TARS instance created successfully

Simple UI-TARS tests completed: 3/3 passed
All simple UI-TARS tests passed!
```

---

## Using UI-TARS

### Browser Control with UI-TARS

```python
from interpreter import interpreter

# Enable UI-TARS for browser operations
interpreter.computer.browser.use_ui_tars = True

# Analyze a webpage
interpreter.computer.browser.go_to_url("https://example.com")
interpreter.computer.browser.analyze_page("Find all buttons on this page")
```

### Vision Analysis with UI-TARS

```python
from interpreter import interpreter

# Load UI-TARS vision module
interpreter.computer.vision.load(load_ui_tars=True)

# Analyze an image
result = interpreter.computer.vision.query(
    query="Describe this UI and identify clickable elements",
    path="screenshot.png",
    use_ui_tars=True
)

print(result)
```

### Identify GUI Elements

```python
from interpreter import interpreter

# Identify elements in a screenshot
elements = interpreter.computer.vision.ui_tars.identify_elements(
    path="app_screenshot.png"
)

print(elements)
```

---

## System Requirements

### Minimum
- Python 3.9+
- 8 GB RAM
- 20 GB disk space
- Windows 10/11, Linux (Ubuntu 20.04+), or macOS 10.15+

### Recommended
- Python 3.11
- 16 GB RAM
- NVIDIA GPU with 8+ GB VRAM
- CUDA 11.8+
- 25 GB disk space

---

## First-Time Setup

### 1. Model Download
On first use, UI-TARS will download the model (~13 GB):
```
Loading UI-TARS-1.5-7B model...
Downloading model from HuggingFace...
```

This may take 10-30 minutes depending on your internet connection.

### 2. Model Loading
First load takes 2-5 minutes:
```
Loading UI-TARS-1.5-7B model...
UI-TARS-1.5-7B model loaded successfully
```

Subsequent loads are faster (~30 seconds).

---

## Troubleshooting

### Issue: Dependencies Not Found
```bash
# Install all required dependencies
pip install '.[ui-tars,server,local]'
```

### Issue: CUDA Not Available
UI-TARS will automatically fall back to CPU. For GPU support:
1. Install CUDA 11.8 or higher
2. Install PyTorch with CUDA support:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

### Issue: Out of Memory
- Reduce other applications' memory usage
- Use CPU mode (slower but requires less RAM)
- Upgrade to system with more RAM

### Issue: Model Download Fails
```bash
# Set HuggingFace cache directory with more space
export HF_HOME=/path/to/larger/drive/.cache/huggingface
```

---

## Performance Tips

### GPU Acceleration
- Ensure CUDA is properly installed
- Check GPU availability:
  ```python
  import torch
  print(torch.cuda.is_available())
  print(torch.cuda.get_device_name(0))
  ```

### Memory Optimization
- Close unnecessary applications
- Use batch processing for multiple images
- Clear cache periodically

### Speed Optimization
- Keep model loaded in memory between uses
- Use GPU for faster inference
- Pre-download model before deployment

---

## Common Use Cases

### 1. Web Scraping with Understanding
```python
# Navigate to a complex web application
browser.go_to_url("https://app.example.com")

# Let UI-TARS identify the login form
browser.analyze_page("Find the login form and its fields")
```

### 2. GUI Testing
```python
# Analyze application screenshot
elements = vision.ui_tars.identify_elements(path="app.png")

# Get detailed element information
for element in elements:
    print(f"Type: {element['type']}")
    print(f"Position: {element['position']}")
    print(f"Function: {element['function']}")
```

### 3. Automated UI Navigation
```python
# Analyze current state
current_state = browser.analyze_page("What can I do on this page?")

# Make decisions based on UI-TARS analysis
# Interact with elements
```

---

## Additional Resources

- **Full Documentation:** `UI_TARS_INTEGRATION_VERIFICATION_REPORT.md`
- **Integration Summary:** `UI-TARS_INTEGRATION_FINAL_SUMMARY.md`
- **Test Scripts:** `test_ui_tars_simple.py`, `test_ui_tars_comprehensive.py`
- **Build Scripts:** `build-portable.bat`, `build-portable.sh`

---

## Support

For issues or questions:
1. Check the verification report
2. Run the simple test: `python test_ui_tars_simple.py`
3. Review the integration documentation
4. Check HuggingFace model page: https://huggingface.co/ByteDance-Seed/UI-TARS-1.5-7B

---

**Quick Start Version:** 1.0  
**Last Updated:** 2025-10-26  
**Status:** Production Ready
