# OpenClaw Content Factory Workflow

## Concept
A fully automated content creation system using multiple AI agents. Research → Write → Design → all automated.

## Quick Setup

Send this prompt to your OpenClaw bot:

```
Build me a content factory inside of Discord. Set up channels for different agents. Have an agent that researches top trending stories, another agent that takes those stories and writes scripts, then another agent that generates thumbnails. Have all their work organized in different channels.
```

## How It Works

### Agent Architecture

```
┌─────────────────┐
│  Coordinator    │  Orchestrates workflow
└────────┬────────┘
         │
    ┌────┴────┬────────────┐
    ▼         ▼            ▼
┌───────┐ ┌───────┐   ┌────────┐
│Henry  │ │Quill  │   │Pixel   │
│Research│ │Writer │   │Designer│
│Agent  │ │Agent  │   │Agent   │
└───┬───┘ └───┬───┘   └───┬────┘
    │         │           │
    ▼         ▼           ▼
Stories    Scripts    Thumbnails
```

### Daily Workflow (8am)

1. **Henry (Research)** - Scans for trending topics
2. **Quill (Writer)** - Picks best idea, writes script
3. **Pixel (Designer)** - Generates thumbnail
4. **Coordinator** - Posts to platforms

## Usage Examples

### YouTube Content Factory

```
Set up a YouTube content factory:
1. Research agent scans: Twitter, Reddit, YouTube trends
2. Writer agent picks best topic, writes full script
3. Designer agent creates thumbnail
4. Post to YouTube with scheduled time
```

### Twitter Thread Factory

```
Create Twitter automation:
1. Research: Find trending topics in my niche
2. Writer: Convert to engaging thread format
3. Schedule: Post at optimal engagement times
4. Analytics: Track impressions and engagement
```

### Blog Content Factory

```
Build blog automation:
1. Research: Find high-ranking keywords
2. Writer: Generate SEO-optimized articles
3. Designer: Create featured images
4. Publish: Post to WordPress/ghost
```

### Newsletter Factory

```
Newsletter workflow:
1. Research: Curate top stories of week
2. Writer: Compile into newsletter format
3. Design: Create header images
4. Send: Schedule via ConvertKit/Mailchimp
```

## Agent Details

### 1. Research Agent (Henry)

**Responsibilities:**
- Monitor multiple sources
- Identify trends
- Score by potential
- Feed to writer

**Sources to Monitor:**
- Twitter/X
- Reddit (relevant subs)
- YouTube trending
- Product Hunt
- Hacker News
- Google Trends

**Output:**
```json
{
  "topic": "Local LLMs on Mac",
  "score": 9.5,
  "sources": ["Twitter", "Reddit"],
  "angle": "How to run GPT-4 locally",
  "potential_views": 100000
}
```

### 2. Writer Agent (Quill)

**Responsibilities:**
- Take research input
- Write script/post
- Match voice/style
- Optimize for platform

**Capabilities:**
- YouTube scripts
- Twitter threads
- Blog posts
- Newsletters
- LinkedIn posts

**Output:**
```json
{
  "title": "Run GPT-4 on Your Mac for FREE",
  "script": "🎬 Full script...",
  "hooks": ["Did you know...", "This changed everything..."],
  "call_to_action": "Subscribe for more"
}
```

### 3. Design Agent (Pixel)

**Responsibilities:**
- Generate thumbnails
- Create social images
- Design banners
- Style consistency

**Tools:**
- DALL-E 3
- Midjourney
- Stable Diffusion
- Local models (e.g., Nano Banana)

**Output:**
- Thumbnail: 1280x720 PNG
- Social: 1200x630 OG image
- Banner: 1546x423 PNG

## Prompt Templates

### Template 1: Basic YouTube Factory

```
Create a YouTube content factory that:
1. Researches trending topics daily at 8am
2. Writes scripts for top 3 ideas
3. Generates thumbnails for each
4. Saves to organized folder structure
```

### Template 2: Multi-Platform Factory

```
Build content factory for:
- YouTube (long-form)
- Twitter (threads)
- LinkedIn (posts)
- Newsletter (weekly digest)

Each piece should be tailored to platform
```

### Template 3: Niche Factory

```
Set up content factory for [niche]:
- Research [industry] trends
- Write in [brand voice]
- Target [audience]
- Post to [platforms]
```

## Discord Setup

### Channels

```
📋 #research-feed     → Trending topics
📝 #scripts           → Written content  
🖼️ #thumbnails        → Generated images
✅ #approved          → Ready to post
🚀 #published         → Live content
📊 #analytics         → Performance data
```

### Bot Commands

```
!research    → Run research now
!write       → Generate new script
!image       → Create thumbnail
!publish     → Post to platform
!analytics   → Show performance
!factory status → Check all agents
```

## Automation Schedule

| Time | Agent | Task |
|------|-------|------|
| 6am | Henry | Research overnight |
| 7am | Quill | Write scripts |
| 8am | Pixel | Generate thumbnails |
| 9am | Coordinator | Human review |
| 10am | Coordinator | Publish |

## Benefits

1. **Scale**: Produce 10x more content
2. **Consistency**: Daily output
3. **Quality**: AI-written, human-reviewed
4. **Speed**: Hours → Minutes
5. **Variety**: Multi-platform from one research

## Real-World Example

```
Morning (while you sleep):
- Henry researches overnight
- Finds: "Local LLMs" trending
- Quill writes script about running GPT-4 locally
- Pixel creates thumbnail

You wake up:
- Full script ready
- Thumbnail ready
- Just review and hit publish

Result: 100K+ views video, while you slept
```

## Cost Analysis

| Component | Cost |
|-----------|------|
| API (Opus) | $200/month |
| Image Gen | $50/month |
| Hosting | $20/month |
| **Total** | **~$270/month** |

Compare to:
- Freelance writer: $500+/video
- Designer: $100+/thumbnail
- This system: Pays for itself after 1 video

## Pro Tips

1. **Human in Loop**: Always review before publishing
2. **Iterate**: Refine based on what performs
3. **Niche Down**: Better for specific niches
4. **Batch**: Generate multiple at once
5. **Repurpose**: Turn one video into 10 tweets
