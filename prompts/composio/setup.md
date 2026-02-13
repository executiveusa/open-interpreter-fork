# Composio Setup Guide

## Overview
Composio provides 250+ app integrations for AI agents. This guide helps you connect Open Interpreter with Composio to access powerful automation capabilities.

## Installation

```bash
pip install composio-core
```

## Setup Steps

### 1. Get Your API Key
1. Visit [Composio Dashboard](https://app.composio.dev)
2. Create an account or sign in
3. Navigate to Settings → API Keys
4. Copy your API key

### 2. Initialize Composio in Open Interpreter

```python
from interpreter import interpreter
from composio import Composio

# Set up Composio
composio = Composio(api_key="YOUR_API_KEY")

# Configure interpreter to use Composio tools
interpreter.composio = composio
```

### 3. Available Integrations

| Category | Apps |
|----------|------|
| Development | GitHub, GitLab, Slack, Discord |
| Productivity | Notion, Google Workspace, Microsoft 365 |
| Communication | Telegram, WhatsApp, Discord |
| Data | Airtable, PostgreSQL, MongoDB |
| Media | YouTube, Twitter, LinkedIn |

## Quick Start Prompt

```
I want to set up Composio integration. Please:
1. Initialize the Composio client with my API key
2. Show me available tools for GitHub integration
3. Create a workflow that syncs GitHub issues to Notion
```

## Usage Examples

### GitHub Integration
```
Connect to my GitHub account and create a new issue in repository [owner/repo] with title "[issue]" and body "[description]"
```

### Slack Integration
```
Send a message to channel #general in Slack with content "Build completed successfully"
```

### Notion Integration
```
Create a new page in my Notion workspace under database [database_id] with properties {title: "Task Name", status: "In Progress"}
```

## Environment Variables

```bash
export COMPOSIO_API_KEY="your_api_key_here"
```

## Next Steps

- See [Composio Cookbook](./cookbook.md) for advanced recipes
- Check [Tool Reference](./tools.md) for all available actions
