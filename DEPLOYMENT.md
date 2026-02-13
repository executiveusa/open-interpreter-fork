# Open Interpreter - Production Deployment Guide

This guide covers deploying Open Interpreter with the multi-agent coordination system and real-time dashboard.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Configuration](#configuration)
5. [Monitoring](#monitoring)
6. [Scaling](#scaling)
7. [Security](#security)

---

## Quick Start

### Prerequisites

- Docker and Docker Compose
- At least one LLM API key (OpenAI or Anthropic)
- (Optional) Composio, Notion API keys for integrations

### 1. Clone and Configure

```bash
# Clone the repository
git clone https://github.com/executiveusa/open-interpreter-fork.git
cd open-interpreter-fork

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 2. Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 3. Access the Application

- **Dashboard**: http://localhost:5000
- **LMC Server**: ws://localhost:8000

---

## Docker Deployment

### Development Mode

```bash
# Build and run with hot reload
docker-compose up --build
```

### Production Mode

```bash
# Build production image
docker build -f Dockerfile.production -t open-interpreter:latest .

# Run with environment file
docker run -d \
  --name interpreter \
  -p 5000:5000 \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  open-interpreter:latest
```

### With Nginx (Recommended for Production)

```bash
# Start with nginx profile
docker-compose --profile production up -d
```

---

## Cloud Deployment

### AWS ECS

```yaml
# task-definition.json
{
  "family": "open-interpreter",
  "containerDefinitions": [
    {
      "name": "interpreter",
      "image": "your-ecr-repo/open-interpreter:latest",
      "essential": true,
      "portMappings": [
        {"containerPort": 5000, "protocol": "tcp"},
        {"containerPort": 8000, "protocol": "tcp"}
      ],
      "environment": [
        {"name": "LOG_LEVEL", "value": "INFO"}
      ],
      "secrets": [
        {"name": "OPENAI_API_KEY", "valueFrom": "arn:aws:secretsmanager:..."}
      ]
    }
  ],
  "cpu": "1024",
  "memory": "2048",
  "networkMode": "awsvpc"
}
```

### Google Cloud Run

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/open-interpreter

# Deploy to Cloud Run
gcloud run deploy open-interpreter \
  --image gcr.io/PROJECT_ID/open-interpreter \
  --port 5000 \
  --set-env-vars OPENAI_API_KEY=your-key
```

### Heroku

```bash
# Create Heroku app
heroku create open-interpreter

# Set environment variables
heroku config:set OPENAI_API_KEY=your-key

# Deploy
git push heroku main
```

### DigitalOcean App Platform

```yaml
# app.yaml
name: open-interpreter
services:
  - name: interpreter
    dockerfile_path: Dockerfile.production
    source_dir: .
    github:
      repo: executiveusa/open-interpreter-fork
      branch: main
    envs:
      - key: OPENAI_API_KEY
        value: your-key
    http_port: 5000
    instance_count: 1
    instance_size_slug: basic-xxs
```

---

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes* | OpenAI API key |
| `ANTHROPIC_API_KEY` | Yes* | Anthropic API key |
| `COMPOSIO_API_KEY` | No | Composio integration key |
| `NOTION_API_KEY` | No | Notion integration key |
| `SECRET_KEY` | Yes | Flask secret key |
| `LOG_LEVEL` | No | Logging level (default: INFO) |

*At least one LLM API key is required

### Agent Mail Configuration

```bash
# Path for agent mail storage
AGENT_MAIL_PATH=./data/mail

# Path for Beads issue tracking
BEADS_PATH=./data/beads

# Enable file reservation enforcement
FILE_RESERVATIONS_ENFORCEMENT_ENABLED=true
```

---

## Monitoring

### Health Checks

```bash
# Dashboard health
curl http://localhost:5000/api/state

# LMC server health
curl http://localhost:8000/health
```

### Logs

```bash
# Docker logs
docker-compose logs -f interpreter

# Application logs
tail -f logs/app.log
```

### Metrics

The dashboard provides real-time metrics:
- Active agents count
- Message throughput
- Issue status distribution
- File reservation status

---

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  interpreter:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

```bash
docker-compose -f docker-compose.yml -f docker-compose.scale.yml up -d
```

### Load Balancing

Use nginx for load balancing multiple instances:

```nginx
upstream dashboard {
    least_conn;
    server interpreter-1:5000;
    server interpreter-2:5000;
    server interpreter-3:5000;
}
```

---

## Security

### 1. API Key Management

Never commit API keys to version control. Use:
- Environment variables
- Secret management (AWS Secrets Manager, HashiCorp Vault)
- Docker secrets

### 2. Network Security

```yaml
# Restrict to internal network
services:
  interpreter:
    networks:
      - internal
    ports: []  # No external ports

  nginx:
    networks:
      - internal
      - external
    ports:
      - "80:80"
```

### 3. HTTPS

Always use HTTPS in production:

```bash
# Generate SSL certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/key.pem -out ssl/cert.pem
```

### 4. Rate Limiting

Nginx configuration includes rate limiting:

```nginx
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
```

---

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find and kill process
   lsof -i :5000
   kill -9 <PID>
   ```

2. **API key not found**
   ```bash
   # Verify environment
   docker-compose exec interpreter env | grep API_KEY
   ```

3. **WebSocket connection failed**
   - Check nginx configuration
   - Verify firewall allows WebSocket traffic

### Debug Mode

```bash
# Run with debug logging
LOG_LEVEL=DEBUG docker-compose up
```

---

## Support

- GitHub Issues: https://github.com/executiveusa/open-interpreter-fork/issues
- Documentation: https://docs.openinterpreter.com
