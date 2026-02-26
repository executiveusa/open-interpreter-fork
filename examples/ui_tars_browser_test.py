"""
Test script for UI-TARS integration with Open Interpreter browser control
"""

def test_ui_tars_import():
    """Test that we can import the UI-TARS vision module"""
    print("Testing UI-TARS import...")
    
    try:
        from interpreter.core.computer.vision.ui_tars.ui_tars_vision import UiTarsVision
        print("✓ UI-TARS vision module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to import UI-TARS vision module: {e}")
        return False

def test_ui_tars_initialization():
    """Test that we can initialize the UI-TARS vision module"""
    print("Testing UI-TARS initialization...")
    
    try:
        from interpreter.core.computer.vision.ui_tars.ui_tars_vision import UiTarsVision
        
        # Create a mock computer object
        class MockComputer:
            def __init__(self):
                self.debug = True
        
        computer = MockComputer()
        ui_tars = UiTarsVision(computer)
        print("✓ UI-TARS vision module initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize UI-TARS vision module: {e}")
        return False

if __name__ == "__main__":
    print("Running UI-TARS integration tests...\n")
    
    tests = [
        test_ui_tars_import,
        test_ui_tars_initialization
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Tests completed: {passed}/{len(tests)} passed")
    
    if passed == len(tests):
        print("All tests passed! UI-TARS integration is ready.")
    else:
        print("Some tests failed. Please check the implementation.")