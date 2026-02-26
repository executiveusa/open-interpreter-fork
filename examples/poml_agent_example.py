"""
Example script demonstrating POML integration with Open Interpreter agents.
"""

from interpreter import interpreter

def main():
    print("Open Interpreter POML Agent Example")
    print("=" * 40)
    
    # Check if POML is available
    if not interpreter.computer.poml.is_available():
        print("Error: POML is not available. Please install it with: pip install poml")
        return
    
    print("✓ POML is available and integrated")
    
    # Example 1: Create a data analysis agent prompt
    print("\n1. Creating a Data Analysis Agent Prompt")
    data_analysis_prompt = interpreter.computer.poml.create_agent_prompt(
        agent_type="data_analyst",
        objective="Analyze the provided sales data and identify key trends",
        context={
            "dataset": "Q1_Sales_2024.csv",
            "columns": "date, product, revenue, region, customer_segment",
            "time_period": "January - March 2024"
        },
        instructions=[
            "Load and validate the sales data",
            "Calculate total revenue by region",
            "Identify top performing products",
            "Detect seasonal trends in sales",
            "Generate a summary report with insights"
        ]
    )
    
    print("Generated prompt:")
    print(data_analysis_prompt)
    
    # Example 2: Create a web research agent prompt
    print("\n2. Creating a Web Research Agent Prompt")
    research_prompt = interpreter.computer.poml.create_agent_prompt(
        agent_type="web_researcher",
        objective="Research the latest developments in AI-powered coding assistants",
        context={
            "sources": "tech news websites, research papers, GitHub repositories",
            "focus_areas": "new features, performance improvements, adoption rates",
            "timeframe": "last 6 months"
        },
        instructions=[
            "Search for recent articles about AI coding assistants",
            "Identify key features released in the last 6 months",
            "Compare performance benchmarks if available",
            "Summarize adoption trends in the developer community",
            "Provide a comprehensive analysis report"
        ]
    )
    
    print("Generated prompt:")
    print(research_prompt)
    
    # Example 3: Custom template creation
    print("\n3. Creating a Custom POML Template")
    
    custom_template_content = """
<code_review>
    <task>{{task_description}}</task>
    <code_language>{{language}}</code_language>
    <review_criteria>
        {{#each criteria}}
        <criterion>{{this}}</criterion>
        {{/each}}
    </review_criteria>
    <output_format>
        Provide feedback in the following format:
        1. Overall assessment
        2. Specific issues found
        3. Suggestions for improvement
        4. Code quality rating (1-10)
    </output_format>
</code_review>
    """
    
    custom_template = interpreter.computer.poml.create_template(
        "code_review_agent",
        custom_template_content.strip()
    )
    
    if custom_template:
        print("✓ Custom template created successfully")
        
        # Render the custom template
        rendered_template = interpreter.computer.poml.render_template(custom_template, {
            "task_description": "Review Python script for web scraping functionality",
            "language": "Python",
            "criteria": [
                "Code readability and structure",
                "Error handling implementation",
                "Performance optimization",
                "Security considerations",
                "Documentation quality"
            ]
        })
        
        print("Rendered custom template:")
        print(rendered_template)
    else:
        print("✗ Failed to create custom template")

if __name__ == "__main__":
    main()"""
Example script demonstrating POML integration with Open Interpreter agents.
"""

from interpreter import interpreter

def main():
    print("Open Interpreter POML Agent Example")
    print("=" * 40)
    
    # Check if POML is available
    if not interpreter.computer.poml.is_available():
        print("Error: POML is not available. Please install it with: pip install poml")
        return
    
    print("✓ POML is available and integrated")
    
    # Example 1: Create a data analysis agent prompt
    print("\n1. Creating a Data Analysis Agent Prompt")
    data_analysis_prompt = interpreter.computer.poml.create_agent_prompt(
        agent_type="data_analyst",
        objective="Analyze the provided sales data and identify key trends",
        context={
            "dataset": "Q1_Sales_2024.csv",
            "columns": "date, product, revenue, region, customer_segment",
            "time_period": "January - March 2024"
        },
        instructions=[
            "Load and validate the sales data",
            "Calculate total revenue by region",
            "Identify top performing products",
            "Detect seasonal trends in sales",
            "Generate a summary report with insights"
        ]
    )
    
    print("Generated prompt:")
    print(data_analysis_prompt)
    
    # Example 2: Create a web research agent prompt
    print("\n2. Creating a Web Research Agent Prompt")
    research_prompt = interpreter.computer.poml.create_agent_prompt(
        agent_type="web_researcher",
        objective="Research the latest developments in AI-powered coding assistants",
        context={
            "sources": "tech news websites, research papers, GitHub repositories",
            "focus_areas": "new features, performance improvements, adoption rates",
            "timeframe": "last 6 months"
        },
        instructions=[
            "Search for recent articles about AI coding assistants",
            "Identify key features released in the last 6 months",
            "Compare performance benchmarks if available",
            "Summarize adoption trends in the developer community",
            "Provide a comprehensive analysis report"
        ]
    )
    
    print("Generated prompt:")
    print(research_prompt)
    
    # Example 3: Custom template creation
    print("\n3. Creating a Custom POML Template")
    
    custom_template_content = """
<code_review>
    <task>{{task_description}}</task>
    <code_language>{{language}}</code_language>
    <review_criteria>
        {{#each criteria}}
        <criterion>{{this}}</criterion>
        {{/each}}
    </review_criteria>
    <output_format>
        Provide feedback in the following format:
        1. Overall assessment
        2. Specific issues found
        3. Suggestions for improvement
        4. Code quality rating (1-10)
    </output_format>
</code_review>
    """
    
    custom_template = interpreter.computer.poml.create_template(
        "code_review_agent",
        custom_template_content.strip()
    )
    
    if custom_template:
        print("✓ Custom template created successfully")
        
        # Render the custom template
        rendered_template = interpreter.computer.poml.render_template(custom_template, {
            "task_description": "Review Python script for web scraping functionality",
            "language": "Python",
            "criteria": [
                "Code readability and structure",
                "Error handling implementation",
                "Performance optimization",
                "Security considerations",
                "Documentation quality"
            ]
        })
        
        print("Rendered custom template:")
        print(rendered_template)
    else:
        print("✗ Failed to create custom template")

if __name__ == "__main__":
    main()