"""
Open Interpreter Integrations Module

Provides integrations with:
- Composio: 250+ app integrations
- Notion: Knowledge management / Second Brain
- OpenClaw: Automation workflows
- Agent Mail + Beads: Multi-agent coordination
"""

from .composio import ComposioIntegration, get_composio, COMPOSIO_PROMPTS
from .notion import NotionIntegration, get_notion, SECOND_BRAIN_PROMPTS
from .openclaw import (
    OpenClawWorkflows,
    get_openclaw,
    SecondBrainWorkflow,
    MorningBriefWorkflow,
    ContentFactoryWorkflow,
    GoalTrackingWorkflow
)
from .agent_mail import (
    AgentMail,
    Beads,
    get_agent_mail,
    get_beads,
    Agent,
    Message,
    FileReservation,
    Issue,
    IssueStatus,
    ReservationStatus
)

__all__ = [
    # Composio
    "ComposioIntegration",
    "get_composio",
    "COMPOSIO_PROMPTS",
    
    # Notion
    "NotionIntegration", 
    "get_notion",
    "SECOND_BRAIN_PROMPTS",
    
    # OpenClaw
    "OpenClawWorkflows",
    "get_openclaw",
    "SecondBrainWorkflow",
    "MorningBriefWorkflow", 
    "ContentFactoryWorkflow",
    "GoalTrackingWorkflow",
    
    # Agent Mail + Beads
    "AgentMail",
    "Beads", 
    "get_agent_mail",
    "get_beads",
    "Agent",
    "Message",
    "FileReservation",
    "Issue",
    "IssueStatus",
    "ReservationStatus",
]

__version__ = "0.1.0"
