# KKH Nursing Chatbot - Fly.io Deployment Guide

## Prerequisites

1. **Install Fly.io CLI (flyctl)**:
   ```powershell
   # For Windows PowerShell
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Create a Fly.io account** at https://fly.io

3. **Login to Fly.io**:
   ```bash
   flyctl auth login
   ```

## Deployment Steps

### Option 1: Automatic Deployment

1. Run the deployment script:
   ```bash
   # For Unix/Linux/macOS
   chmod +x deploy.sh
   ./deploy.sh
   
   # For Windows
   bash deploy.sh
   ```

### Option 2: Manual Deployment

1. **Initialize the Fly.io app** (if not done already):
   ```bash
   flyctl launch --no-deploy
   ```

2. **Set environment variables** (if using external LLM server):
   ```bash
   flyctl secrets set LLM_SERVER_URL=https://your-llm-server.com
   ```

3. **Deploy the application**:
   ```bash
   flyctl deploy
   ```

4. **Check deployment status**:
   ```bash
   flyctl status
   ```

5. **View logs**:
   ```bash
   flyctl logs
   ```

## Configuration

### Environment Variables

- `LLM_SERVER_URL`: URL of your LLM server (optional, defaults to local development server)
- `PORT`: Port number (automatically set by Fly.io to 8501)

### Scaling

To scale your application:
```bash
# Scale to 2 instances
flyctl scale count 2

# Scale memory
flyctl scale memory 2048
```

### Custom Domain

To add a custom domain:
```bash
flyctl certs create your-domain.com
```

## Important Notes

1. **LLM Server**: The application expects an external LLM server. Make sure your LLM server is accessible from the internet or consider deploying it separately.

2. **File Storage**: The `data/` folder with PDFs will be included in the deployment. For production, consider using external storage.

3. **Embedding Model**: The SentenceTransformer model will be downloaded during the first run, which may take some time.

4. **Costs**: Fly.io has a generous free tier, but monitor your usage to avoid unexpected charges.

## Troubleshooting

### Common Issues:

1. **Build fails**: Check that all dependencies are in `requirements.txt`
2. **App doesn't start**: Check logs with `flyctl logs`
3. **LLM connection fails**: Verify the LLM_SERVER_URL environment variable
4. **Model loading issues**: Increase memory allocation in `fly.toml`

### Useful Commands:

```bash
# Restart the app
flyctl machine restart

# SSH into the app
flyctl ssh console

# Check resource usage
flyctl machine list

# Update secrets
flyctl secrets list
flyctl secrets set KEY=value
```

## Support

For Fly.io specific issues, check their documentation: https://fly.io/docs/
