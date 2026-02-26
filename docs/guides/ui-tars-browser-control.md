# UI-TARS Browser Control Integration

This guide explains how to use the UI-TARS-1.5-7B model for enhanced browser control in Open Interpreter.

## Overview

UI-TARS-1.5-7B is a multimodal vision-language model specifically designed for GUI interaction tasks. It excels at:
- Understanding web page layouts
- Identifying interactive elements
- Providing precise element descriptions
- Suggesting appropriate actions

The integration enhances Open Interpreter's browser automation capabilities by providing more accurate visual understanding.

## Installation

To use UI-TARS with Open Interpreter, you need to install the additional dependencies:

```bash
pip install 'open-interpreter[ui-tars]'
```

Or if installing from source:

```bash
pip install accelerate bitsandbytes
```

## Usage

### Enabling UI-TARS

UI-TARS is enabled by default in the browser module. You can explicitly enable or disable it:

```python
from interpreter import interpreter

# Enable UI-TARS (default)
interpreter.computer.browser.use_ui_tars = True

# Disable UI-TARS
interpreter.computer.browser.use_ui_tars = False
```

### Using UI-TARS Directly

You can also use the UI-TARS vision module directly:

```python
from interpreter.core.computer.vision.ui_tars.ui_tars_vision import UiTarsVision

# Initialize UI-TARS
ui_tars = UiTarsVision(interpreter.computer)

# Analyze an image
result = ui_tars.query(
    query="Describe the interactive elements in this image",
    path="screenshot.png"
)
```

## Features

### Enhanced Page Analysis

When UI-TARS is enabled, the browser's `analyze_page()` method will:
1. Capture a screenshot of the current page
2. Use UI-TARS to identify and describe interactive elements
3. Provide more accurate element positioning and functionality
4. Better understand the context of user intents

### Visual Element Identification

UI-TARS can identify:
- Buttons and their functions
- Input fields and their purposes
- Navigation elements
- Dropdown menus
- Links and their destinations
- Modal dialogs and overlays

## Performance Considerations

UI-TARS-1.5-7B is a large model that requires:
- Significant GPU memory (16GB+ recommended)
- Longer processing times for inference
- Internet connection for initial model download

For systems with limited resources, consider using the model in 4-bit quantized mode.

## Troubleshooting

### Model Loading Issues

If you encounter issues loading the UI-TARS model:

1. Ensure you have enough GPU memory
2. Try using 4-bit quantization:
   ```python
   # In ui_tars_vision.py, modify the model loading:
   self.model = AutoModelForCausalLM.from_pretrained(
       model_id,
       trust_remote_code=True,
       torch_dtype=torch.bfloat16,
       device_map="auto",
       quantization_config=BitsAndBytesConfig(
           load_in_4bit=True,
           bnb_4bit_compute_dtype=torch.bfloat16
       )
   )
   ```

### CUDA Out of Memory

If you encounter CUDA out of memory errors:
1. Reduce the max_new_tokens parameter in queries
2. Use CPU inference (much slower):
   ```python
   self.device = "cpu"
   ```

## Example Usage

```python
from interpreter import interpreter

# Navigate to a webpage
interpreter.computer.browser.go_to_url("https://example.com")

# Analyze the page with UI-TARS
interpreter.computer.browser.analyze_page("Find the login button")

# The output will include UI-TARS's enhanced analysis of the page
```

This integration significantly improves Open Interpreter's ability to understand and interact with web pages, making browser automation more reliable and accurate.