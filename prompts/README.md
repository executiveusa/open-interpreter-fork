# Open Interpreter Prompts & Workflows

A comprehensive collection of prompts and workflows to enhance Open Interpreter with powerful integrations and automation capabilities.

## Table of Contents

### Integration Prompts

| Directory | Description |
|-----------|-------------|
| [`composio/`](composio/) | Composio 250+ app integrations |
| [`notion/`](notion/) | Notion knowledge management |
| [`openclaw/`](openclaw/) | OpenClaw-style automation workflows |
| [`agent-mail-beads/`](agent-mail-beads/) | Multi-agent coordination system |

## Quick Start

### Composio Integration

Connect Open Interpreter with 250+ apps:

```bash
pip install composio-core
```

Then use the setup prompt:
```
I want to set up Composio integration. Please:
1. Initialize the Composio client with my API key
2. Show me available tools for GitHub integration
3. Create a workflow that syncs GitHub issues to Notion
```

### Notion Integration

Build a second brain in Notion:

1. Create a Notion integration at [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Connect it to your workspace
3. Use the setup prompt to connect

### OpenClaw Workflows

Set up powerful automation:

- **Second Brain**: Remember everything via text
- **Morning Brief**: Daily automated reports
- **Content Factory**: Multi-agent content creation
- **Research**: Automated market research
- **Goal Tracking**: AI-powered task management

### Multi-Agent Coordination

Run multiple Open Interpreter instances coordinated:

- Agent Mail: Communication between agents
- Beads: Task tracking with Git-backed issues
- Git Worktrees: Parallel agent workspaces

## Directory Structure

```
prompts/
├── composio/
│   ├── setup.md         # Composio setup guide
│   └── cookbook.md       # Advanced recipes
├── notion/
│   ├── setup.md          # Notion API setup
│   └── second-brain.md  # Second brain system
├── openclaw/
│   ├── second-brain.md  # Memory system
│   ├── morning-brief.md # Daily reports
│   └── content-factory.md # Content automation
└── agent-mail-beads/
    ├── setup.md         # AM+B setup
    └── multi-agent.md    # Coordination workflows
```

## Feature Comparison

| Feature | Complexity | Setup Time | Use Case |
|---------|------------|------------|----------|
| Composio | Medium | 15 min | App automation |
| Notion | Low | 10 min | Knowledge management |
| OpenClaw Workflows | High | 30 min | Personal AI assistant |
| Agent Mail + Beads | High | 1 hour | Multi-agent development |

## Environment Variables

### Composio
```bash
export COMPOSIO_API_KEY="your_api_key"
```

### Notion
```bash
export NOTION_API_KEY="secret_xxxxx"
export NOTION_DATABASE_ID="your_db_id"
```

### Agent Mail
```bash
export AGENT_MAIL_PATH="./mail"
export FILE_RESERVATIONS_ENFORCEMENT_ENABLED=true
```

### Beads
```bash
export BEADS_PATH=".beads"
```

## Recommended Workflows

### 1. Personal AI Assistant
1. Set up Notion second brain
2. Configure morning brief
3. Add goal tracking

### 2. Content Creator
1. Set up content factory
2. Configure research automation
3. Connect social media accounts via Composio

### 3. Development Team
1. Set up Agent Mail + Beads
2. Configure Git worktrees
3. Enable file reservation enforcement

## Cost Estimates

| Integration | Monthly Cost |
|-------------|---------------|
| Composio | $20-50/month |
| Notion | $10/month |
| OpenClaw (Opus) | $200/month |
| OpenClaw (MiniMax) | $10/month |
| Agent Mail + Beads | Free (self-hosted) |

## Documentation

- [Composio Docs](https://docs.composio.dev)
- [Notion API Docs](https://developers.notion.io)
- [Open Interpreter Docs](https://docs.openinterpreter.com)
- [Agent Mail Docs](https://agentmail.docs)
- [Beads Docs](https://beads.docs)

## Contributing

Add new prompts by creating files in the appropriate directory. Follow the existing format and include:

1. Overview section
2. Setup instructions
3. Usage examples
4. Prompt templates
5. Best practices

## License

Same as Open Interpreter - AGPL
