# System Architecture 🏗️

## Overview

Production-ready sentiment analysis platform with 3 main layers:

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React + Vite)                  │
│  Dashboard | Upload | Analysis | Charts | Early Warnings    │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/CORS
┌────────────────────────▼────────────────────────────────────┐
│                   API Layer (FastAPI)                        │
│  Routes: Conversations | Analytics | Predictions | Health   │
└────────────┬──────────────────────────────┬─────────────────┘
             │                              │
     ┌───────▼────────────┐      ┌──────────▼──────────┐
     │ Service Layer      │      │   ML Models Layer   │
     │                    │      │                     │
     │ • Sentiment        │      │ • Escalation        │
     │   Analyzer         │      │   Classifier        │
     │ • Escalation       │      │ • TF-IDF + Log      │
     │   Detector         │      │   Regression        │
     │ • Conversation     │      │ • Model Storage     │
     │   Service          │      │                     │
     │ • Analytics        │      └─────────────────────┘
     │   Service          │
     └───────┬────────────┘
             │
┌────────────▼────────────────────────────────────────────────┐
│              Data Layer (MongoDB Atlas)                      │
│  Collections: Conversations                                  │
│  Indexes: thread_id, platform, created_at, escalation...   │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Frontend Architecture

### Technology Stack
- **Framework**: React 18
- **Build Tool**: Vite 5
- **Styling**: TailwindCSS (utility-first)
- **HTTP Client**: Axios
- **Routing**: React Router v6
- **Charts**: Recharts
- **State Management**: React Hooks (useState, useEffect)

### Directory Structure
```
frontend/src/
├── pages/
│   ├── Dashboard.jsx         # Analytics & KPI dashboard
│   ├── UploadConversation.jsx # JSON input & analysis
│   └── ThreadDetails.jsx      # Individual conversation view
├── components/
│   ├── SentimentChart.jsx    # Reusable sentiment visualization
│   └── EscalationBanner.jsx  # Alert component
├── services/
│   └── api.js                # Axios API client
├── styles/
│   └── index.css             # Global & component styles
├── App.jsx                   # Main app component
└── main.jsx                  # Entry point
```

### Data Flow
1. **User uploads JSON** → UploadConversation.jsx validates
2. **API Call** → api.js sends to backend `/upload-thread`
3. **Response received** → Display results
4. **User navigates** → ThreadDetails shows sentiment trajectory
5. **Dashboard loads** → Fetches `/analytics/*` endpoints

### State Management Strategy
- **Local state**: Component-level with useState
- **API state**: Loading, error, data states
- **No Redux**: Hooks + Context sufficient for app size

---

## 2. API Layer (FastAPI)

### Route Structure
```
FastAPI App
├── /health                      [GET]   - System health
├── /conversations
│   ├── /upload-thread          [POST]  - Upload & analyze
│   ├/ (list all)               [GET]   - Get conversations
│   ├/ {thread_id}              [GET]   - Get specific
│   └/ {thread_id}/sentiment-trajectory  [GET]
├── /analytics
│   ├── /overview               [GET]   - KPI stats
│   ├── /funnel                 [GET]   - Outcomes
│   ├── /sentiment-distribution [GET]   - Labels
│   ├── /sentiment-over-time    [GET]   - Trends
│   └── /escalation-playbook    [GET]   - Insights
└── /predict
    └── /early-warning          [POST]  - ML prediction
```

### Request/Response Pattern

**Example: Upload Conversation**
```
POST /conversations/upload-thread

Request:
{
  "thread_id": "chat_123",
  "platform": "Twitter",
  "messages": [
    {
      "speaker": "customer",
      "text": "Hello...",
      "timestamp": "2024-02-21T10:00:00Z"
    }
  ]
}

Response:
{
  "thread_id": "chat_123",
  "message_count": 5,
  "sentiment_trajectory": [0.5, -0.2, -0.8, 0.1, -0.3],
  "overall_sentiment": -0.14,
  "escalation_detected": true,
  "escalation_reasons": ["Sharp sentiment drop detected"],
  "messages_with_sentiment": [...]
}
```

### Error Handling
- **400**: Validation errors (missing fields)
- **404**: Resource not found (thread_id)
- **500**: Server errors with detailed message
- **503**: Database disconnected

---

## 3. Service Layer

### 3.1 Sentiment Analyzer Service
```python
# sentiment_analyzer.py

analyze_turn(text: str) → (score: float, label: str, confidence: float)
├── VADER Model (default)
│   └── Fast, no dependencies, -1 to +1 score
└── HuggingFace Model (optional)
    └── More accurate, ~300MB download

analyze_conversation(messages: List[str]) → List[float]
└── Returns sentiment trajectory

calculate_overall_sentiment(scores: List[float]) → float
└── Average sentiment across conversation
```

**Sentiment Labels**:
- **Negative**: score < -0.1
- **Neutral**: -0.1 ≤ score ≤ 0.1
- **Positive**: score > 0.1

### 3.2 Escalation Detector Service
```python
# escalation_detector.py

Rules (OR logic - any match = escalation):
1. Consecutive Negatives
   └── 2+ messages with sentiment < -0.1

2. Sharp Sentiment Drop
   └── Drop > 0.6 between consecutive messages

3. Trigger Words
   └── Keywords: "refund", "cancel", "angry", "complaint", "terrible", etc.

4. Recent Negative Trend
   └── Last 3 messages avg sentiment < -0.3

detect_overall_escalation() → (bool, List[str])
└── Returns escalation flag + reasons
```

### 3.3 Conversation Service
```python
# conversation_service.py

process_conversation(conversation_in) → ConversationAnalysisResponse
├── 1. Sentiment Analysis
│   └── Analyze each message
├── 2. Escalation Detection
│   └── Flag messages + overall escalation
├── 3. MongoDB Storage
│   └── Insert/Update conversation
└── 4. Return Results
    └── Enriched conversation object

get_conversation(thread_id) → Conversation
├── Retrieve from MongoDB
└── Parse to Pydantic model
```

### 3.4 Analytics Service
```python
# analytics_service.py

get_overview() → AnalyticsOverview
├── Total conversations
├── Escalated count
├── Escalation rate %
└── Average sentiment

get_funnel() → FunnelData
├── Resolved count
├── Escalated count
└── Unresolved count

get_escalation_playbook() → EscalationPlaybook
├── Top negative keywords
├── Common failure patterns
├── Avg time before escalation
├── Agent response delays
└── Recommended actions

get_sentiment_over_time(days: int) → List[dict]
└── Daily sentiment trends
```

### 3.5 ML Early Warning Service
```python
# early_warning.py

Model: Pipeline(
  TfidfVectorizer(max_features=100, ngram_range=(1,2)),
  LogisticRegression()
)

predict_early_warning(customer_messages, thread_id) → EarlyWarningPrediction
├── Input: First 3 customer messages
├── Process:
│   ├── Convert to TF-IDF vectors
│   ├── Pass through classifier
│   ├── Get probability (0-1)
│   └── Determine risk level
└── Output: Risk score + reasons

Train: train_classifier_from_conversations(conversations)
└── Auto-trains on escalated vs normal conversations
```

---

## 4. Data Layer (MongoDB)

### Collection: conversations
```mongodb
{
  _id: ObjectId,
  thread_id: String,        // Unique key
  platform: String,
  created_at: ISODate,
  updated_at: ISODate,
  
  messages: [
    {
      message_id: String,
      speaker: String,      // "customer" or "agent"
      text: String,
      timestamp: ISODate,
      sentiment_score: Number,   // -1 to +1
      sentiment_label: String,   // "Positive", "Neutral", "Negative"
      escalation_flag: Boolean
    }
  ],
  
  overall_sentiment_trend: [Number],  // Array of scores
  overall_sentiment_label: String,
  escalation_detected: Boolean,
  escalation_reasons: [String],
  final_outcome: String      // "resolved", "escalated", "unresolved"
}
```

### Indexes
```mongodb
// For quick lookup
db.conversations.createIndex({ thread_id: 1 }, { unique: true })

// For filtering
db.conversations.createIndex({ platform: 1 })
db.conversations.createIndex({ created_at: -1 })
db.conversations.createIndex({ escalation_detected: 1 })
db.conversations.createIndex({ final_outcome: 1 })

// Compound index for common queries
db.conversations.createIndex({ escalation_detected: 1, created_at: -1 })
db.conversations.createIndex({ platform: 1, final_outcome: 1 })
```

---

## 5. Data Processing Pipeline

### Conversation Upload Flow
```
1. Frontend: User uploads JSON
   └── Validation: thread_id, messages array, speaker, text, timestamp

2. Backend: POST /upload-thread
   ├── Parse ConversationIn
   ├── Sentiment Analysis (per message)
   ├── Escalation Detection (per message + overall)
   ├── MongoDB Storage
   └── Response with enriched data

3. Database: Store document
   ├── Calculate indexes
   ├── Update created_at, updated_at
   └── Ready for queries

4. Frontend: Display results
   ├── Show sentiment trajectory
   ├── Display escalation warnings
   ├── Navigate to details page
   └── Update dashboard
```

### Analytics Query Flow
```
Frontend: User views dashboard
  ├── Load /analytics/overview
  ├── Load /analytics/funnel
  ├── Load /analytics/sentiment-distribution
  ├── Load /analytics/sentiment-over-time
  └── Load /analytics/escalation-playbook

Backend: Aggregate data
  ├── Group by field (outcome, label, date)
  ├── Count occurrences
  ├── Calculate averages
  ├── Sort + limit
  └── Return formatted JSON

Frontend: Visualize
  ├── KPI cards
  ├── Bar charts
  ├── Line charts
  ├── Pie charts
  └── Table lists
```

---

## 6. Communication Protocols

### Frontend ↔ Backend
- **Protocol**: HTTP/REST
- **Data Format**: JSON
- **Authentication**: None (for now; add JWT/OAuth for production)
- **CORS**: Configured for localhost development
- **Timeout**: Default 30s (Axios)

### Backend ↔ MongoDB
- **Protocol**: MongoDB Wire Protocol
- **Connection Pool**: PyMongo handles
- **Retry Logic**: Built-in reconnection
- **Timeout**: 10s connect, 5s select

### Configuration
```python
# Backend CORS
CORSMiddleware(
  allow_origins=["http://localhost:5173"],
  allow_methods=["*"],
  allow_headers=["*"]
)

# Axios timeout
axios.defaults.timeout = 30000

# MongoDB timeout
client = MongoClient(
  serverSelectionTimeoutMS=5000,
  connectTimeoutMS=10000
)
```

---

## 7. Error Handling & Logging

### Logging Strategy
```python
# All modules log to console
logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Key logs
✓ = Success (connections, data processing)
✗ = Error (exceptions, failed connections)
⚠ = Warning (missing models, fallbacks)
```

### Exception Handling
```
Frontend Errors:
├── Network errors → Show toast message
├── Validation errors → Form feedback
└── Server errors → Error banner + retry

Backend Errors:
├── Validation → HTTPException 400
├── Not found → HTTPException 404
├── Server → HTTPException 500 + detailed message
└── Database → HTTPException 503 + retry logic

Global Handler:
└── Catch-all for unhandled exceptions
```

---

## 8. Security Considerations

### Current (Development)
- No authentication
- CORS allows localhost
- MongoDB requires credentials
- Sensitive env vars in .env

### Production Recommendations
1. **Authentication**: JWT tokens
2. **API Keys**: For external services
3. **Rate Limiting**: Prevent abuse
4. **Input Validation**: Pydantic models
5. **HTTPS**: Force SSL/TLS
6. **MongoDB Atlas**: IP whitelist, encrypted connections
7. **Environment**: Secure env var management
8. **Logging**: Don't log sensitive data

---

## 9. Performance Optimization

### Database
- **Indexes**: Created on startup
- **Query optimization**: Use aggregation pipelines
- **Connection pooling**: PyMongo handles
- **Caching**: Could add Redis for popular queries

### Backend
- **VADER**: < 10ms per message
- **Batch processing**: Process multiple messages sequentially
- **Async routes**: Could add async for I/O operations

### Frontend
- **Code splitting**: Vite auto-splits by route
- **Lazy loading**: Components load on demand
- **Recharts optimization**: Limits chart points for performance

### Best Practices
```python
# Efficient MongoDB queries
db.conversations.find(
  {"escalation_detected": True},
  {"messages": {"$slice": -10}}  # Last 10 messages only
)

# Project only needed fields
db.conversations.find({}, {"thread_id": 1, "escalation_detected": 1})

# Use aggregation for complex queries
db.conversations.aggregate([
  { $match: {"created_at": {"$gte": start_date}} },
  { $group: {"_id": "$platform", "count": {"$sum": 1}} }
])
```

---

## 10. Deployment Architecture

### Local Development
```
Your Machine
├── Backend (port 8000)
│   └── Python + FastAPI + Uvicorn
├── Frontend (port 5173)
│   └── Node + Vite + React
└── MongoDB Atlas (cloud)
    └── Managed by MongoDB Inc.
```

### Production Deployment
```
Cloud Provider (AWS, GCP, Azure)
├── Frontend (Netlify/Vercel/S3)
│   ├── Static CDN
│   └── Auto-scaling
├── Backend (Docker + K8s or Platform)
│   ├── Container orchestration
│   └── Auto-scaling + load balancing
└── MongoDB Atlas
    ├── Replica set
    ├── Automated backups
    └── Enterprise monitoring
```

---

## 11. System Constraints & Limits

| Constraint | Value | Notes |
|-----------|-------|-------|
| Max messages per conversation | 1000 | API design limit |
| Max message text length | 5000 chars | Validation |
| Sentiment score precision | 2 decimals | Float |
| API response timeout | 30s | Client-side |
| MongoDB connection timeout | 10s | Server-side |
| Request body size | 10 MB | FastAPI default |
| Concurrent connections | Limited by tier | MongoDB Atlas |

---

## 12. Future Enhancements

### Short Term
- [ ] User authentication (JWT)
- [ ] Conversation search
- [ ] Export to CSV/PDF
- [ ] Real-time WebSocket updates
- [ ] Fine-tuned sentiment models

### Medium Term
- [ ] Multi-language support
- [ ] Custom escalation rules
- [ ] Agent performance metrics
- [ ] Knowledge base integration
- [ ] Auto-suggested responses

### Long Term
- [ ] Sentiment prediction
- [ ] Conversation clustering
- [ ] Topic extraction
- [ ] Chatbot integration
- [ ] Real-time monitoring dashboard

---

This architecture provides a solid, scalable foundation for the sentiment analysis system!
