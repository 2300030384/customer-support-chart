# Quick Start Guide 🚀

Get the sentiment analysis system up and running in 5 minutes!

## Step 1: MongoDB Atlas Setup (2 minutes)

### Option A: Using Free Tier ✅ RECOMMENDED
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up (free) or login
3. Create new project → "sentiment-analysis"
4. Build database:
   - Provider: AWS
   - Region: Closest to you
   - Tier: **M0 Sandbox** (Free)
5. Create database user:
   - Username: `admin`
   - Password: `StrongPassword123!`
   - Click "Create User"
6. Get connection string:
   - Go to "Connect" → "Drivers"
   - Copy the connection string
   - Should look like: `mongodb+srv://admin:StrongPassword123@cluster.mongodb.net/?retryWrites=true&w=majority`
7. Replace the placeholder database name with `sentiment_db`:
   - Final: `mongodb+srv://admin:StrongPassword123@cluster.mongodb.net/sentiment_db?retryWrites=true&w=majority`

### Option B: Local MongoDB
Skip MongoDB Atlas and use local MongoDB:
```
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=sentiment_db
```

---

## Step 2: Backend Setup (2 minutes)

### Windows Batch File (Fastest)
Create `backend\setup.bat`:
```batch
@echo off
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo Setup complete! Run: python -m uvicorn main:app --reload
pause
```

Run: Double-click `setup.bat`

### Manual Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (choose your OS)
## Windows:
venv\Scripts\activate
## Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your MongoDB URL
```

### Configure Environment
Edit `backend/.env`:
```
MONGODB_URL=mongodb+srv://admin:StrongPassword123@cluster.mongodb.net/sentiment_db
MONGODB_DB_NAME=sentiment_db
ENVIRONMENT=development
DEBUG=True
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### Run Backend
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend is running at: **http://localhost:8000**
📚 API docs: **http://localhost:8000/docs**

---

## Step 3: Frontend Setup (1 minute)

### Windows Batch File (Fastest)
Create `frontend\setup.bat`:
```batch
@echo off
npm install
npm run dev
```

Run: Double-click `setup.bat`

### Manual Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend is running at: **http://localhost:5173**

---

## Step 4: Test It! (Instant ✨)

### Option 1: Web UI (Easiest)
1. Open http://localhost:5173
2. Click **Upload** in navigation
3. Click **Load Sample** button
4. Click **Analyze Conversation**
5. View results on the next page!

### Option 2: API Test (curl)
```bash
curl -X POST http://localhost:8000/conversations/upload-thread \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "test_123",
    "platform": "Twitter",
    "messages": [
      {
        "speaker": "customer",
        "text": "Hi, I have an issue with my order",
        "timestamp": "2024-02-21T10:00:00Z"
      },
      {
        "speaker": "agent",
        "text": "I would be happy to help!",
        "timestamp": "2024-02-21T10:01:00Z"
      }
    ]
  }'
```

### Option 3: Swagger UI
1. Go to http://localhost:8000/docs
2. Try endpoints directly in the UI!

---

## 🎯 Main Features to Try

### Dashboard
Go to **http://localhost:5173** - See:
- ✅ Total conversations analyzed
- ✅ Escalation statistics
- ✅ Sentiment distribution
- ✅ Trends over time

### Upload Conversations
Click **Upload** - You can:
- ✅ Paste JSON conversations
- ✅ Load sample data
- ✅ See real-time analysis
- ✅ View escalation warnings

### View Details
Click on any conversation to see:
- ✅ Sentiment trajectory chart
- ✅ Message-by-message breakdown
- ✅ Early warning prediction
- ✅ Escalation reasons

---

## 📝 Sample Conversation JSON

```json
{
  "thread_id": "chat_abc123",
  "platform": "Twitter",
  "messages": [
    {
      "speaker": "customer",
      "text": "Hi, I ordered something 3 days ago and haven't received it",
      "timestamp": "2024-02-21T10:00:00Z"
    },
    {
      "speaker": "agent",
      "text": "Thank you for contacting us. Let me check your order status.",
      "timestamp": "2024-02-21T10:05:00Z"
    },
    {
      "speaker": "customer",
      "text": "This is ridiculous! Your shipping is terrible!",
      "timestamp": "2024-02-21T10:10:00Z"
    },
    {
      "speaker": "agent",
      "text": "I sincerely apologize for the delay. I'm investigating immediately.",
      "timestamp": "2024-02-21T10:15:00Z"
    },
    {
      "speaker": "customer",
      "text": "I want a full refund. This is unacceptable!",
      "timestamp": "2024-02-21T10:20:00Z"
    }
  ]
}
```

---

## 🔧 Configuration Reference

### Backend Environment Variables
```env
# Required
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/db_name
MONGODB_DB_NAME=sentiment_db

# Optional
ENVIRONMENT=development          # production/development
DEBUG=True                        # Enable debug mode
CORS_ORIGINS=["http://localhost:5173"]
SENTIMENT_MODEL=vader             # vader or huggingface
```

### API Endpoints Quick Reference
```
GET  /health                           → System health check
POST /conversations/upload-thread      → Analyze conversation
GET  /conversations                    → List all conversations
GET  /analytics/overview               → Analytics overview
GET  /analytics/funnel                 → Outcome distribution
GET  /analytics/escalation-playbook    → Insights & keywords
POST /predict/early-warning            → Predict escalation risk
```

---

## ⚡ Running Both Services (Easy Way)

### Option 1: Two Terminals
```bash
# Terminal 1
cd backend
python -m uvicorn main:app --reload

# Terminal 2
cd frontend
npm run dev
```

### Option 2: One Command (with npm-run-all)
In backend folder:
```bash
npm install npm-run-all
```

Create `package.json`:
```json
{
  "scripts": {
    "start:all": "npm-run-all --parallel start:backend start:frontend",
    "start:backend": "cd backend && python -m uvicorn main:app --reload",
    "start:frontend": "cd frontend && npm run dev"
  }
}
```

---

## 🐛 Common Issues & Fixes

### "Connection refused" - Backend
**Problem**: Can't connect to backend
**Solution**:
```bash
# Check if backend is running
curl http://localhost:8000/health

# Restart backend
python -m uvicorn main:app --reload --port 8000
```

### "Cannot find module" - Frontend
**Problem**: Missing dependencies
**Solution**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### "CORS error" - Frontend can't reach backend
**Problem**: CORS not configured
**Solution**: Check `.env` has:
```
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

### "MongoDB connection timeout"
**Problem**: Can't connect to MongoDB Atlas
**Solutions**:
1. Check IP whitelist in MongoDB Atlas (Network Access)
2. Verify connection string in .env
3. Ensure credentials are correct
4. Check internet connection
5. Try: `0.0.0.0/0` for development (NOT production!)

### "Port already in use"
**Problem**: Port 8000 or 5173 is taken
**Solution**:
```bash
# Use different port
python -m uvicorn main:app --reload --port 8001

# Or kill the process using the port
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :8000
kill -9 <PID>
```

---

## 📊 Next Steps: MongoDB Atlas Charts

Once you have data:
1. Go to MongoDB Atlas → Charts
2. Create dashboard
3. Add charts (see `MONGODB_ATLAS_SETUP.md` for aggregations)
4. Set up alerts for high escalation rates

---

## 🎯 Success Checklist

- ✅ Backend running on http://localhost:8000/docs
- ✅ Frontend running on http://localhost:5173
- ✅ MongoDB Atlas connection established
- ✅ Sample data uploaded and analyzed
- ✅ Dashboard shows statistics
- ✅ Sentiment trajectory chart displays
- ✅ Early warning prediction works

---

## 📚 Learn More

- **Backend Details**: See `README.md`
- **API Documentation**: http://localhost:8000/docs
- **Database Setup**: See `MONGODB_ATLAS_SETUP.md`
- **Source Code**: Check `backend/` and `frontend/` directories

---

## 🎉 You're Done!

Your sentiment analysis system is ready to use! 

**Next actions**:
1. ✅ Upload real conversations
2. ✅ View analytics on dashboard
3. ✅ Try early warning predictions
4. ✅ Set up MongoDB Charts for team
5. ✅ Configure alerts and monitoring

---

**Questions?** Check README.md for detailed documentation.
**Ready to deploy?** See deployment section in README.md

Happy analyzing! 🚀
