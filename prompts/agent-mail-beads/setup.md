# Agent Mail + Beads Multi-Agent Coordination

## Overview
Combine Agent Mail for communication and Beads for task tracking to create a powerful multi-agent development system.

## What is Agent Mail?

Agent Mail is "Gmail for your coding agents":
- **Identity Management**: Agents get memorable names (e.g., GreenCastle)
- **Async Messaging**: Inbox/outbox system for agent communication
- **File Reservations**: Lease files before editing to prevent conflicts
- **Conflict Avoidance**: Prevents multiple agents from editing same files

## What is Beads?

Beads is a "memory upgrade for your coding agent":
- **Git-backed Issues**: Issues stored as JSONL in `.beads/` directory
- **Hash-based IDs**: Conflict-free IDs (e.g., `bd-a1b2`)
- **Issue Graph**: Parent/child relationships, blocking dependencies
- **Compaction**: Semantic summarization of old tasks

## Architecture

```
┌─────────────────────────────────────────────┐
│           Main Repository                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │  .beads │  │  mail/  │  │ .git    │     │
│  │ (Issues)│  │(Messages│  │(History)│     │
│  └─────────┘  └─────────┘  └─────────┘     │
└─────────────────────────────────────────────┘
         ▲               ▲
         │               │
    ┌────┴────┐    ┌────┴────┐
    ▼         ▼    ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐
│Worktree│ │Worktree│ │Worktree│
│Agent A │ │Agent B │ │Agent C │
└────────┘ └────────┘ └────────┘
```

## Setup Prompt

```
Set up Agent Mail + Beads for multi-agent development:
1. Initialize Agent Mail with project key "my-project"
2. Set up Beads issue tracking in .beads directory
3. Configure file reservation system
4. Create initial agent identities
5. Set up MCP tools for agent communication
```

## Core Features

### 1. Agent Identity

```python
# Register an agent
register_agent(
    project_key="my-project",
    program="claude",
    model="opus-4",
    name="GreenCastle",
    capabilities=["frontend", "react", "typescript"]
)
```

### 2. File Reservations

```python
# Reserve files before editing
file_reservation_paths(
    project_key="my-project",
    agent_name="GreenCastle",
    paths=["src/components/*.tsx"],
    exclusive=True,
    ttl_seconds=3600  # 1 hour lease
)
```

### 3. Messaging

```python
# Send message to another agent
send_message(
    project_key="my-project",
    sender="GreenCastle",
    to="BlueBuilder",
    subject="Component API Changes",
    body="I updated the Button component API..."
)

# Check inbox
messages = fetch_inbox(
    project_key="my-project",
    agent_name="GreenCastle"
)
```

### 4. Issue Tracking

```bash
# Create issue
bd issue create --title "Add user authentication" --priority high

# List ready issues
bd issue list --status ready

# Update issue
bd issue update bd-abc123 --status in-progress

# Show dependencies
bd issue deps bd-abc123
```

## Git Worktree Setup

### Create Agent Worktree

```bash
# 1. Create branch for agent
git branch agent-frontend main

# 2. Create worktree
git worktree add ./worktrees/agent-frontend agent-frontend

# 3. Agent works in their directory
cd ./worktrees/agent-frontend
```

### Bootstrap Script

```bash
#!/bin/bash
# agent-bootstrap.sh

AGENT_ID="agent-$(date +%s)"
PROJECT="my-project"

# 1. Create unique branch and worktree
git branch $AGENT_ID main
git worktree add ./worktrees/$AGENT_ID $AGENT_ID

# 2. Register with Agent Mail
call_mcp_tool "register_agent" \
  --name "BlueBuilder" \
  --project $PROJECT

# 3. Reserve critical files
call_mcp_tool "file_reservation_paths" \
  --agent "BlueBuilder" \
  --paths '["src/frontend/*"]' \
  --exclusive true

# 4. Pull tasks from Beads
bd issue list --status ready
```

## Workflow Example

### Morning Standup

1. **Pull latest**: `git pull && bd sync`
2. **Check inbox**: `fetch_inbox()`
3. **Check tasks**: `bd issue list --status ready`
4. **Reserve files**: `file_reservation_paths()`
5. **Start work**: Implement task

### Work Complete

1. **Commit**: `git add . && git commit -m "feat: ..."`
2. **Update issue**: `bd issue update --status done`
3. **Notify team**: `send_message(...)`
4. **Release reservation**: `file_reservation_release(...)`
5. **Push**: `git push`

## Best Practices

1. **Always reserve files** before editing
2. **Enable enforcement** via pre-commit hooks
3. **Use unique branches** for each worktree
4. **Sync frequently** to avoid conflicts
5. **Clear reservations** when done

## Environment Variables

```bash
export AGENT_MAIL_PATH="./mail"
export BEADS_PATH=".beads"
export FILE_RESERVATIONS_ENFORCEMENT_ENABLED=true
```

## Integration with Open Interpreter

```python
from interpreter import interpreter

# Agent Mail integration
interpreter.agent_mail_enabled = True
interpreter.project_key = "my-project"

# Beads integration
interpreter.beads_enabled = True
interpreter.beads_path = ".beads"

# Worktree awareness
interpreter.worktree_path = "./worktrees/agent-frontend"
```
