"""
POML (Prompt Orchestration Markup Language) module for Open Interpreter.
This module provides integration with Microsoft's POML for structured prompting.
"""

try:
    import poml
    POML_AVAILABLE = True
except ImportError:
    POML_AVAILABLE = False
    poml = None

class POML:
    def __init__(self, computer):
        self.computer = computer
        self.interpreter = computer.interpreter
        
        # Initialize POML components if available
        if POML_AVAILABLE:
            self.engine = poml
        else:
            self.engine = None
    
    def is_available(self):
        """Check if POML is available for use."""
        return POML_AVAILABLE
    
    def create_template(self, name, content, **kwargs):
        """
        Create a POML template for structured prompting.
        
        Args:
            name (str): Name of the template
            content (str): POML template content
            **kwargs: Additional template parameters
            
        Returns:
            Template object if POML is available, None otherwise
        """
        if not self.is_available():
            self._warn_unavailable()
            return None
            
        try:
            template = self.engine.PromptTemplate(name=name, content=content, **kwargs)
            return template
        except Exception as e:
            self.interpreter.computer.terminal.error(f"Error creating POML template: {str(e)}")
            return None
    
    def render_template(self, template, data=None):
        """
        Render a POML template with provided data.
        
        Args:
            template: POML template object
            data (dict): Data to render the template with
            
        Returns:
            Rendered prompt string
        """
        if not self.is_available() or template is None:
            if not self.is_available():
                self._warn_unavailable()
            return ""
            
        try:
            if data is None:
                data = {}
            return template.render(data)
        except Exception as e:
            self.interpreter.computer.terminal.error(f"Error rendering POML template: {str(e)}")
            return ""
    
    def create_agent_prompt(self, agent_type, objective, context=None, instructions=None):
        """
        Create a standardized agent prompt using POML structure.
        
        Args:
            agent_type (str): Type of agent (e.g., 'data_analyst', 'web_researcher')
            objective (str): Main objective for the agent
            context (dict): Context information for the agent
            instructions (list): List of step-by-step instructions
            
        Returns:
            Rendered prompt string
        """
        if not self.is_available():
            self._warn_unavailable()
            return ""
        
        # Create a POML template for agent prompts
        template_content = """
<task>
    <agent_type>{{agent_type}}</agent_type>
    <objective>{{objective}}</objective>
    {{#if context}}
    <context>
        {{#each context}}
        <{{@key}}>{{this}}</{{@key}}>
        {{/each}}
    </context>
    {{/if}}
    {{#if instructions}}
    <instructions>
        {{#each instructions}}
        <step>{{this}}</step>
        {{/each}}
    </instructions>
    {{/if}}
    <output_format>Provide your response in a structured format appropriate for the task.</output_format>
</task>
        """
        
        template = self.create_template(f"{agent_type}_agent", template_content.strip())
        if template is None:
            return ""
        
        # Prepare data for rendering
        data = {
            "agent_type": agent_type,
            "objective": objective,
            "context": context or {},
            "instructions": instructions or []
        }
        
        return self.render_template(template, data)
    
    def _warn_unavailable(self):
        """Warn the user that POML is not available."""
        self.interpreter.computer.terminal.warn(
            "POML is not available. Please install it with: pip install poml"
        )