# Quick Deployment Guide (5 Steps)

Follow these exact steps to deploy your application in about 15 minutes.

## Step 1: Prepare for Deployment (2 minutes)

### Create .env file in backend directory:
```bash
cd backend
```

Create a file named `.env`:
```env
MONGODB_URL=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/sentiment_db
MONGODB_DB_NAME=sentiment_db
ENVIRONMENT=production
DEBUG=False
CORS_ORIGINS=["*"]
```

Replace YOUR_USERNAME, YOUR_PASSWORD, and YOUR_CLUSTER with your MongoDB Atlas credentials.

## Step 2: Push to GitHub (3 minutes)

```bash
# From project root directory
git init
git add .
git commit -m "Production-ready sentiment analysis system"

# Go to https://github.com/new and create a repository
# Then run (replace USERNAME and REPO):
git remote add origin https://github.com/USERNAME/REPO.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy Backend to Heroku (5 minutes)

### Option A: Using Heroku CLI
```bash
# Install Heroku CLI if not already installed

# Login to Heroku
heroku login

# Create app (replace APP_NAME with something unique)
heroku create sentiment-analysis-api-[yourname]

# Set environment variables
heroku config:set MONGODB_URL="mongodb+srv://username:password@cluster.mongodb.net/sentiment_db" \
                   MONGODB_DB_NAME=sentiment_db \
                   ENVIRONMENT=production \
                   DEBUG=False

# Deploy
git push heroku main

# Monitor deployment
heroku logs --tail
```

### Option B: Using Heroku Dashboard
1. Go to https://dashboard.heroku.com/apps
2. Click "Create new app"
3. Enter app name and select region
4. Go to Deploy tab → GitHub → authorize → select repository
5. Enable auto-deploy
6. Go to Settings → Config Vars → add MongoDB variables
7. Click "Deploy Branch" manually

**Your Backend URL**: `https://sentiment-analysis-api-[yourname].herokuapp.com`

## Step 4: Build and Deploy Frontend (3 minutes)

### Update API endpoint:
Edit `frontend/src/services/api.js`:
```javascript
const API_BASE_URL = 'https://sentiment-analysis-api-[yourname].herokuapp.com';
```

### Build:
```bash
cd frontend
npm install
npm run build
```

### Deploy to Netlify:
1. Go to https://app.netlify.com
2. Click "Add new site" → "Import an existing project"
3. Select GitHub → authorize → select repository (with frontend folder)
4. Build settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
5. Click Deploy

OR

1. Drag and drop the `frontend/dist` folder to Netlify

**Your Frontend URL**: `https://sentiment-analysis-[yourname].netlify.app`

## Step 5: Test Deployment (2 minutes)

### Test Backend:
```bash
curl https://sentiment-analysis-api-[yourname].herokuapp.com/health
```

Expected response:
```json
{"status":"healthy","timestamp":"2024-01-20T...","database":"connected"}
```

### Test Frontend:
1. Open `https://sentiment-analysis-[yourname].netlify.app`
2. Go to "Upload Conversation"
3. Try uploading a test conversation
4. Check Dashboard shows data
5. Test "Early Warning Prediction"

## Configuration Reference

### MongoDB Connection String Format:
```
mongodb+srv://USERNAME:PASSWORD@CLUSTER.mongodb.net/DATABASE_NAME?retryWrites=true&w=majority
```

### Environment Variables Needed:
- `MONGODB_URL` - Your MongoDB Atlas connection string
- `MONGODB_DB_NAME` - Database name (sentiment_db)
- `ENVIRONMENT` - production or development
- `DEBUG` - False for production
- `CORS_ORIGINS` - Allow all origins or specific URL

### Frontend Environment:
- Vite automatically uses `npm run build` for production
- API endpoint configured in `src/services/api.js`

## Troubleshooting

### "Cannot connect to MongoDB" Error
- Check MongoDB Atlas connection string
- Verify username/password are correct
- Go to MongoDB Atlas → Network Access → add IP address (0.0.0.0/0 for testing)

### "API not responding" from Frontend
- Check backend URL is correct in `api.js`
- Rebuild frontend if you changed the URL
- Check Heroku logs: `heroku logs --tail`

### "Port already in use" (Local testing)
- The app uses port 8000
- Change the port in `main.py` if needed
- Check if another server is running

### Frontend shows "Cannot GET /"
- This usually means wrong publish directory
- Should be `dist` not `build`
- Rebuild with `npm run build`

## Deployment Complete! 🎉

You now have:
```
✅ Backend API: https://sentiment-analysis-api-[yourname].herokuapp.com
✅ Frontend: https://sentiment-analysis-[yourname].netlify.app
✅ Database: MongoDB Atlas
```

### Features Available:
- ✨ Sentiment analysis for customer conversations
- 📊 Real-time analytics dashboard with 5 charts
- 🚨 Escalation detection with risk levels
- 🤖 Early warning ML classifier for proactive intervention
- 🔄 Historical sentiment tracking

### Next Steps:
1. Share your frontend URL with others
2. Upload sample conversations to populate analytics
3. Monitor the early warning predictions
4. Adjust escalation rules if needed

---

**Need Help?** See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed troubleshooting.
