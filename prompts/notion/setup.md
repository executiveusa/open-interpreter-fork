# Notion Integration Setup

## Overview
Connect Open Interpreter with Notion for powerful knowledge management, second brain systems, and productivity workflows.

## Prerequisites

1. Notion Account
2. Notion Integration Token
3. Notion Pages/Databases to connect

## Setup Steps

### 1. Create Integration

1. Go to [Notion My Integrations](https://www.notion.so/my-integrations)
2. Click "+ New integration"
3. Name: "Open Interpreter"
4. Select appropriate capabilities:
   - Read content
   - Update content
   - Insert content
5. Copy the "Internal Integration Secret"

### 2. Connect to Your Workspace

1. Go to the Notion page/database you want to access
2. Click "..." menu → "Connect to" → Select your integration
3. Repeat for each page/database

### 3. Configure Open Interpreter

```python
import os
from interpreter import interpreter
from notion_client import Client

# Set up Notion client
notion = Client(auth=os.environ["NOTION_API_KEY"])

# Store in interpreter for easy access
interpreter.notion = notion
```

### 4. Environment Variables

```bash
export NOTION_API_KEY="secret_xxxxxxxxxxxxxxxxxxxxx"
export NOTION_DATABASE_ID="your_database_id"
```

## Quick Start Prompt

```
Connect to my Notion workspace and:
1. List all databases I have access to
2. Show me the structure of my [database name] database
3. Create a test page with some sample content
```

## Core Operations

### Reading Data

```python
# Query a database
results = notion.databases.query(
    database_id="your_database_id",
    filter={"property": "Status", "status": {"equals": "In Progress"}}
)

# Get a page
page = notion.pages.retrieve(page_id="page_id")

# Get page content
blocks = notion.blocks.children.list(block_id="page_id")
```

### Writing Data

```python
# Create a new page
new_page = notion.pages.create(
    parent={"database_id": "your_database_id"},
    properties={
        "Name": {"title": [{"text": {"content": "New Task"}}]},
        "Status": {"status": {"name": "Not Started"}}
    }
)

# Update a page
notion.pages.update(
    page_id="page_id",
    properties={"Status": {"status": {"name": "Done"}}}
)
```

### Working with Blocks

```python
# Add content to a page
notion.blocks.children.append(
    block_id="page_id",
    children=[
        {"object": "block", "type": "paragraph", 
         "paragraph": {"rich_text": [{"text": {"content": "Hello World"}}]}}
    ]
)
```

## Integration with Open Interpreter

The following prompt initializes Notion integration:

```
Initialize Notion integration with my API key. Use database [YOUR_DATABASE_ID] as the primary database. Create helper functions for:
- Creating tasks with title, status, and due date
- Querying tasks by status
- Updating task properties
```

## Common Use Cases

| Use Case | Description |
|----------|-------------|
| Second Brain | Store and retrieve all conversations |
| Task Management | Track todos and projects |
| Content Calendar | Plan and schedule content |
| Meeting Notes | Document meetings with action items |
| Knowledge Base | Organize research and documentation |

## Security Notes

- Never commit API keys to version control
- Use environment variables
- Restrict integration permissions to only needed pages
- Rotate keys periodically
