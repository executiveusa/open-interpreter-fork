"""
Comprehensive UI-TARS Integration Verification Script
This script verifies all aspects of the UI-TARS integration with Open Interpreter
"""

import sys
import traceback

def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80 + "\n")

def print_result(test_name, passed, details=""):
    """Print a test result"""
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {test_name}")
    if details:
        print(f"  {details}")
    return passed

# Test Results
results = {
    "passed": 0,
    "failed": 0,
    "warnings": 0
}

# ==============================================================================
# TEST 1: Module Imports
# ==============================================================================
print_section("TEST 1: Module Imports")

try:
    from interpreter.core.computer.vision.ui_tars.ui_tars_vision import UiTarsVision
    passed = print_result("UI-TARS vision module import", True)
    results["passed"] += 1
except Exception as e:
    passed = print_result("UI-TARS vision module import", False, str(e))
    results["failed"] += 1

try:
    from interpreter.core.computer.vision.vision import Vision
    passed = print_result("Vision module import", True)
    results["passed"] += 1
except Exception as e:
    passed = print_result("Vision module import", False, str(e))
    results["failed"] += 1

try:
    from interpreter.core.computer.browser.browser import Browser
    passed = print_result("Browser module import", True)
    results["passed"] += 1
except Exception as e:
    passed = print_result("Browser module import", False, str(e))
    results["failed"] += 1

# ==============================================================================
# TEST 2: Class Structure Verification
# ==============================================================================
print_section("TEST 2: Class Structure Verification")

try:
    expected_methods = ['__init__', 'load', 'query', 'identify_elements']
    missing_methods = []
    
    for method in expected_methods:
        if not hasattr(UiTarsVision, method):
            missing_methods.append(method)
    
    if not missing_methods:
        passed = print_result("UI-TARS class has all expected methods", True)
        results["passed"] += 1
    else:
        passed = print_result("UI-TARS class has all expected methods", False, 
                            f"Missing: {', '.join(missing_methods)}")
        results["failed"] += 1
except Exception as e:
    passed = print_result("UI-TARS class structure check", False, str(e))
    results["failed"] += 1

# ==============================================================================
# TEST 3: Instance Creation
# ==============================================================================
print_section("TEST 3: Instance Creation")

try:
    class MockComputer:
        def __init__(self):
            self.debug = True
    
    computer = MockComputer()
    ui_tars = UiTarsVision(computer)
    
    expected_attrs = ['computer', 'model', 'tokenizer', 'device']
    missing_attrs = []
    
    for attr in expected_attrs:
        if not hasattr(ui_tars, attr):
            missing_attrs.append(attr)
    
    if not missing_attrs:
        passed = print_result("UI-TARS instance creation", True, f"Device: {ui_tars.device}")
        results["passed"] += 1
    else:
        passed = print_result("UI-TARS instance creation", False, 
                            f"Missing attributes: {', '.join(missing_attrs)}")
        results["failed"] += 1
except Exception as e:
    passed = print_result("UI-TARS instance creation", False, str(e))
    results["failed"] += 1

# ==============================================================================
# TEST 4: Vision Module Integration
# ==============================================================================
print_section("TEST 4: Vision Module Integration")

try:
    class MockComputer:
        def __init__(self):
            self.debug = True
    
    computer = MockComputer()
    vision = Vision(computer)
    
    # Check if UI-TARS attribute exists (may be None initially)
    has_ui_tars_attr = hasattr(vision, 'ui_tars')
    passed = print_result("Vision module has ui_tars attribute", has_ui_tars_attr)
    if has_ui_tars_attr:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Check if Vision.query accepts use_ui_tars parameter
    import inspect
    query_params = inspect.signature(vision.query).parameters
    has_use_ui_tars_param = 'use_ui_tars' in query_params
    
    passed = print_result("Vision.query() accepts use_ui_tars parameter", has_use_ui_tars_param)
    if has_use_ui_tars_param:
        results["passed"] += 1
    else:
        results["failed"] += 1
        
except Exception as e:
    print_result("Vision module integration", False, str(e))
    results["failed"] += 2

# ==============================================================================
# TEST 5: Browser Module Integration
# ==============================================================================
print_section("TEST 5: Browser Module Integration")

try:
    class MockVision:
        def __init__(self):
            self.ui_tars = None
    
    class MockComputer:
        def __init__(self):
            self.debug = True
            self.vision = MockVision()
    
    computer = MockComputer()
    browser = Browser(computer)
    
    has_use_ui_tars = hasattr(browser, 'use_ui_tars')
    passed = print_result("Browser module has use_ui_tars attribute", has_use_ui_tars)
    if has_use_ui_tars:
        print(f"  Default value: {browser.use_ui_tars}")
        results["passed"] += 1
    else:
        results["failed"] += 1
        
except Exception as e:
    print_result("Browser module integration", False, str(e))
    results["failed"] += 1

# ==============================================================================
# TEST 6: Dependency Check
# ==============================================================================
print_section("TEST 6: Dependency Check")

dependencies = {
    'torch': 'PyTorch (deep learning framework)',
    'transformers': 'Hugging Face Transformers (model loading)',
    'accelerate': 'Accelerate (model optimization)',
    'bitsandbytes': 'BitsAndBytes (quantization)',
    'PIL': 'Pillow (image processing)',
}

for dep, description in dependencies.items():
    try:
        if dep == 'PIL':
            import PIL
        else:
            import importlib
            module = importlib.import_module(dep)
            if hasattr(module, '__version__'):
                version = module.__version__
                print_result(f"{description} ({dep})", True, f"Version: {version}")
            else:
                print_result(f"{description} ({dep})", True)
        results["passed"] += 1
    except ImportError:
        print_result(f"{description} ({dep})", False, "Not installed")
        print(f"  Note: Install with 'pip install {dep}' or 'pip install \".[ui-tars]\"'")
        results["warnings"] += 1

# ==============================================================================
# TEST 7: PyTorch CUDA Availability
# ==============================================================================
print_section("TEST 7: PyTorch CUDA Availability")

try:
    import torch
    cuda_available = torch.cuda.is_available()
    
    if cuda_available:
        device_name = torch.cuda.get_device_name(0)
        print_result("CUDA support", True, f"Device: {device_name}")
        results["passed"] += 1
    else:
        print_result("CUDA support", False, "CUDA not available - will use CPU")
        print("  Note: Model will run slower on CPU. For GPU support, install CUDA-enabled PyTorch.")
        results["warnings"] += 1
except ImportError:
    print_result("CUDA support check", False, "PyTorch not installed")
    results["warnings"] += 1

# ==============================================================================
# TEST 8: pyproject.toml Configuration
# ==============================================================================
print_section("TEST 8: pyproject.toml Configuration")

try:
    import toml
    
    with open('pyproject.toml', 'r') as f:
        config = toml.load(f)
    
    # Check for ui-tars extras
    extras = config.get('tool', {}).get('poetry', {}).get('extras', {})
    
    if 'ui-tars' in extras:
        ui_tars_deps = extras['ui-tars']
        print_result("pyproject.toml has [ui-tars] extras", True, 
                    f"Dependencies: {', '.join(ui_tars_deps)}")
        results["passed"] += 1
    else:
        print_result("pyproject.toml has [ui-tars] extras", False)
        results["failed"] += 1
        
except Exception as e:
    print_result("pyproject.toml configuration check", False, str(e))
    results["failed"] += 1

# ==============================================================================
# TEST 9: Build Scripts Existence
# ==============================================================================
print_section("TEST 9: Build Scripts Verification")

import os

build_files = {
    'build-portable.bat': 'Windows portable build script',
    'build-portable.sh': 'Linux/macOS portable build script',
    'Dockerfile.ui-tars': 'Docker containerized deployment',
    'docker-compose.yml': 'Docker Compose orchestration'
}

for filename, description in build_files.items():
    exists = os.path.exists(filename)
    passed = print_result(f"{description} ({filename})", exists)
    if exists:
        results["passed"] += 1
    else:
        results["failed"] += 1

# ==============================================================================
# FINAL REPORT
# ==============================================================================
print_section("VERIFICATION SUMMARY")

total_tests = results["passed"] + results["failed"]
success_rate = (results["passed"] / total_tests * 100) if total_tests > 0 else 0

print(f"Tests Passed:  {results['passed']}")
print(f"Tests Failed:  {results['failed']}")
print(f"Warnings:      {results['warnings']}")
print(f"Success Rate:  {success_rate:.1f}%")

print("\n" + "=" * 80)

if results["failed"] == 0:
    print("✓ ALL CRITICAL TESTS PASSED!")
    print("\nUI-TARS integration is properly configured and ready for use.")
    print("\nNext Steps:")
    print("1. Install dependencies: pip install '.[ui-tars,server,local]'")
    print("2. Run test scripts to verify functionality")
    print("3. Start server with UI-TARS support: interpreter --server")
    sys.exit(0)
else:
    print("✗ SOME TESTS FAILED")
    print("\nPlease review the failed tests above and address any issues.")
    print("\nCommon solutions:")
    print("- Install missing dependencies: pip install '.[ui-tars,server,local]'")
    print("- Ensure all integration files are present")
    print("- Check that code modifications are correctly applied")
    sys.exit(1)
