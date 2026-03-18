# Deployment Guide

## Overview
This guide provides step-by-step instructions to deploy both the backend (FastAPI) and frontend (React) to production.

## Prerequisites
- GitHub account
- Heroku account (for backend) OR Render account
- Netlify or Vercel account (for frontend)
- MongoDB Atlas account (already set up with database)
- Git installed on your computer

## Part 1: Backend Deployment (Heroku)

### Step 1: Prepare for Deployment
1. Navigate to the backend directory
2. Ensure all files are properly created and dependencies are listed in `requirements.txt`
3. The following deployment files should exist:
   - `Procfile` - Commands to run on Heroku
   - `runtime.txt` - Python version specification
   - `.gitignore` - Files to exclude from Git

### Step 2: Create GitHub Repository
1. Go to https://github.com/new
2. Create a new repository named `sentiment-analysis-backend`
3. Do NOT initialize with README (we already have one)
4. Click "Create repository"

### Step 3: Push Code to GitHub
In terminal within the project root directory:
```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: FastAPI sentiment analysis backend"

# Add remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/sentiment-analysis-backend.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Deploy to Heroku
1. Go to https://www.heroku.com/apps
2. Click "New" → "Create new app"
3. Enter app name: `sentiment-analysis-api-[yourname]` (must be unique)
4. Choose region: `United States`
5. Click "Create app"

### Step 5: Configure Environment Variables
1. In Heroku dashboard, go to Settings tab
2. Click "Reveal Config Vars"
3. Add the following variables:
   - **MONGODB_URI**: Your MongoDB Atlas connection string
     - Get this from MongoDB Atlas: `mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/sentiment_db?retryWrites=true&w=majority`
   - **MONGODB_DB_NAME**: `sentiment_db`
   - **LOG_LEVEL**: `INFO`

### Step 6: Connect GitHub Repository
1. In Heroku dashboard, go to "Deploy" tab
2. Under "Deployment method", select GitHub
3. Click "Connect to GitHub"
4. Search for your repository: `sentiment-analysis-backend`
5. Click "Connect"
6. Under "Automatic deploys", click "Enable Automatic Deploys"
7. Manually deploy by clicking "Deploy Branch" (main branch)

### Step 7: Monitor Deployment
1. Click "View logs" to see deployment progress
2. When complete, you'll see: `app/main.py:app --host 0.0.0.0 --port $PORT`
3. Your backend URL will be: `https://sentiment-analysis-api-[yourname].herokuapp.com`

## Part 2: Frontend Deployment (Netlify)

### Step 1: Build Frontend for Production
```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build
```

This creates a `dist` folder with optimized production files.

### Step 2: Update API Endpoint
Before deploying, update the API endpoint in `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = 'https://sentiment-analysis-api-[yourname].herokuapp.com';
```

Rebuild:
```bash
npm run build
```

### Step 3: Deploy to Netlify
1. Go to https://app.netlify.com
2. Click "Add new site" → "Import an existing project"
3. Choose "GitHub"
4. Login with GitHub and authorize Netlify
5. Select your GitHub repository (or create new and push frontend folder)
6. Set build settings:
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
7. Click "Deploy"

### Step 4: Configure Environment Variables (if needed)
1. In Netlify dashboard: Settings → Build & deploy → Environment
2. No secrets needed for frontend deployment

## Part 3: Testing Deployment

### Test Backend Health
```bash
curl https://sentiment-analysis-api-[yourname].herokuapp.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-20T10:30:00.000000",
  "database": "connected"
}
```

### Test Frontend
1. Go to your Netlify URL: `https://sentiment-analysis-[yourname].netlify.app`
2. Upload a conversation thread
3. Verify analytics dashboard loads
4. Check predictions work

## Part 4: Alternative Deployment Options

### Render (Alternative to Heroku)
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
6. Add environment variables (same as Heroku)

### Vercel (Alternative to Netlify)
1. Go to https://vercel.com
2. Click "Add New..." → "Project"
3. Import GitHub repository (frontend folder)
4. Set build settings:
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Deploy

## Part 5: Troubleshooting

### Backend Issues
**Error: "Import pymongo could not be resolved"**
- This is a development-only issue. The dependencies are installed during deployment.

**Error: "Cannot connect to MongoDB"**
- Check MongoDB Atlas connection string in Config Vars
- Verify database user permissions
- Check IP whitelist includes `0.0.0.0/0`

**Error: "Port is not available"**
- Heroku automatically assigns PORT environment variable
- The `Procfile` correctly uses `$PORT`

### Frontend Issues
**Error: "Cannot access backend API"**
- Verify backend URL in `api.js` matches Heroku deployment URL
- Rebuild frontend after changing URL
- Check CORS is enabled in FastAPI (it is, by default)

**Error: "Blank page or 404"**
- Check build command runs correctly in Netlify logs
- Verify publish directory is `dist`
- Clear browser cache and redeploy

## Quick Reference URLs

After deployment, your URLs will be:

**Backend API**: `https://sentiment-analysis-api-[yourname].herokuapp.com`
- GET `/health` - Health check
- POST `/conversations/upload-thread` - Upload conversation
- GET `/conversations/{thread_id}` - Get conversation details
- GET `/analytics/overview` - Analytics overview
- POST `/predict/early-warning` - Escalation prediction

**Frontend**: `https://sentiment-analysis-[yourname].netlify.app`
- `/` - Dashboard with analytics
- `/upload` - Upload new conversation
- `/thread/{thread_id}` - View conversation details

## Monitoring Deployment

### Heroku Logs
```bash
heroku logs --tail -a sentiment-analysis-api-[yourname]
```

### Netlify Logs
View in Netlify dashboard → Deployments → Select deployment → Logs

## Redeploying After Updates

### Backend
1. Make changes to code
2. Commit and push to GitHub
3. Heroku automatically rebuilds if auto-deploy is enabled
4. Check logs: `heroku logs --tail`

### Frontend
1. Make changes to code
2. Commit and push to GitHub
3. Netlify automatically rebuilds
4. View logs in Netlify dashboard

## next Steps

1. Replace all `[yourname]` placeholders with actual values
2. Follow the deployment guide step by step
3. Share your deployment URLs:
   - **Backend**: Your Heroku URL
   - **Frontend**: Your Netlify URL

## Support

For issues:
1. Check the troubleshooting section above
2. Review deployment logs (Heroku/Netlify)
3. Verify all environment variables are set correctly
4. Ensure MongoDB Atlas user has correct permissions
