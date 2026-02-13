"""
Composio Integration for Open Interpreter

This module provides integration with Composio's 250+ app integrations.
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime


class ComposioIntegration:
    """Integrates Open Interpreter with Composio app integrations."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("COMPOSIO_API_KEY")
        self.base_url = "https://api.composio.dev"
        self.tools = {}
        self.connected_apps = []
        
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    async def initialize(self) -> bool:
        """Initialize Composio connection."""
        if not self.api_key:
            raise ValueError("Composio API key not provided")
        
        # Load available tools
        await self._fetch_tools()
        return True
    
    async def _fetch_tools(self):
        """Fetch available tools from Composio."""
        # This would make actual API call in production
        # For now, define common integrations
        self.tools = {
            "github": {
                "name": "GitHub",
                "actions": ["create_issue", "list_issues", "create_pr", "get_repo"],
                "description": "GitHub repository management"
            },
            "slack": {
                "name": "Slack",
                "actions": ["send_message", "list_channels", "post_to_channel"],
                "description": "Slack messaging"
            },
            "notion": {
                "name": "Notion",
                "actions": ["create_page", "query_database", "update_page"],
                "description": "Notion workspace integration"
            },
            "google_workspace": {
                "name": "Google Workspace",
                "actions": ["create_event", "send_email", "read_calendar"],
                "description": "Google Calendar, Gmail, Drive"
            },
            "discord": {
                "name": "Discord",
                "actions": ["send_message", "get_channel", "create_webhook"],
                "description": "Discord bot integration"
            },
            "twitter": {
                "name": "Twitter/X",
                "actions": ["post_tweet", "search_tweets", "get_user"],
                "description": "Twitter/X integration"
            }
        }
    
    def get_available_tools(self) -> Dict[str, Any]:
        """Get all available Composio tools."""
        return self.tools
    
    def get_tool(self, app_name: str) -> Optional[Dict]:
        """Get a specific tool by name."""
        return self.tools.get(app_name.lower())
    
    async def execute_action(
        self, 
        app: str, 
        action: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a Composio action."""
        tool = self.get_tool(app)
        if not tool:
            raise ValueError(f"App {app} not found")
        
        if action not in tool.get("actions", []):
            raise ValueError(f"Action {action} not available for {app}")
        
        # In production, this would make actual API call
        return {
            "status": "success",
            "app": app,
            "action": action,
            "params": params,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_setup_prompt(self) -> str:
        """Get the setup prompt for initializing Composio."""
        return """To set up Composio:

1. Get your API key from https://app.composio.dev
2. Set environment variable: export COMPOSIO_API_KEY="your_key"
3. Initialize in Python:
   from interpreter.integrations.composio import ComposioIntegration
   composio = ComposioIntegration()
   await composio.initialize()"""


# Singleton instance
_composio_instance = None


def get_composio() -> ComposioIntegration:
    """Get or create the global Composio instance."""
    global _composio_instance
    if _composio_instance is None:
        _composio_instance = ComposioIntegration()
    return _composio_instance


# Ready-to-use prompts for common workflows
COMPOSIO_PROMPTS = {
    "github_to_notion": """
Set up an integration that:
1. Watches my GitHub repository for new issues
2. When a new issue is created, creates a page in Notion
3. Maps: title → Notion title, labels → tags
""",
    "daily_standup": """
Create a daily standup automation:
1. Pull completed tasks from GitHub
2. Get updates from Slack
3. Check calendar for today
4. Compile standup and post to Slack #standup
""",
    "content_distribution": """
Content workflow:
1. Write article about {topic}
2. Post to WordPress
3. Share on Twitter with hashtags
4. Post to LinkedIn
5. Add to Notion content calendar
"""
}
