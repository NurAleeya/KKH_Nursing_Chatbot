#!/bin/bash

# Fly.io Deployment Script for KKH Nursing Chatbot

echo "🚀 Deploying KKH Nursing Chatbot to Fly.io..."

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "❌ flyctl is not installed. Please install it first:"
    echo "   PowerShell: iwr https://fly.io/install.ps1 -useb | iex"
    echo "   Or visit: https://fly.io/docs/getting-started/installing-flyctl/"
    exit 1
fi

# Check if user is logged in
if ! flyctl auth whoami &> /dev/null; then
    echo "🔐 Please log in to Fly.io first:"
    echo "   flyctl auth login"
    exit 1
fi

# Deploy the application
echo "📦 Building and deploying application..."
flyctl deploy

echo "✅ Deployment completed!"
echo "🌐 Your application should be available at:"
flyctl status --app kkh-nursing-chatbot
