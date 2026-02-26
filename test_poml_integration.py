"""
Test script to verify POML integration with Open Interpreter.
"""

def test_poml_integration():
    """Test that POML is properly integrated with Open Interpreter."""
    
    try:
        # Import the interpreter
        from interpreter import interpreter
        
        # Check if POML is available
        if interpreter.computer.poml.is_available():
            print("✓ POML is available and integrated successfully")
            
            # Test creating a simple template
            template_content = """
<task>
    <objective>{{objective}}</objective>
    <context>
        <data>{{data}}</data>
    </context>
</task>
            """
            
            template = interpreter.computer.poml.create_template(
                "test_template", 
                template_content.strip()
            )
            
            if template:
                print("✓ POML template creation successful")
                
                # Test rendering the template
                rendered = interpreter.computer.poml.render_template(template, {
                    "objective": "Test the POML integration",
                    "data": "Sample test data"
                })
                
                if rendered:
                    print("✓ POML template rendering successful")
                    print(f"Rendered template:\n{rendered}")
                    
                    # Test agent prompt creation
                    agent_prompt = interpreter.computer.poml.create_agent_prompt(
                        agent_type="test_agent",
                        objective="Verify POML integration",
                        context={"test": "integration"},
                        instructions=["Step 1: Check POML availability", "Step 2: Create template", "Step 3: Render template"]
                    )
                    
                    if agent_prompt:
                        print("✓ Agent prompt creation successful")
                        print(f"Agent prompt:\n{agent_prompt}")
                        return True
                    else:
                        print("✗ Agent prompt creation failed")
                        return False
                else:
                    print("✗ POML template rendering failed")
                    return False
            else:
                print("✗ POML template creation failed")
                return False
        else:
            print("⚠ POML is not available. Please install it with: pip install poml")
            return False
            
    except Exception as e:
        print(f"✗ Error testing POML integration: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing POML integration with Open Interpreter...")
    success = test_poml_integration()
    if success:
        print("\n✓ All POML integration tests passed!")
    else:
        print("\n✗ POML integration tests failed!")