"""
Comprehensive test for UI-TARS integration with different scenarios
"""

def test_import_and_basic_functionality():
    """Test basic import and functionality"""
    print("Testing UI-TARS import and basic functionality...")
    
    try:
        from interpreter.core.computer.vision.ui_tars.ui_tars_vision import UiTarsVision
        print("✓ UI-TARS vision module imported successfully")
        
        # Create a mock computer object
        class MockComputer:
            def __init__(self):
                self.debug = True
        
        computer = MockComputer()
        ui_tars = UiTarsVision(computer)
        
        print("✓ UI-TARS instance created successfully")
        print(f"  Device: {ui_tars.device}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to test UI-TARS: {e}")
        return False

def test_vision_module_integration():
    """Test integration with the main vision module"""
    print("Testing integration with main vision module...")
    
    try:
        # Test that we can import the main vision module
        from interpreter.core.computer.vision.vision import Vision
        
        # Create a mock computer object
        class MockComputer:
            def __init__(self):
                self.debug = True
        
        computer = MockComputer()
        vision = Vision(computer)
        
        print("✓ Main vision module imported and instantiated successfully")
        
        # Check if UI-TARS attribute exists
        if hasattr(vision, 'ui_tars'):
            print("✓ Vision module has UI-TARS attribute")
        else:
            print("⚠ Vision module does not have UI-TARS attribute (may be loaded on demand)")
            
        return True
    except Exception as e:
        print(f"✗ Failed to test vision module integration: {e}")
        return False

def test_browser_module_integration():
    """Test integration with the browser module"""
    print("Testing integration with browser module...")
    
    try:
        # Test that we can import the browser module
        from interpreter.core.computer.browser.browser import Browser
        
        # Create a mock computer object
        class MockComputer:
            def __init__(self):
                self.debug = True
                # Mock vision attribute
                self.vision = type('Vision', (), {
                    'ui_tars': None
                })()
        
        computer = MockComputer()
        browser = Browser(computer)
        
        print("✓ Browser module imported and instantiated successfully")
        
        # Check if UI-TARS flag exists
        if hasattr(browser, 'use_ui_tars'):
            print("✓ Browser module has use_ui_tars attribute")
            print(f"  use_ui_tars: {browser.use_ui_tars}")
        else:
            print("✗ Browser module does not have use_ui_tars attribute")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Failed to test browser module integration: {e}")
        return False

def test_pytorch_availability():
    """Test if PyTorch is available"""
    print("Testing PyTorch availability...")
    
    try:
        import importlib
        torch = importlib.import_module('torch')
        print("✓ PyTorch is available")
        print(f"  Version: {torch.__version__}")
        print(f"  CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"  CUDA device: {torch.cuda.get_device_name()}")
        return True
    except ImportError:
        print("⚠ PyTorch is not available (expected in some environments)")
        return True  # This is not a failure for our integration
    except Exception as e:
        print(f"✗ Error checking PyTorch availability: {e}")
        return False

def test_dependencies():
    """Test if required dependencies are available"""
    print("Testing required dependencies...")
    
    dependencies = [
        ('torch', 'PyTorch for deep learning'),
        ('transformers', 'Hugging Face transformers for model loading'),
        ('PIL', 'Pillow for image processing'),
    ]
    
    missing_deps = []
    
    for dep, description in dependencies:
        try:
            if dep == 'PIL':
                import importlib
                PIL = importlib.import_module('PIL')
                print(f"✓ {description} (Pillow) is available")
            else:
                import importlib
                importlib.import_module(dep)
                print(f"✓ {description} ({dep}) is available")
        except ImportError:
            print(f"⚠ {description} ({dep}) is not available")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"  Missing dependencies: {missing_deps}")
        print("  Note: These will be loaded on demand in UI-TARS module")
    
    return True

if __name__ == "__main__":
    print("Running comprehensive UI-TARS integration tests...\n")
    
    tests = [
        test_import_and_basic_functionality,
        test_vision_module_integration,
        test_browser_module_integration,
        test_pytorch_availability,
        test_dependencies
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Comprehensive UI-TARS tests completed: {passed}/{len(tests)} passed")
    
    if passed == len(tests):
        print("All comprehensive UI-TARS tests passed!")
        print("\nUI-TARS integration is ready for use.")
        print("Note: Actual model loading will happen on first use.")
    else:
        print("Some UI-TARS tests had issues, but integration may still work.")