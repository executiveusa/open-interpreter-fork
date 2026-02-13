"""
Notion Integration for Open Interpreter

This module provides Notion workspace integration for 
knowledge management and second brain functionality.
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Memory:
    """Represents a memory entry."""
    id: str
    content: str
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    source: str = "chat"
    importance: str = "medium"


@dataclass
class Conversation:
    """Represents a conversation summary."""
    id: str
    title: str
    summary: str
    key_points: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    action_items: List[str] = field(default_factory=list)


class NotionIntegration:
    """Integrates Open Interpreter with Notion workspace."""
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        database_id: Optional[str] = None
    ):
        self.api_key = api_key or os.environ.get("NOTION_API_KEY")
        self.database_id = database_id or os.environ.get("NOTION_DATABASE_ID")
        self.client = None
        self.memories: List[Memory] = []
        self.conversations: List[Conversation] = []
        
    async def initialize(self) -> bool:
        """Initialize Notion connection."""
        if not self.api_key:
            raise ValueError("Notion API key not provided")
        
        # In production, this would initialize the Notion client
        # from notion_client import Client
        # self.client = Client(auth=self.api_key)
        
        return True
    
    async def create_page(
        self, 
        title: str, 
        content: str = "",
        properties: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Create a new page in Notion."""
        if not self.client:
            # Simulate for demo
            return {
                "id": f"page_{datetime.utcnow().timestamp()}",
                "title": title,
                "created": True
            }
        
        # Real implementation would call Notion API
        return await self._create_notion_page(title, content, properties)
    
    async def _create_notion_page(
        self, 
        title: str, 
        content: str,
        properties: Optional[Dict]
    ) -> Dict[str, Any]:
        """Create actual Notion page."""
        # This would be the real API call
        return {
            "id": "demo_page_id",
            "object": "page",
            "created_time": datetime.utcnow().isoformat()
        }
    
    async def query_database(
        self, 
        filter_props: Optional[Dict] = None
    ) -> List[Dict]:
        """Query a Notion database."""
        if not self.client:
            return []
        
        # Real implementation
        return []
    
    async def add_memory(
        self, 
        content: str, 
        tags: Optional[List[str]] = None,
        importance: str = "medium"
    ) -> Memory:
        """Add a memory to the second brain."""
        memory = Memory(
            id=f"mem_{len(self.memories)}_{datetime.utcnow().timestamp()}",
            content=content,
            tags=tags or [],
            importance=importance,
            source="chat"
        )
        self.memories.append(memory)
        
        # Optionally sync to Notion
        if self.client and self.database_id:
            await self._sync_memory_to_notion(memory)
        
        return memory
    
    async def _sync_memory_to_notion(self, memory: Memory):
        """Sync memory to Notion database."""
        # Create page in Notion with memory content
        await self.create_page(
            title=f"Memory: {memory.content[:50]}...",
            content=memory.content,
            properties={
                "Tags": {"multi_select": [{"name": t} for t in memory.tags]},
                "Importance": {"select": {"name": memory.importance}},
                "Type": {"select": {"name": "Memory"}}
            }
        )
    
    async def search_memories(self, query: str) -> List[Memory]:
        """Search memories by query."""
        results = []
        query_lower = query.lower()
        
        for memory in self.memories:
            if query_lower in memory.content.lower():
                results.append(memory)
            elif any(query_lower in tag.lower() for tag in memory.tags):
                results.append(memory)
        
        return results
    
    async def get_memories(
        self, 
        days: Optional[int] = None,
        tags: Optional[List[str]] = None
    ) -> List[Memory]:
        """Get memories with optional filters."""
        results = self.memories
        
        if days:
            from datetime import timedelta
            cutoff = datetime.utcnow() - timedelta(days=days)
            results = [m for m in results if m.created_at >= cutoff]
        
        if tags:
            results = [m for m in results if any(t in m.tags for t in tags)]
        
        return results
    
    async def save_conversation(
        self, 
        title: str, 
        summary: str,
        key_points: Optional[List[str]] = None,
        action_items: Optional[List[str]] = None
    ) -> Conversation:
        """Save a conversation summary."""
        conversation = Conversation(
            id=f"conv_{len(self.conversations)}_{datetime.utcnow().timestamp()}",
            title=title,
            summary=summary,
            key_points=key_points or [],
            action_items=action_items or []
        )
        self.conversations.append(conversation)
        return conversation
    
    def get_setup_prompt(self) -> str:
        """Get the setup prompt for initializing Notion."""
        return """To set up Notion:

1. Go to https://www.notion.so/my-integrations
2. Create a new integration
3. Copy the Internal Integration Secret
4. Set environment variable: export NOTION_API_KEY="your_key"
5. Share your database with the integration
6. Set: export NOTION_DATABASE_ID="your_database_id"

Initialize in Python:
from interpreter.integrations.notion import NotionIntegration
notion = NotionIntegration()
await notion.initialize()"""


# Second Brain Prompt Templates
SECOND_BRAIN_PROMPTS = {
    "setup": """Build a second brain system where:
- I can save memories via text message
- I can search and retrieve memories
- Memories are organized by tags
- There's a nice UI to browse everything
- Everything syncs across my devices""",
    
    "research": """Create a research second brain:
- Save links and articles
- Add notes and annotations
- Create study guides from saved content
- Track learning progress
- Connect related concepts""",
    
    "project": """Create a project knowledge base:
- Store meeting notes
- Track decisions made
- Link to relevant documents
- Tag by project and category
- Generate status reports"""
}


# Singleton instance
_notion_instance = None


def get_notion() -> NotionIntegration:
    """Get or create the global Notion instance."""
    global _notion_instance
    if _notion_instance is None:
        _notion_instance = NotionIntegration()
    return _notion_instance
