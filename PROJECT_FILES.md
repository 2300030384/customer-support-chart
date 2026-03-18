# Project File Structure - Complete List

## Root Directory
```
sentiment-analysis-project/
├── backend/                          # FastAPI backend
├── frontend/                         # React frontend
├── README.md                         # Project overview
├── QUICKSTART.md                     # Quick start guide
├── DEPLOYMENT.md                     # Detailed deployment guide
├── DEPLOYMENT_STATUS.md              # Status of fixes and ready check
├── QUICK_DEPLOY.md                   # 5-step quick deployment
└── ARCHITECTURE.md                   # Architecture documentation
```

## Backend Files

### Configuration & Main
- `backend/main.py` - FastAPI application entry point with lifespan management
- `backend/requirements.txt` - Python package dependencies
- `backend/.env.example` - Example environment variables
- `.env` (create manually) - Actual environment variables for deployment
- `backend/Procfile` - Heroku/Render deployment configuration
- `backend/runtime.txt` - Python version specification (3.11.7)
- `backend/.gitignore` - Git exclusion rules

### Database (`backend/app/database/`)
- `connection.py` - MongoDB connection management (synchronous PyMongo)
  - `connect_to_mongo()` - Initialize connection
  - `close_mongo_connection()` - Graceful shutdown
  - `get_database()` - Get database instance
  - `create_indexes()` - Create MongoDB indexes

### Models (`backend/app/models/`)
- `schemas.py` - Pydantic data validation models (15+ models)
  - ConversationIn, Conversation, Message
  - AnalyticsOverview, SentimentAnalysisResult
  - EarlyWarningPrediction, EscalationPlaybook
  - FunnelData, NegativeKeyword, FailurePattern
  - And more...

### Services (`backend/app/services/`)
- `sentiment_analyzer.py` - VADER sentiment analysis
  - `analyze_turn()` - Analyze single message
  - `analyze_conversation()` - Analyze entire conversation
  - `calculate_overall_sentiment()` - Calculate average sentiment
  - `get_sentiment_label()` - Convert score to label

- `escalation_detector.py` - Multi-rule escalation detection
  - `detect_overall_escalation()` - Overall escalation check
  - `detect_escalation_per_message()` - Per-message escalation
  - `contains_trigger_words()` - Check for negative keywords
  - 4 detection rules: consecutive negatives, sentiment drop, trigger words, recent trend

- `conversation_service.py` - Orchestrates sentiment + escalation + storage
  - `process_conversation()` - Main processing pipeline
  - `get_conversation()` - Retrieve by thread_id
  - `get_all_conversations()` - Get all conversations
  - `get_sentiment_trajectory()` - Get sentiment trend

- `analytics_service.py` - Analytics and insights
  - `get_overview()` - Dashboard overview metrics
  - `get_funnel()` - Conversation outcomes
  - `get_sentiment_distribution()` - Sentiment distribution chart
  - `get_escalation_playbook()` - Escalation insights
  - `get_sentiment_over_time()` - Time-series sentiment

- `early_warning.py` - ML classifier for escalation prediction
  - `EarlyWarningClassifier` - TF-IDF + Logistic Regression
  - `predict_early_warning()` - Predict escalation risk
  - `train_classifier_from_conversations()` - Train on data

### Routes (`backend/app/routes/`)
- `health.py` - Health check endpoints
  - `GET /health` - Verify system status

- `conversations.py` - Conversation management endpoints
  - `POST /conversations/upload-thread` - Upload conversation
  - `GET /conversations` - Get all conversations
  - `GET /conversations/{thread_id}` - Get specific conversation
  - `GET /conversations/{thread_id}/sentiment-trajectory` - Get trend

- `analytics.py` - Analytics endpoints
  - `GET /analytics/overview` - Overview metrics
  - `GET /analytics/funnel` - Funnel data
  - `GET /analytics/sentiment-distribution` - Distribution
  - `GET /analytics/sentiment-over-time` - Trends
  - `GET /analytics/escalation-playbook` - Playbook

- `predictions.py` - ML prediction endpoints
  - `POST /predict/early-warning` - Escalation prediction

### Configuration
- `backend/app/config.py` - Settings management with pydantic-settings
  - MongoDB configuration
  - CORS settings
  - API configuration

### ML Models
- `backend/ml_models/escalation_classifier.pkl` - Trained classifier (generated at runtime)

## Frontend Files

### Configuration & Main
- `frontend/package.json` - Node package dependencies
- `frontend/vite.config.js` - Vite build configuration
- `frontend/tailwind.config.js` - TailwindCSS configuration
- `frontend/postcss.config.js` - PostCSS configuration
- `frontend/index.html` - HTML entry point
- `frontend/.gitignore` - Git exclusion rules

### Styles
- `frontend/src/styles/index.css` - Global styles with TailwindCSS directives

### Components
- `frontend/src/App.jsx` - Main app component with routing
- `frontend/src/main.jsx` - React entry point

### Pages/Views
- `frontend/src/pages/Dashboard.jsx` - Analytics dashboard
  - 4 KPI cards (Total, Escalated, Unresolved, Resolved)
  - 5 charts (Bar, Pie, Line, Histogram, Time series)

- `frontend/src/pages/UploadConversation.jsx` - Upload new conversation
  - JSON input form with validation
  - Sample conversation loader
  - Real-time analysis display

- `frontend/src/pages/ThreadDetails.jsx` - View conversation details
  - Sentiment trajectory visualization
  - Early warning prediction
  - Message breakdown
  - Escalation analysis

### Services
- `frontend/src/services/api.js` - Axios API client
  - conversationAPI endpoints
  - analyticsAPI endpoints
  - predictionAPI endpoints
  - healthAPI endpoint

## Documentation Files

### Main Documentation
- `README.md` - Project overview and key features
- `QUICKSTART.md` - Software stack and quick start
- `ARCHITECTURE.md` - System architecture and data flow
- `API_REFERENCE.md` - Complete API endpoint documentation
- `TESTING_GUIDE.md` - Testing instructions
- `MONGODB_ATLAS_SETUP.md` - MongoDB Atlas setup guide

### Deployment Documentation
- `DEPLOYMENT.md` - Comprehensive deployment guide (5 parts)
- `DEPLOYMENT_STATUS.md` - Status of all fixes and ready check
- `QUICK_DEPLOY.md` - 5-step quick deployment guide

## Database Schema

### Conversations Collection
```javascript
{
  _id: ObjectId,
  thread_id: string (unique index),
  platform: string (index),
  messages: [
    {
      message_id: string,
      speaker: "customer" | "agent",
      text: string,
      timestamp: datetime,
      sentiment_score: number (-1 to 1),
      sentiment_label: "Positive" | "Neutral" | "Negative",
      escalation_flag: boolean
    }
  ],
  overall_sentiment_trend: [number],
  overall_sentiment_label: string,
  escalation_detected: boolean (index),
  escalation_reasons: [string],
  final_outcome: "resolved" | "escalated" | "unresolved",
  created_at: datetime (index),
  updated_at: datetime
}
```

## Dependencies Summary

### Backend (requirements.txt)
- fastapi (0.104.1) - Web framework
- uvicorn (0.24.0) - ASGI server
- pymongo (4.6.0) - MongoDB driver (synchronous)
- pydantic (2.5.0) - Data validation
- python-dotenv (1.0.0) - Environment variables
- transformers (4.35.0) - HuggingFace models
- torch (2.1.0) - PyTorch (for transformers)
- vaderSentiment (3.3.2) - VADER sentiment analysis
- scikit-learn (1.3.2) - ML algorithms
- pandas (2.1.1) - Data manipulation
- numpy (1.26.0) - Numerical computing

### Frontend (package.json)
- react (^18.2.0) - UI framework
- vite (^5.0.0) - Build tool
- tailwindcss (^3.3.0) - Styling
- recharts (^2.10.0) - Charts
- axios (^1.6.0) - HTTP client
- react-router-dom (^6.18.0) - Routing

## Total Project Statistics
- Backend files: 12 Python files
- Frontend files: 8 JavaScript/JSX files
- Configuration files: 6 files
- Documentation: 9 markdown files
- Total files: ~40+ files
- Code lines: ~5000+ lines of Python + JavaScript
- Documentation: ~10000+ words

## API Endpoints Summary

### Health (1 endpoint)
- GET /health

### Conversations (4 endpoints)
- POST /conversations/upload-thread
- GET /conversations
- GET /conversations/{thread_id}
- GET /conversations/{thread_id}/sentiment-trajectory

### Analytics (5 endpoints)
- GET /analytics/overview
- GET /analytics/funnel
- GET /analytics/sentiment-distribution
- GET /analytics/sentiment-over-time
- GET /analytics/escalation-playbook

### Predictions (1 endpoint)
- POST /predict/early-warning

**Total: 11 API endpoints**

## Status ✓

All files have been created and are ready for deployment:
- ✅ Backend services completed
- ✅ Frontend components completed
- ✅ API routes implemented
- ✅ Database schema designed
- ✅ Async/sync issues fixed
- ✅ Deployment files created
- ✅ Comprehensive documentation provided
- ✅ Ready for production deployment

---

*Last updated: After all async/sync corrections and deployment file creation*

*Next step: Follow QUICK_DEPLOY.md or DEPLOYMENT.md for deployment*
