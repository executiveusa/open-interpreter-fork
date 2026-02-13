# OpenClaw Morning Brief Workflow

## Concept
Every morning at 8am, your bot sends you a completely custom morning brief with everything you need to know for the day. Scheduled, automated, personalized.

## Quick Setup

Send this prompt to your OpenClaw bot:

```
I want to set up a regular morning brief. Every morning, send me a report through Telegram. I want this report to include:
1. New stories relevant to my interest
2. Ideas for businesses I can create
3. Tasks I need to complete today
4. Recommendations for tasks we can complete together today
```

## What's Included

### 1. AI News/Stories
- Researches top AI stories from last 24 hours
- Curates based on your interests
- Summarizes key points

### 2. Business Ideas
- Generates startup ideas based on trends
- Identifies market opportunities
- Validates ideas quickly

### 3. Your Tasks
- Pulls from your task manager
- Shows due today
- Prioritizes by urgency

### 4. AI Can-Do List
- Bot suggests tasks it can help with
- Things you didn't know it could do
- Saves you hours of work

## Usage Examples

### Basic Morning Brief

```
Set up a morning brief that includes:
- Top 3 news stories from yesterday
- My calendar for today
- Tasks due today
- Weather for my location
```

### Advanced Morning Brief

```
Create a detailed morning brief:
1. AI industry news (last 24 hours)
2. YouTube video ideas based on trends
3. Tasks from my Notion database
4. Ideas for new content
5. Things you can help me with today
6. Quick tips for productivity
```

### Business-Focused Brief

```
Morning brief for entrepreneurs:
1. Tech startup news
2. Funding rounds in my space
3. Competitor updates
4. Tasks from project management
5. Meeting reminders
6. Action items from yesterday
```

## Customization Options

| Component | Options |
|-----------|---------|
| Time | 6am, 7am, 8am, 9am |
| Channel | Telegram, Discord, iMessage, Email |
| News Sources | Twitter, Reddit, News APIs, Custom |
| Task Sources | Notion, Todoist, Calendar, GitHub |
| Format | Text, Markdown, HTML |

## Prompt Templates

### Template 1: Basic

```
Every morning at 8am, send me a brief with:
- 3 interesting news stories
- My calendar for today
- Tasks due today
```

### Template 2: Content Creator

```
Morning brief at 7am:
1. Trending topics on Twitter
2. YouTube trending videos
3. Content ideas for today
4. My scheduled posts
5. Engagement metrics from yesterday
```

### Template 3: Developer

```
Developer morning brief:
1. GitHub trending repos
2. New releases from followed repos
3. PRs needing review
4. Documentation updates
5. Stack Overflow questions in my tags
```

### Template 4: Entrepreneur

```
Entrepreneur daily brief:
1. Startup news and funding
2. Competitor moves
3. Customer feedback summary
4. Sales pipeline update
5. Team standup notes
6. Action items
```

## How It Works

### Scheduling
```python
# Cron job for morning brief
cron.schedule("0 8 * * *", send_morning_brief)
```

### Research Phase
```python
async def research():
    # 1. Fetch news
    news = await fetch_news()
    
    # 2. Analyze trends
    trends = await analyze_trends(news)
    
    # 3. Generate ideas
    ideas = await generate_ideas(trends)
    
    return {"news": news, "trends": trends, "ideas": ideas}
```

### Task Aggregation
```python
async def get_tasks():
    # Pull from multiple sources
    notion_tasks = await get_notion_tasks()
    github_tasks = await get_github_issues()
    calendar_events = await get_calendar()
    
    return aggregate_and_prioritize([notion_tasks, github_tasks, calendar_events])
```

### Delivery
```python
async def send_brief(brief, channel="telegram"):
    if channel == "telegram":
        await telegram.send(brief)
    elif channel == "discord":
        await discord.send(brief)
    # etc.
```

## Benefits

1. **Zero Effort**: Set it and forget it
2. **Personalized**: Only relevant info
3. **Proactive**: AI suggests tasks it can do
4. **Multi-channel**: Get it where you want
5. **Time Saved**: Hours of research done for you

## Example Output

```
☀️ Good Morning!

📰 TOP NEWS
1. OpenAI releases new model with breakthrough capabilities
2. Tech giants investing heavily in AI infrastructure
3. New study shows 40% productivity increase with AI assistants

💡 BUSINESS IDEAS
1. AI-powered code review tool for enterprise
2. Personalized learning platform using local LLMs
3. Automated documentation generator for APIs

📋 YOUR TASKS
- [ ] Review PR #234 (High)
- [ ] Update documentation (Medium)  
- [ ] Team meeting at 2pm (Low)

🤖 I CAN HELP WITH
- Write unit tests for the new feature
- Generate release notes
- Refactor the authentication module

Have a productive day!
```

## Cost

- API costs only
- Research runs while you sleep
- ~$20-50/month depending on usage

## Pro Tips

1. **Customize Channels**: Use multiple channels if needed
2. **Adjust Time**: Find your optimal wake-up time
3. **Iterate**: Refine the brief over time
4. **Add Sources**: Keep adding relevant sources
5. **Review**: Check what you actually read and adjust
