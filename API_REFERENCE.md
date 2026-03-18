# API Reference 📚

Complete API documentation for all endpoints.

---

## Base URL
```
http://localhost:8000
```

## Authentication
None (add JWT for production)

## Response Format
All responses are JSON

---

## Health & Status Endpoints

### Health Check
```
GET /health
```

**Description**: Check system health and database connection

**Response** (200):
```json
{
  "status": "healthy",
  "timestamp": "2024-02-21T10:00:00.000Z",
  "database": "connected"
}
```

**Error** (503):
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "error": "Connection timeout"
}
```

---

### Root Info
```
GET /
```

**Description**: Get API information and available endpoints

**Response** (200):
```json
{
  "message": "Sentiment Analysis API for Customer Support",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "upload": "/upload-thread",
    "analytics": "/analytics/overview",
    "docs": "/docs"
  }
}
```

---

## Conversation Endpoints

### Upload & Analyze Conversation
```
POST /conversations/upload-thread
```

**Description**: Upload a conversation and perform sentiment analysis + escalation detection

**Request**:
```json
{
  "thread_id": "string (required)",
  "platform": "string (optional, default: 'unknown')",
  "messages": [
    {
      "speaker": "customer | agent (required)",
      "text": "string (required)",
      "timestamp": "ISO 8601 datetime (required)"
    }
  ]
}
```

**Example**:
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
      }
    ]
  }'
```

**Response** (200):
```json
{
  "thread_id": "chat_12345",
  "message_count": 5,
  "sentiment_trajectory": [0.5, -0.2, -0.8, 0.1, -0.3],
  "overall_sentiment": -0.14,
  "escalation_detected": true,
  "escalation_reasons": [
    "Sharp sentiment drop detected",
    "Trigger words found: refund"
  ],
  "messages_with_sentiment": [
    {
      "message_id": "msg_1",
      "sentiment_score": 0.5,
      "sentiment_label": "Positive",
      "confidence": 0.85
    }
  ]
}
```

**Errors**:
- 400: Validation error
- 422: Invalid schema
- 500: Processing error

---

### Get All Conversations
```
GET /conversations?limit=100
```

**Description**: Retrieve all conversations with optional limit

**Query Parameters**:
- `limit` (int, optional): Number of conversations to return (1-1000, default: 100)

**Example**:
```bash
curl -X GET "http://localhost:8000/conversations?limit=50"
```

**Response** (200):
```json
{
  "total": 10,
  "conversations": [
    {
      "id": "507f1f77bcf86cd799439011",
      "thread_id": "chat_12345",
      "platform": "Twitter",
      "created_at": "2024-02-21T10:00:00Z",
      "messages": [],
      "escalation_detected": true,
      "escalation_reasons": [],
      "overall_sentiment_trend": [0.5, -0.2],
      "final_outcome": "escalated"
    }
  ]
}
```

**Errors**:
- 500: Database error

---

### Get Specific Conversation
```
GET /conversations/{thread_id}
```

**Description**: Retrieve a specific conversation by thread_id

**Path Parameters**:
- `thread_id` (string, required): Unique conversation ID

**Example**:
```bash
curl -X GET "http://localhost:8000/conversations/chat_12345"
```

**Response** (200):
```json
{
  "id": "507f1f77bcf86cd799439011",
  "thread_id": "chat_12345",
  "platform": "Twitter",
  "created_at": "2024-02-21T10:00:00Z",
  "updated_at": "2024-02-21T10:30:00Z",
  "messages": [
    {
      "message_id": "msg_1",
      "speaker": "customer",
      "text": "Hello, I have an issue",
      "timestamp": "2024-02-21T10:00:00Z",
      "sentiment_score": 0.5,
      "sentiment_label": "Positive",
      "escalation_flag": false
    }
  ],
  "overall_sentiment_trend": [0.5, -0.2, -0.8],
  "overall_sentiment_label": "Negative",
  "escalation_detected": true,
  "escalation_reasons": ["Sharp sentiment drop detected"],
  "final_outcome": "escalated"
}
```

**Errors**:
- 404: Conversation not found
- 500: Database error

---

### Get Sentiment Trajectory
```
GET /conversations/{thread_id}/sentiment-trajectory
```

**Description**: Get sentiment scores over message progression for visualization

**Path Parameters**:
- `thread_id` (string, required): Unique conversation ID

**Example**:
```bash
curl -X GET "http://localhost:8000/conversations/chat_12345/sentiment-trajectory"
```

**Response** (200):
```json
{
  "thread_id": "chat_12345",
  "trajectory": [
    {
      "turn": 1,
      "sentiment": 0.5,
      "speaker": "customer",
      "escalation_point": false
    },
    {
      "turn": 2,
      "sentiment": -0.2,
      "speaker": "agent",
      "escalation_point": false
    },
    {
      "turn": 3,
      "sentiment": -0.8,
      "speaker": "customer",
      "escalation_point": true
    }
  ]
}
```

**Errors**:
- 404: Conversation not found
- 500: Database error

---

## Analytics Endpoints

### Overview Statistics
```
GET /analytics/overview
```

**Description**: Get high-level analytics statistics

**Example**:
```bash
curl -X GET "http://localhost:8000/analytics/overview"
```

**Response** (200):
```json
{
  "total_threads": 45,
  "escalated_threads": 12,
  "unresolved_threads": 8,
  "resolved_threads": 25,
  "escalation_rate": 26.67,
  "avg_sentiment": 0.145
}
```

---

### Funnel Data
```
GET /analytics/funnel
```

**Description**: Get conversation outcome distribution

**Example**:
```bash
curl -X GET "http://localhost:8000/analytics/funnel"
```

**Response** (200):
```json
{
  "resolved": 25,
  "escalated": 12,
  "unresolved": 8
}
```

---

### Sentiment Distribution
```
GET /analytics/sentiment-distribution
```

**Description**: Get distribution of sentiment labels across all messages

**Example**:
```bash
curl -X GET "http://localhost:8000/analytics/sentiment-distribution"
```

**Response** (200):
```json
{
  "distribution": {
    "Positive": 120,
    "Neutral": 85,
    "Negative": 95
  },
  "total": 300
}
```

---

### Sentiment Over Time
```
GET /analytics/sentiment-over-time?days=30
```

**Description**: Get daily average sentiment trends

**Query Parameters**:
- `days` (int, optional): Number of days to look back (1-365, default: 30)

**Example**:
```bash
curl -X GET "http://localhost:8000/analytics/sentiment-over-time?days=7"
```

**Response** (200):
```json
{
  "days": 7,
  "data": [
    {
      "date": "2024-02-15",
      "avg_sentiment": 0.25,
      "conversation_count": 5
    },
    {
      "date": "2024-02-16",
      "avg_sentiment": -0.15,
      "conversation_count": 8
    },
    {
      "date": "2024-02-21",
      "avg_sentiment": 0.32,
      "conversation_count": 12
    }
  ]
}
```

---

### Escalation Playbook & Insights
```
GET /analytics/escalation-playbook
```

**Description**: Get insights from escalated conversations including keywords, patterns, and recommendations

**Example**:
```bash
curl -X GET "http://localhost:8000/analytics/escalation-playbook"
```

**Response** (200):
```json
{
  "total_escalated_conversations": 12,
  "top_negative_keywords": [
    {
      "keyword": "refund",
      "frequency": 5,
      "sentiment_impact": -0.45
    },
    {
      "keyword": "cancel",
      "frequency": 4,
      "sentiment_impact": -0.38
    },
    {
      "keyword": "angry",
      "frequency": 3,
      "sentiment_impact": -0.52
    }
  ],
  "most_common_failure_patterns": [
    {
      "pattern": "Negative sentiment progression",
      "occurrences": 8,
      "avg_time_to_escalation_minutes": 12.5
    }
  ],
  "avg_time_before_escalation_minutes": 10.2,
  "common_agent_response_delay_minutes": 3.5,
  "recommended_actions": [
    "Improve agent response time (currently > 3 minutes)",
    "Train agents to handle conversations with 'refund'",
    "Implement early intervention system"
  ]
}
```

---

## ML Prediction Endpoints

### Early Warning Prediction
```
POST /predict/early-warning
```

**Description**: Predict escalation risk based on first 3 customer messages using ML classifier

**Request**:
```json
{
  "thread_id": "string (required)",
  "customer_messages": ["string", "string", ...]
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/predict/early-warning \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "chat_12345",
    "customer_messages": [
      "I received a broken product",
      "This is your second time",
      "I want a refund!"
    ]
  }'
```

**Response** (200):
```json
{
  "thread_id": "chat_12345",
  "escalation_probability": 0.87,
  "confidence": 0.65,
  "risk_level": "high",
  "warning_reasons": [
    "High escalation probability detected",
    "Contains keywords: refund",
    "Negative sentiment detected early"
  ]
}
```

**Risk Levels**:
- `low`: probability < 0.4
- `medium`: probability 0.4 - 0.7
- `high`: probability > 0.7

**Errors**:
- 400: Invalid request format
- 500: Prediction error

---

## Data Models

### Sentiment Analysis Result
```json
{
  "message_id": "string",
  "sentiment_score": "float (-1 to +1)",
  "sentiment_label": "Positive | Neutral | Negative",
  "confidence": "float (0 to 1)"
}
```

### Conversation Analysis Response
```json
{
  "thread_id": "string",
  "message_count": "int",
  "sentiment_trajectory": ["float[]"],
  "overall_sentiment": "float",
  "escalation_detected": "boolean",
  "escalation_reasons": ["string[]"],
  "messages_with_sentiment": ["SentimentAnalysisResult[]"]
}
```

### Analytics Overview
```json
{
  "total_threads": "int",
  "escalated_threads": "int",
  "unresolved_threads": "int",
  "resolved_threads": "int",
  "escalation_rate": "float (0-100)",
  "avg_sentiment": "float"
}
```

---

## Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Endpoint executed successfully |
| 400 | Bad Request | Missing required field |
| 404 | Not Found | Conversation thread_id doesn't exist |
| 422 | Unprocessable Entity | Invalid data format |
| 500 | Server Error | Database connection failed |
| 503 | Service Unavailable | MongoDB not connected |

---

## Error Response Format

```json
{
  "detail": "Error message explaining what went wrong"
}
```

**Example**:
```json
{
  "detail": "Conversation must have at least one message"
}
```

---

## Rate Limiting

None implemented (add for production):
- 100 requests/minute per IP
- 1000 requests/hour per user
- Burst limit: 10 requests/second

---

## Pagination

Provided via:
- `limit` parameter on GET endpoints
- Default: 100
- Max: 1000

---

## Sorting

Default sorting:
- Conversations: `created_at` (descending - newest first)
- Analytics: Grouped/sorted by relevance

---

## Filtering

Currently available:
- By `platform` (in future analytics)
- By date range (in `/analytics/sentiment-over-time`)
- By `escalation_detected` status (in future)

---

## Common Query Examples

### Get last 5 escalated conversations
```bash
# Not directly supported - get all then filter client-side
curl -X GET "http://localhost:8000/conversations?limit=1000"
```

### Get escalation rate by platform
```bash
# Not directly supported - requires custom endpoint
# Workaround: Get /analytics/escalation-playbook for overall insights
```

### Get sentiment for date range
```bash
curl -X GET "http://localhost:8000/analytics/sentiment-over-time?days=7"
```

### Upload and immediately get details
```bash
curl -X POST http://localhost:8000/conversations/upload-thread \
  -H "Content-Type: application/json" \
  -d {...} | jq '.thread_id'

# Use thread_id from response to get conversation
curl -X GET http://localhost:8000/conversations/{thread_id}
```

---

## Authentication (Future)

When implementing authentication:

```bash
curl -X GET http://localhost:8000/conversations \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Required headers:
- `Authorization: Bearer <token>`

---

## Rate Limiting (Future)

Response headers:
- `X-RateLimit-Limit`: 100
- `X-RateLimit-Remaining`: 95
- `X-RateLimit-Reset`: 1613898000

---

## CORS Headers

All endpoints support:
```
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Testing with Postman

1. Download and install [Postman](https://www.postman.com/downloads/)
2. Create new collection
3. Add requests:
   - **GET** `http://localhost:8000/health`
   - **POST** `http://localhost:8000/conversations/upload-thread`
   - **GET** `http://localhost:8000/analytics/overview`
   - Etc.
4. Test all endpoints

---

## Interactive API Docs

Visit `http://localhost:8000/docs` for:
- Swagger UI
- Try-it-out for all endpoints
- Schema documentation
- Example requests/responses

---

## Webhooks (Future)

Could implement webhooks for:
- `conversation.escalated`
- `escalation.detected`
- `analysis.complete`

---

## Batch Operations (Future)

Could add:
- `POST /conversations/batch-upload` - Upload multiple conversations
- `POST /conversations/batch-analyze` - Analyze existing conversations

---

## Export Functions (Future)

Could add:
- `GET /conversations/{thread_id}/export/json` - JSON export
- `GET /conversations/{thread_id}/export/pdf` - PDF report
- `GET /analytics/export/csv` - Analytics CSV

---

**API Version**: 1.0.0  
**Last Updated**: February 21, 2024  
**Status**: Production Ready ✅
