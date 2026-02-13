# Multi-Agent Coordination Workflows

## Beads Village Pattern

A "Beads Village" is a self-contained ecosystem where multiple AI agents collaborate autonomously using Agent Mail for communication and Beads for task management.

## Repository Layout

```
/my-project
 ├── .git                    # Shared object database
 ├── .beads/                 # Shared issue graph
 │    ├── issues.jsonl       # All issues
 │    └── cache.db          # SQLite cache
 ├── mail/                   # Agent Mail storage
 │    ├── inbox/             # Agent inboxes
 │    └── outbox/           # Sent messages
 ├── worktrees/
 │    ├── agent-frontend/    # Frontend agent workspace
 │    ├── agent-backend/    # Backend agent workspace
 │    └── agent-devops/     # DevOps agent workspace
 └── src/                    # Main codebase
```

## Agent Types

### 1. Frontend Agent
- **Name**: GreenCastle
- **Branch**: agent-frontend
- **Worktree**: ./worktrees/agent-frontend
- **Focus**: UI components, React, CSS
- **Reserved Files**: src/components/*, src/pages/*

### 2. Backend Agent
- **Name**: BlueBuilder  
- **Branch**: agent-backend
- **Worktree**: ./worktrees/agent-backend
- **Focus**: API routes, database, auth
- **Reserved Files**: src/api/*, src/models/*

### 3. DevOps Agent
- **Name**: RedStorm
- **Branch**: agent-devops
- **Worktree**: ./worktrees/agent-devops
- **Focus**: CI/CD, infrastructure, deployment
- **Reserved Files**: .github/*, terraform/*, docker/*

## Daily Workflow

### Morning (All Agents)

```bash
# 1. Sync latest changes
git fetch origin
git pull origin main

# 2. Sync Beads
bd sync

# 3. Check inbox
fetch_inbox --project my-project --agent $AGENT_NAME

# 4. Get ready tasks
bd issue list --status ready

# 5. Reserve files
file_reservation_paths --paths $MY_FILES --ttl 3600
```

### Work Phase

```python
# Agent workflow
async def agent_work_loop():
    while True:
        # Check for new messages
        messages = fetch_inbox()
        
        # Check for new tasks
        issues = bd.list(status="ready")
        
        # If there's work
        if issues:
            issue = issues[0]
            
            # Reserve related files
            files = get_related_files(issue)
            reserve(files)
            
            # Do the work
            await implement(issue)
            
            # Update issue
            bd.update(issue.id, status="done")
            
            # Notify team
            send_message(
                to="coordinator",
                subject=f"Completed: {issue.title}"
            )
            
            # Release reservations
            release(files)
        
        # Sleep before next iteration
        await sleep(60)
```

### Evening (All Agents)

```bash
# 1. Commit changes
git add -A
git commit -m "agent: completed task bd-xxxx"

# 2. Push branch
git push origin agent-$NAME

# 3. Update issue status
bd issue update bd-xxxx --status merged

# 4. Release all reservations
file_reservation_release --all
```

## Coordination Patterns

### Pattern 1: Independent Work

Agents work on different features simultaneously:

```
Agent A: Feature X (branch agent-a)
Agent B: Feature Y (branch agent-b)
Agent C: Feature Z (branch agent-c)

# No conflicts - different files
```

### Pattern 2: Handoff

One agent completes work, hands off to another:

```
1. Agent A completes backend API
2. Agent A sends message to Agent B
3. Agent B reserves frontend files
4. Agent B builds UI for API
```

### Pattern 3: Blocked Dependency

One agent waits for another:

```
Agent A: Implement User API (issue bd-001)
Agent B: Build User Dashboard (issue bd-002, blocks: bd-001)

# Beads shows bd-002 as "blocked"
# Agent B works on something else until bd-001 done
```

### Pattern 4: Shared Component

Two agents need same file:

```
1. Agent A reserves shared/utils.ts
2. Agent A works on utility functions
3. Agent B tries to reserve - gets conflict
4. Agent B waits or works on different files
5. Agent A releases, Agent B reserves
```

## Conflict Resolution

### Advisory Mode (Default)

```bash
# Agent tries to reserve already-reserved file
file_reservation_paths --paths ["src/shared/utils.ts"]
# Returns: CONFLICT - BlueBuilder has exclusive reservation
# Agent chooses: wait, work on something else, or request override
```

### Enforced Mode (Strict)

```bash
# Enable enforcement
export FILE_RESERVATIONS_ENFORCEMENT_ENABLED=true

# Install pre-commit guard
install_precommit_guard

# Now commits are blocked if they modify reserved files
git commit -m "fix utils"
# Error: Cannot commit - src/shared/utils.ts is reserved by BlueBuilder
```

## CI/CD Integration

### Dynamic Agent Spin-up

```yaml
# .github/workflows/agent.yml
name: Agent Work

on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 8am

jobs:
  agent:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Create agent branch
        run: |
          AGENT_ID="agent-${{ github.run_id }}"
          git branch $AGENT_ID main
          git worktree add ./worktrees/$AGENT_ID $AGENT_ID
      
      - name: Register agent
        run: |
          # Call Agent Mail API
          curl -X POST $AGENT_MAIL_URL/register \
            -d '{"name": "CI-${{ github.run_id }}", ...}'
      
      - name: Get ready tasks
        run: bd issue list --status ready
      
      - name: Execute work
        run: |
          # Run Open Interpreter in agent worktree
          cd ./worktrees/agent-${{ github.run_id }}
          interpreter --task "$(bd issue next)"
      
      - name: Cleanup
        run: |
          git worktree remove ./worktrees/$AGENT_ID
          git branch -d agent-${{ github.run_id }}
```

## Monitoring & Observability

### Web UI

Access at `http://agent-mail:3000`:
- Browse all agent inboxes
- Read message threads
- View file reservations
- Search messages

### Metrics

```bash
# Active reservations
file_reservation_list --status active

# Agent activity
bd issue activity --days 7

# Message volume
mail stats --by-agent
```

## Best Practices

1. **Unique Branches**: Always create new branch for new worktree
2. **Short TTLs**: Use 1-2 hour reservations, extend if needed
3. **Frequent Sync**: Pull and push frequently
4. **Clear Messages**: Use descriptive subjects and bodies
5. **Respect Reservations**: Don't ignore conflicts
6. **Enable Enforcement**: Use pre-commit guard in production
7. **Prune Worktrees**: Clean up stale worktrees regularly
