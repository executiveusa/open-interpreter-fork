#!/bin/bash
# Open Interpreter Vercel Deployment Script
# Project ID: prj_VOcIl5dMZoWyjCda8pcXsdGCIrbc

set -e

echo "=========================================="
echo "Open Interpreter - Vercel Deployment"
echo "=========================================="

# Check for Vercel token
if [ -z "$VERCEL_TOKEN" ]; then
    echo "ERROR: VERCEL_TOKEN environment variable not set"
    echo ""
    echo "To deploy, you need a Vercel token. Get one from:"
    echo "https://vercel.com/account/tokens"
    echo ""
    echo "Then run:"
    echo "export VERCEL_TOKEN='your-token-here'"
    echo "./deploy-vercel.sh"
    exit 1
fi

# Set project ID
PROJECT_ID="prj_VOcIl5dMZoWyjCda8pcXsdGCIrbc"

echo "Project ID: $PROJECT_ID"
echo ""

# Add environment secrets
echo "Setting up environment secrets..."

# Function to add secret
add_secret() {
    local name=$1
    local value=$2
    if [ -n "$value" ]; then
        echo "Setting $name..."
        vercel env add $name production --force --token $VERCEL_TOKEN --project $PROJECT_ID <<< "$value" 2>/dev/null || true
    fi
}

# Add secrets from environment
add_secret "OPENAI_API_KEY" "$OPENAI_API_KEY"
add_secret "ANTHROPIC_API_KEY" "$ANTHROPIC_API_KEY"
add_secret "COMPOSIO_API_KEY" "$COMPOSIO_API_KEY"
add_secret "NOTION_API_KEY" "$NOTION_API_KEY"
add_secret "NOTION_DATABASE_ID" "$NOTION_DATABASE_ID"
add_secret "SECRET_KEY" "oi-vercel-production-secret-key-2024"

echo ""
echo "Deploying to Vercel..."

# Deploy to Vercel
vercel --prod --token $VERCEL_TOKEN --yes --project $PROJECT_ID

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
