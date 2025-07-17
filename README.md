# KKH Nursing Chatbot - Fly.io Deployment

A nursing assistant chatbot for KK Women's and Children's Hospital, powered by OpenRouter and deployed on Fly.io.

## Features

- **Clinical Guidelines**: Ask questions and get relevant medical guidance
- **Fluid Calculator**: Calculate daily fluid requirements based on patient weight
- **Educational Quizzes**: Interactive quizzes for nursing education
- **24/7 Availability**: Always accessible AI-powered assistant

## Architecture

- **Backend**: FastAPI with OpenRouter integration
- **Frontend**: Modern HTML/CSS/JavaScript interface
- **AI Model**: Configurable models via OpenRouter API
- **Deployment**: Containerized deployment on Fly.io

## Prerequisites

1. **Fly.io Account**: Sign up at [fly.io](https://fly.io)
2. **OpenRouter API Key**: Get one from [openrouter.ai](https://openrouter.ai)
3. **Flyctl CLI**: Install from [fly.io/docs/hands-on/install-flyctl/](https://fly.io/docs/hands-on/install-flyctl/)

## Quick Deployment

### Option 1: Using PowerShell (Windows)
```powershell
# Set your OpenRouter API key
$env:OPENROUTER_API_KEY = "your-api-key-here"

# Run deployment script
.\deploy.ps1
```

### Option 2: Using Bash (Linux/Mac)
```bash
# Set your OpenRouter API key
export OPENROUTER_API_KEY="your-api-key-here"

# Make script executable and run
chmod +x deploy.sh
./deploy.sh
```

### Option 3: Manual Deployment

1. **Login to Fly.io**:
   ```bash
   flyctl auth login
   ```

2. **Launch the app** (first time only):
   ```bash
   flyctl launch
   ```

3. **Set OpenRouter API Key**:
   ```bash
   flyctl secrets set OPENROUTER_API_KEY="your-api-key-here"
   ```

4. **Deploy**:
   ```bash
   flyctl deploy
   ```

## Configuration

### Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)
- `PORT`: Application port (default: 8080)

### OpenRouter Model Configuration

The default model is `mistralai/mistral-7b-instruct`. To change the model, update the `OpenRouterLLM` class in `backend/chatbot.py`:

```python
def __init__(self, model_name="meta-llama/llama-3.1-8b-instruct"):
    self.model_name = model_name
    # ... rest of the configuration
```

Available models: [OpenRouter Models](https://openrouter.ai/models)

## Development

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   ```bash
   export OPENROUTER_API_KEY="your-api-key-here"
   ```

3. **Run the application**:
   ```bash
   python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8080
   ```

4. **Access the application**:
   - Frontend: http://localhost:8080
   - API docs: http://localhost:8080/docs

### Project Structure

```
├── backend/
│   ├── main.py          # FastAPI application
│   ├── routes.py        # API routes
│   └── chatbot.py       # OpenRouter integration
├── frontend/
│   ├── index.html       # Main UI
│   ├── script.js        # Frontend logic
│   └── style.css        # Styling
├── Dockerfile           # Container configuration
├── fly.toml             # Fly.io configuration
├── requirements.txt     # Python dependencies
└── deploy.*             # Deployment scripts
```

## API Endpoints

- `GET /` - Main application interface
- `POST /api/ask` - Ask questions to the chatbot
- `GET /api/health` - Health check endpoint
- `GET /health` - Application health status

## Monitoring and Maintenance

### View Logs
```bash
flyctl logs
```

### Check Application Status
```bash
flyctl status
```

### Scale Application
```bash
flyctl scale count 1
```

### SSH into Application
```bash
flyctl ssh console
```

## Troubleshooting

### Common Issues

1. **OpenRouter API Key Not Set**:
   - Ensure the API key is set as a secret: `flyctl secrets set OPENROUTER_API_KEY="your-key"`

2. **Application Not Starting**:
   - Check logs: `flyctl logs`
   - Verify health check: `curl https://your-app.fly.dev/health`

3. **Memory Issues**:
   - Scale up memory: `flyctl scale memory 2gb`

### Getting Support

- Check the logs: `flyctl logs`
- Review Fly.io documentation: [fly.io/docs](https://fly.io/docs)
- OpenRouter documentation: [openrouter.ai/docs](https://openrouter.ai/docs)

## Security Notes

- API keys are stored as encrypted secrets in Fly.io
- HTTPS is enforced for all connections
- CORS is configured for secure cross-origin requests

## License

This project is developed for KK Women's and Children's Hospital educational purposes.
