# OpenClaw Second Brain Workflow

## Concept
The second brain system uses OpenClaw's memory capabilities to remember everything you tell it. Just text your bot from anywhere and it remembers.

## Quick Setup

Send this prompt to your OpenClaw bot:

```
I want to build a second brain system where I can review all our notes, conversations, and memories. Please build that out with Next.js.
```

## Features

### 1. Memory Storage
- Remember anything via text message
- iMessage, Telegram, Discord support
- Automatic categorization

### 2. Search & Retrieval
- Global search (Cmd+K)
- Filter by tags, date, source
- Full-text search across all memories

### 3. Conversation History
- View all past conversations
- Timeline view
- Topic-based grouping

### 4. Easy Input
- Text from phone = saved to brain
- No complex apps needed
- Simple text interface

## Usage Examples

### Saving Memories

**From Telegram/iMessage/Discord:**
```
Hey, remember that I want to read the book about local LLMs
```

```
Remind me about the meeting at 3pm tomorrow
```

```
Please remember this link: [URL]
```

### Retrieving Memories

**In the web interface:**
```
Search for: local LLMs
```

```
Show me memories from last week
```

```
Find everything about [topic]
```

## System Components

### 1. Memory Database
- SQLite for fast access
- Full-text search
- Tag-based organization

### 2. Web Interface
- Next.js application
- Real-time sync
- Mobile-responsive

### 3. Message Handlers
- Telegram bot
- Discord bot  
- iMessage (via Mac)

### 4. Sync System
- Git-backed storage
- Cross-device sync
- Version history

## Prompt Templates

### Template 1: Basic Second Brain

```
Build a second brain system where:
- I can save memories via text message
- I can search and retrieve memories
- Memories are organized by tags
- There's a nice UI to browse everything
- Everything syncs across my devices
```

### Template 2: Advanced Second Brain

```
Create a second brain with:
1. Memory storage with importance levels
2. Auto-tagging based on content
3. Conversation threading
4. Task extraction from conversations
5. Daily memory review feature
6. Export capabilities
```

### Template 3: Research-Focused Brain

```
Build a research second brain:
- Save links and articles
- Add notes and annotations
- Create study guides from saved content
- Track learning progress
- Connect related concepts
```

## Implementation Details

### Backend (Python/FastAPI)
```python
# Core memory storage
class MemoryStore:
    def add(self, content, metadata):
        # Save to database
        # Auto-tag
        # Index for search
        
    def search(self, query):
        # Full-text search
        # Return ranked results
        
    def get_timeline(self, days=30):
        # Get memories by date
```

### Frontend (Next.js)
```javascript
// Search component
function SearchModal() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  
  // Global keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.metaKey && e.key === 'k') {
        // Open search
      }
    }
  })
}
```

### Message Handlers
```python
# Telegram handler
@bot.message_handler()
def handle_message(message):
    # Parse intent
    # Save memory
    # Confirm to user
```

## Best Practices

1. **Consistent Input**: Use same trigger phrases
2. **Regular Review**: Weekly memory review
3. **Tag Strategy**: Consistent tagging system
4. **Important Markers**: Mark truly important items
5. **Clean Up**: Remove duplicates regularly

## Benefits

- No complex apps to manage
- Just text your bot
- Everything remembered
- Easy search
- Cross-platform
- Free (just API costs)

## Cost

- Bot API costs: ~$10-20/month
- Hosting: Free (self-hosted or Vercel)
- Total: ~$10-20/month

Compare to:
- Notion: $10/month
- Apple Notes: Free but limited
- Evernote: $10/month

This system is free and more powerful!
