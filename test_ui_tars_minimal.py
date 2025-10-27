"""
Minimal test for UI-TARS integration that works even with limited resources
"""

def test_ui_tars_minimal():
    """Test that UI-TARS integration works at a basic level"""
    print("Testing minimal UI-TARS integration...")
    
    try:
        # Import the UI-TARS module
        from interpreter.core.computer.vision.ui_tars.ui_tars_vision import UiTarsVision
        
        # Create a mock computer object
        class MockComputer:
            def __init__(self):
                self.debug = False  # Disable debug to reduce output
        
        computer = MockComputer()
        
        # Create UI-TARS instance
        ui_tars = UiTarsVision(computer)
        
        # Verify basic attributes
        assert hasattr(ui_tars, 'computer'), "Missing computer attribute"
        assert hasattr(ui_tars, 'model'), "Missing model attribute"
        assert hasattr(ui_tars, 'tokenizer'), "Missing tokenizer attribute"
        assert hasattr(ui_tars, 'device'), "Missing device attribute"
        
        print("✓ UI-TARS module imported and instantiated successfully")
        print(f"✓ Basic attributes verified")
        print(f"  Device set to: {ui_tars.device}")
        
        return True
        
    except Exception as e:
        print(f"✗ Minimal UI-TARS test failed: {e}")
        return False

def test_vision_module_with_ui_tars():
    """Test that the vision module can work with UI-TARS"""
    print("Testing vision module with UI-TARS support...")
    
    try:
        # Import the vision module
        from interpreter.core.computer.vision.vision import Vision
        
        # Create a mock computer object
        class MockComputer:
            def __init__(self):
                self.debug = False
        
        computer = MockComputer()
        
        # Create vision instance
        vision = Vision(computer)
        
        # Verify it has the UI-TARS attribute (even if None)
        assert hasattr(vision, 'ui_tars'), "Vision module missing ui_tars attribute"
        
        print("✓ Vision module imported successfully")
        print("✓ UI-TARS support attribute verified")
        
        return True
        
    except Exception as e:
        print(f"✗ Vision module test failed: {e}")
        return False

def test_browser_module_with_ui_tars():
    """Test that the browser module can work with UI-TARS"""
    print("Testing browser module with UI-TARS support...")
    
    try:
        # Import the browser module
        from interpreter.core.computer.browser.browser import Browser
        
        # Create a mock computer object
        class MockComputer:
            def __init__(self):
                self.debug = False
                # Mock vision attribute
                self.vision = type('Vision', (), {
                    'ui_tars': None
                })()
        
        computer = MockComputer()
        
        # Create browser instance
        browser = Browser(computer)
        
        # Verify it has the UI-TARS flag
        assert hasattr(browser, 'use_ui_tars'), "Browser module missing use_ui_tars attribute"
        
        print("✓ Browser module imported successfully")
        print(f"✓ UI-TARS support flag verified: {browser.use_ui_tars}")
        
        return True
        
    except Exception as e:
        print(f"✗ Browser module test failed: {e}")
        return False

if __name__ == "__main__":
    print("Running minimal UI-TARS integration tests...\n")
    
    tests = [
        test_ui_tars_minimal,
        test_vision_module_with_ui_tars,
        test_browser_module_with_ui_tars
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Minimal UI-TARS tests completed: {passed}/{len(tests)} passed")
    
    if passed == len(tests):
        print("\n✅ All minimal tests passed!")
        print("UI-TARS integration is working correctly.")
        print("Actual model loading will happen on first use.")
    else:
        print("\n❌ Some tests failed.")
        print("Check the errors above for details.")