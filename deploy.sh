#!/bin/bash

# KKH Nursing Chatbot Deployment Script for Fly.io

echo "🏥 KKH Nursing Chatbot - Fly.io Deployment"
echo "=========================================="

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "❌ flyctl is not installed. Please install it first:"
    echo "https://fly.io/docs/hands-on/install-flyctl/"
    exit 1
fi

# Check if user is logged in to Fly.io
if ! flyctl auth whoami &> /dev/null; then
    echo "🔐 Please log in to Fly.io first:"
    flyctl auth login
fi

# Check if OPENROUTER_API_KEY is set
if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "🔑 Setting up OpenRouter API Key..."
    echo "Please enter your OpenRouter API Key:"
    read -s OPENROUTER_API_KEY
    if [ -z "$OPENROUTER_API_KEY" ]; then
        echo "❌ OpenRouter API Key is required. Get one from: https://openrouter.ai/"
        exit 1
    fi
fi

echo "🚀 Deploying to Fly.io..."

# Set secrets
echo "📝 Setting OpenRouter API Key..."
flyctl secrets set OPENROUTER_API_KEY="$OPENROUTER_API_KEY"

# Deploy the application
echo "🚀 Deploying application..."
flyctl deploy

# Show status
echo "📊 Application status:"
flyctl status

echo "✅ Deployment complete!"
echo "🌐 Your application should be available at: https://kkh-nursing-chatbot.fly.dev"
echo ""
echo "📋 Useful commands:"
echo "  flyctl logs        - View application logs"
echo "  flyctl ssh console - SSH into the application"
echo "  flyctl status      - Check application status"
echo "  flyctl scale count 1  - Scale to 1 instance"
