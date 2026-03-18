# Sentiment Analysis in Customer Support Chats 🎯

A production-ready AI-powered system for analyzing sentiment and detecting escalations in customer support conversations.

## 🚀 Features

### Backend (FastAPI)
- ✅ Real-time sentiment analysis (VADER & HuggingFace models)
- ✅ Automatic escalation detection with multi-rule engine
- ✅ ML-powered early warning predictions (TF-IDF + Logistic Regression)
- ✅ Comprehensive analytics and reporting
- ✅ MongoDB integration with optimized indexes
- ✅ CORS support for frontend integration
- ✅ Health check and monitoring endpoints

### Frontend (React + Vite)
- ✅ Modern dark-themed dashboard UI
- ✅ Real-time conversation upload with JSON validation
- ✅ Interactive sentiment trajectory visualization
- ✅ Advanced analytics with Recharts
- ✅ Early warning risk prediction display
- ✅ Sample data loader for testing
- ✅ Responsive design (mobile-friendly)

### Analytics
- ✅ Conversation overview statistics
- ✅ Funnel analysis (Resolved → Escalated → Unresolved)
- ✅ Sentiment distribution charts
- ✅ Escalation patterns and trends
- ✅ Negative keyword extraction
- ✅ Agent response time analysis
- ✅ Failure pattern identification

---

## 📋 Project Structure

```
hackathon-project/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── models/
│   │   │   └── schemas.py     # Pydantic models
│   │   ├── services/
│   │   │   ├── sentiment_analyzer.py    # Sentiment analysis
│   │   │   ├── escalation_detector.py   # Escalation detection
│   │   │   ├── conversation_service.py  # Core orchestration
│   │   │   ├── analytics_service.py     # Analytics logic
│   │   │   └── early_warning.py         # ML predictions
│   │   ├── routes/
│   │   │   ├── health.py      # Health checks
│   │   │   ├── conversations.py   # Conversation endpoints
│   │   │   ├── analytics.py    # Analytics endpoints
│   │   │   └── predictions.py  # ML endpoints
│   │   ├── database/
│   │   │   └── connection.py   # MongoDB connection
│   │   └── config.py           # Configuration
│   ├── main.py                 # FastAPI app
│   ├── requirements.txt        # Dependencies
│   ├── .env.example            # Environment template
│   └── ml_models/              # ML model storage
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx       # Main dashboard
│   │   │   ├── UploadConversation.jsx   # Upload page
│   │   │   └── ThreadDetails.jsx   # Details page
│   │   ├── components/             # Reusable components
│   │   ├── services/
│   │   │   └── api.js              # API client
│   │   ├── styles/
│   │   │   └── index.css           # Global styles
│   │   └── App.jsx                 # Main app
│   ├── vite.config.js              # Vite config
│   ├── tailwind.config.js          # Tailwind config
│   ├── package.json                # Dependencies
│   └── index.html                  # HTML entry
│
├── MONGODB_ATLAS_SETUP.md     # MongoDB configuration guide
└── README.md                  # This file
```

---

## 🔧 Installation & Setup

### Prerequisites
- **Python 3.9+**
- **Node.js 18+**
- **MongoDB Atlas** (free tier available)
- **pip** and **npm**

### Backend Setup

1. **Clone/Extract and navigate to backend**:
   ```bash
   cd backend
   ```

2. **Create .env file**:
   ```bash
   cp .env.example .env
   ```

3. **Edit .env with your MongoDB connection**:
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/sentiment_db
   MONGODB_DB_NAME=sentiment_db
   ENVIRONMENT=development
   DEBUG=True
   CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
   ```

4. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or
   source venv/bin/activate      # Mac/Linux
   ```

5. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Run backend**:
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at: `http://localhost:8000`
   API docs: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend**:
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run development server**:
   ```bash
   npm run dev
   ```

   Frontend will be available at: `http://localhost:5173`

4. **Build for production**:
   ```bash
   npm run build
   ```

---

## 📡 API Endpoints

### Health & Status
- `GET /health` - Check system health and database connection
- `GET /` - Root endpoint with API info

### Conversations
- `POST /conversations/upload-thread` - Upload and analyze conversation
- `GET /conversations` - Get all conversations
- `GET /conversations/{thread_id}` - Get specific conversation
- `GET /conversations/{thread_id}/sentiment-trajectory` - Get sentiment over time

### Analytics
- `GET /analytics/overview` - Overview statistics
- `GET /analytics/funnel` - Conversation outcomes funnel
- `GET /analytics/sentiment-distribution` - Sentiment label distribution
- `GET /analytics/sentiment-over-time` - Sentiment trends (time-based)
- `GET /analytics/escalation-playbook` - Escalation insights & recommendations

### ML Predictions
- `POST /predict/early-warning` - Predict escalation risk from first 3 messages

---

## 🧪 Testing with Sample Data

### Using Frontend
1. Navigate to "Upload" page
2. Click "Load Sample" button
3. Click "Analyze Conversation"
4. View results and sentiment trajectory

### Using API (curl/Postman)
```bash
curl -X POST http://localhost:8000/conversations/upload-thread \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "chat_12345",
    "platform": "Twitter",
    "messages": [
      {
        "speaker": "customer",
        "text": "Hi, I have an issue with my order",
        "timestamp": "2024-02-21T10:00:00Z"
      },
      {
        "speaker": "agent",
        "text": "I would be happy to help. What is the issue?",
        "timestamp": "2024-02-21T10:01:00Z"
      }
    ]
  }'
```

---

## 📊 Data/Conversation JSON Format

```json
{
  "thread_id": "unique_conversation_id",
  "platform": "Twitter",
  "messages": [
    {
      "speaker": "customer",
      "text": "The message content",
      "timestamp": "2024-02-21T10:00:00Z"
    },
    {
      "speaker": "agent",
      "text": "Agent response",
      "timestamp": "2024-02-21T10:01:00Z"
    }
  ]
}
```

---

## 🤖 Sentiment Analysis

### Models Supported
1. **VADER** (Default - Lightweight)
   - No external downloads needed
   - Fast inference
   - Good for general sentiment
   - Score range: -1 to +1

2. **HuggingFace** (Advanced)
   - More accurate
   - Requires model download (~300MB)
   - Slower inference
   - Set `sentiment_model: huggingface` in .env

### Labels
- **Negative**: Score < -0.1
- **Neutral**: Score between -0.1 and 0.1
- **Positive**: Score > 0.1

---

## ⚠️ Escalation Detection Rules

The system flags escalation when:

1. **Two consecutive negative messages** detected
2. **Sharp sentiment drop** (> 0.6 decrease between messages)
3. **Trigger words** found: "refund", "cancel", "angry", "complaint", "not happy", "terrible", "hate", "lawsuit", etc.
4. **Recent negative trend**: Last 3 messages with avg sentiment < -0.3

---

## 🎯 ML Early Warning Classifier

**Model**: TF-IDF + Logistic Regression
**Input**: First 3 customer messages
**Output**: Escalation probability (0-1) + confidence score

**Usage**:
```bash
curl -X POST http://localhost:8000/predict/early-warning \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "chat_123",
    "customer_messages": [
      "Hi, I have a problem",
      "Its been 2 days unresolved",
      "I want a refund now!"
    ]
  }'
```

**Response**:
```json
{
  "thread_id": "chat_123",
  "escalation_probability": 0.87,
  "confidence": 0.75,
  "risk_level": "high",
  "warning_reasons": [
    "Contains keywords: refund",
    "Negative sentiment detected early"
  ]
}
```

---

## 📈 Analytics & Insights

### Overview Metrics
- Total conversations processed
- Number of escalated conversations
- Escalation rate percentage
- Average sentiment across all conversations

### Funnel Analysis
- **Resolved**: Conversations successfully completed
- **Escalated**: Conversations that escalated
- **Unresolved**: Conversations still pending

### Sentiment Trends
- Time-series sentiment tracking
- Distribution of positive/neutral/negative messages
- Sentiment trajectory per conversation

### Escalation Insights
- Top negative keywords
- Common failure patterns
- Average time before escalation
- Agent response delays
- Actionable recommendations

---

## 🗄️ MongoDB Schema

### Conversations Collection

```javascript
{
  _id: ObjectId,
  thread_id: String (unique),
  platform: String,
  created_at: Date,
  updated_at: Date,
  messages: [
    {
      message_id: String,
      speaker: String ("customer" | "agent"),
      text: String,
      timestamp: Date,
      sentiment_score: Number (-1 to 1),
      sentiment_label: String ("Positive" | "Neutral" | "Negative"),
      escalation_flag: Boolean
    }
  ],
  overall_sentiment_trend: [Number],
  overall_sentiment_label: String,
  escalation_detected: Boolean,
  escalation_reasons: [String],
  final_outcome: String ("resolved" | "escalated" | "unresolved")
}
```

### Indexes Created
- **Unique**: `thread_id`
- **Regular**: `platform`, `created_at`, `escalation_detected`, `final_outcome`

---

## 📊 MongoDB Atlas Charts

Detailed configuration for 7 analytics dashboards in `MONGODB_ATLAS_SETUP.md`:
1. Funnel chart (conversation outcomes)
2. Sentiment trajectory line chart
3. Escalation rate pie chart
4. Sentiment distribution histogram
5. Escalation reasons analysis
6. Time series sentiment trends
7. Interactive filters by platform, date, escalation status

---

## 🎨 Frontend Features

### Dashboard
- 4 KPI cards (Total conversations, Escalated, Escalation rate, Avg sentiment)
- Bar chart for conversation outcomes
- Pie chart for sentiment distribution
- Line chart for sentiment trends over 30 days
- Escalation insights panel with keywords and recommendations

### Upload Page
- Paste JSON format conversations
- Load sample data button
- Real-time JSON validation
- Shows analysis results after upload
- Displays sentiment distribution and escalation warnings
- Auto-navigate to conversation details on success

### Thread Details Page
- Full conversation analysis
- 4 metric cards
- Sentiment trajectory visualization with escalation points highlighted
- Early warning risk prediction with probability
- Message-by-message breakdown with sentiment labels
- Escalation alerts

---

## 🔐 Environment Variables

```env
# Database
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/db_name
MONGODB_DB_NAME=sentiment_db

# Application
ENVIRONMENT=production           # development or production
DEBUG=False

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Sentiment Model
SENTIMENT_MODEL=vader           # vader or huggingface
```

---

## 📦 Dependencies

### Backend
- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **pymongo**: MongoDB driver
- **pydantic**: Data validation
- **vaderSentiment**: Sentiment analysis
- **transformers**: HuggingFace models (optional)
- **scikit-learn**: ML (TF-IDF, Logistic Regression)
- **numpy**, **pandas**: Data processing

### Frontend
- **react**: UI framework
- **react-router-dom**: Routing
- **axios**: HTTP client
- **recharts**: Charts & visualization
- **tailwindcss**: Styling
- **vite**: Build tool

---

## 🚀 Production Deployment

### Backend (Docker)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (Netlify/Vercel)
```bash
npm run build
# Deploy dist/ folder
```

### MongoDB Atlas
- Use cluster with replication
- Enable backups
- Set up IP whitelist for production
- Monitor with Atlas charts and alerts

---

## 🐛 Troubleshooting

### Backend won't connect to MongoDB
- Check connection string in .env
- Verify MongoDB Atlas IP whitelist
- Ensure credentials are correct
- Check network connectivity

### Frontend can't connect to backend
- Verify backend is running on port 8000
- Check CORS_ORIGINS includes frontend URL
- Ensure API base URL is correct in api.js
- Check browser console for CORS errors

### Low sentiment analysis accuracy
- Try switching from VADER to HuggingFace model
- Ensure messages are in English
- Check for special characters or emojis
- Consider fine-tuning on domain-specific data

### ML predictions always neutral
- Ensure training data exists in database
- Check if sufficient escalated conversations exist
- Verify early_warning.py classifier initialization
- Check customer message quality

---

## 📝 Logging

Logs are displayed in console with format:
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

To save logs to file, modify `main.py`:
```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
```

---

## 🤝 Contributing

To extend this project:

1. **Add new sentiment models**: Extend `sentiment_analyzer.py`
2. **Add escalation rules**: Update `escalation_detector.py`
3. **Add analytics**: New methods in `analytics_service.py`
4. **Add frontend pages**: Create in `src/pages/`
5. **Improve ML**: Retraining and tunning scripts in `ml_models/`

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

## 📞 Support

For issues, questions, or feedback:
1. Check the documentation files
2. Review API docs at `/docs` when backend is running
3. Check browser console for frontend errors
4. Review backend logs in terminal

---

## 🎯 Success Metrics

Track these KPIs to measure system effectiveness:
- Escalation rate (target: < 20%)
- Average sentiment (target: > 0.2)
- False positive escalations discovered
- Average time before escalation detection (target: < 5 messages)
- User satisfaction with predictions

---

**Build date**: February 21, 2026
**Version**: 1.0.0
**Status**: Production-ready ✅
