# KKH Nursing Chatbot Deployment Script for Fly.io (Windows PowerShell)

Write-Host "🏥 KKH Nursing Chatbot - Fly.io Deployment" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Check if flyctl is installed
if (!(Get-Command flyctl -ErrorAction SilentlyContinue)) {
    Write-Host "❌ flyctl is not installed. Please install it first:" -ForegroundColor Red
    Write-Host "https://fly.io/docs/hands-on/install-flyctl/" -ForegroundColor Yellow
    exit 1
}

# Check if user is logged in to Fly.io
try {
    flyctl auth whoami | Out-Null
} catch {
    Write-Host "🔐 Please log in to Fly.io first:" -ForegroundColor Yellow
    flyctl auth login
}

# Check if OPENROUTER_API_KEY is set
$OPENROUTER_API_KEY = $env:OPENROUTER_API_KEY
if (-not $OPENROUTER_API_KEY) {
    Write-Host "🔑 Setting up OpenRouter API Key..." -ForegroundColor Yellow
    $OPENROUTER_API_KEY = Read-Host "Please enter your OpenRouter API Key" -AsSecureString
    $OPENROUTER_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($OPENROUTER_API_KEY))
    
    if (-not $OPENROUTER_API_KEY) {
        Write-Host "❌ OpenRouter API Key is required. Get one from: https://openrouter.ai/" -ForegroundColor Red
        exit 1
    }
}

Write-Host "🚀 Deploying to Fly.io..." -ForegroundColor Green

# Set secrets
Write-Host "📝 Setting OpenRouter API Key..." -ForegroundColor Yellow
flyctl secrets set "OPENROUTER_API_KEY=$OPENROUTER_API_KEY"

# Deploy the application
Write-Host "🚀 Deploying application..." -ForegroundColor Green
flyctl deploy

# Show status
Write-Host "📊 Application status:" -ForegroundColor Green
flyctl status

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "🌐 Your application should be available at: https://kkh-nursing-chatbot.fly.dev" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Useful commands:" -ForegroundColor Yellow
Write-Host "  flyctl logs        - View application logs" -ForegroundColor White
Write-Host "  flyctl ssh console - SSH into the application" -ForegroundColor White
Write-Host "  flyctl status      - Check application status" -ForegroundColor White
Write-Host "  flyctl scale count 1  - Scale to 1 instance" -ForegroundColor White
