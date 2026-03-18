# Testing Guide 🧪

Complete testing procedures to validate the sentiment analysis system.

---

## Prerequisites

- Backend running on `http://localhost:8000`
- Frontend running on `http://localhost:5173`
- MongoDB Atlas connected
- `curl` or Postman installed (JSON client recommended)

---

## 1. Health Check Tests

### Test 1.1: Server Health
```bash
curl -X GET http://localhost:8000/health

# Expected Response (200):
{
  "status": "healthy",
  "timestamp": "2024-02-21T10:00:00.000Z",
  "database": "connected"
}
```

### Test 1.2: Root Endpoint
```bash
curl -X GET http://localhost:8000/

# Expected Response (200):
{
  "message": "Sentiment Analysis API for Customer Support",
  "version": "1.0.0",
  "endpoints": { ... }
}
```

---

## 2. Sentiment Analysis Tests

### Test 2.1: Upload Basic Conversation
```bash
curl -X POST http://localhost:8000/conversations/upload-thread \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "test_basic_001",
    "platform": "Email",
    "messages": [
      {
        "speaker": "customer",
        "text": "Hello, I love your product!",
        "timestamp": "2024-02-21T10:00:00Z"
      },
      {
        "speaker": "agent",
        "text": "Thank you for the kind words!",
        "timestamp": "2024-02-21T10:01:00Z"
      }
    ]
  }'

# Expected Response (200):
# - escalation_detected: false
# - overall_sentiment: positive (> 0.3)
# - sentiment_trajectory: [positive_score, positive_score]
```

### Test 2.2: Upload Negative Conversation
```bash
curl -X POST http://localhost:8000/conversations/upload-thread \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "test_negative_001",
    "platform": "Twitter",
    "messages": [
      {
        "speaker": "customer",
        "text": "Your service is terrible!",
        "timestamp": "2024-02-21T10:00:00Z"
      },
      {
        "speaker": "agent",
        "text": "We apologize for your experience.",
        "timestamp": "2024-02-21T10:01:00Z"
      },
      {
        "speaker": "customer",
        "text": "I hate this company!",
        "timestamp": "2024-02-21T10:02:00Z"
      }
    ]
  }'

# Expected Response (200):
# - escalation_detected: true
# - contains trigger words warning
# - overall_sentiment: negative (< -0.2)
```

### Test 2.3: Escalation Detection
```bash
curl -X POST http://localhost:8000/conversations/upload-thread \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "test_escalation_001",
    "platform": "Chat",
    "messages": [
      {
        "speaker": "customer",
        "text": "I need help with my order",
        "timestamp": "2024-02-21T10:00:00Z"
      },
      {
        "speaker": "agent",
        "text": "Sure, what is the issue?",
        "timestamp": "2024-02-21T10:01:00Z"
      },
      {
        "speaker": "customer",
        "text": "This is bad service",
        "timestamp": "2024-02-21T10:02:00Z"
      },
      {
        "speaker": "agent",
        "text": "We are sorry to hear that",
        "timestamp": "2024-02-21T10:03:00Z"
      },
      {
        "speaker": "customer",
        "text": "I want a full refund NOW!",
        "timestamp": "2024-02-21T10:04:00Z"
      }
    ]
  }'

# Expected Response (200):
# - escalation_detected: true
# - escalation_reasons: ["Trigger words found: refund", ...]
# - messages[4].escalation_flag: true
```

### Test 2.4: Message with Sentiment Detail
```bash
curl -X POST http://localhost:8000/conversations/upload-thread \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "test_sentiment_detail_001",
    "platform": "Chat",
    "messages": [
      {"speaker": "customer", "text": "Amazing service!", "timestamp": "2024-02-21T10:00:00Z"},
      {"speaker": "customer", "text": "The worst experience ever", "timestamp": "2024-02-21T10:01:00Z"},
      {"speaker": "customer", "text": "It was okay", "timestamp": "2024-02-21T10:02:00Z"}
    ]
  }'

# Validate each message has different sentiment labels
# messages_with_sentiment[0].sentiment_label: "Positive"
# messages_with_sentiment[1].sentiment_label: "Negative"
# messages_with_sentiment[2].sentiment_label: "Neutral"
```

---

## 3. Conversation Retrieval Tests

### Test 3.1: Get All Conversations
```bash
curl -X GET http://localhost:8000/conversations

# Expected Response (200):
{
  "total": 4,
  "conversations": [
    {
      "thread_id": "test_basic_001",
      "escalation_detected": false,
      ...
    },
    ...
  ]
}
```

### Test 3.2: Get Specific Conversation
```bash
curl -X GET http://localhost:8000/conversations/test_basic_001

# Expected Response (200):
{
  "thread_id": "test_basic_001",
  "platform": "Email",
  "messages": [...],
  "escalation_detected": false,
  ...
}
```

### Test 3.3: Get Non-Existent Conversation
```bash
curl -X GET http://localhost:8000/conversations/nonexistent_id

# Expected Response (404):
{
  "detail": "Conversation not found"
}
```

### Test 3.4: Sentiment Trajectory
```bash
curl -X GET http://localhost:8000/conversations/test_escalation_001/sentiment-trajectory

# Expected Response (200):
{
  "thread_id": "test_escalation_001",
  "trajectory": [
    {"turn": 1, "sentiment": 0.5, "speaker": "customer", "escalation_point": false},
    {"turn": 2, "sentiment": 0.2, "speaker": "agent", "escalation_point": false},
    ...
  ]
}
```

---

## 4. Analytics Tests

### Test 4.1: Overview Analytics
```bash
curl -X GET http://localhost:8000/analytics/overview

# Expected Response (200):
{
  "total_threads": 4,
  "escalated_threads": 2,
  "unresolved_threads": 2,
  "resolved_threads": 2,
  "escalation_rate": 50.0,
  "avg_sentiment": 0.15
}
```

### Test 4.2: Funnel Data
```bash
curl -X GET http://localhost:8000/analytics/funnel

# Expected Response (200):
{
  "resolved": 2,
  "escalated": 1,
  "unresolved": 1
}
```

### Test 4.3: Sentiment Distribution
```bash
curl -X GET http://localhost:8000/analytics/sentiment-distribution

# Expected Response (200):
{
  "distribution": {
    "Positive": 3,
    "Neutral": 2,
    "Negative": 4
  },
  "total": 9
}
```

### Test 4.4: Sentiment Over Time
```bash
curl -X GET "http://localhost:8000/analytics/sentiment-over-time?days=30"

# Expected Response (200):
{
  "days": 30,
  "data": [
    {
      "date": "2024-02-21",
      "avg_sentiment": 0.15,
      "conversation_count": 2
    },
    ...
  ]
}
```

### Test 4.5: Escalation Playbook
```bash
curl -X GET http://localhost:8000/analytics/escalation-playbook

# Expected Response (200):
{
  "total_escalated_conversations": 2,
  "top_negative_keywords": [
    {
      "keyword": "refund",
      "frequency": 1,
      "sentiment_impact": -0.3
    },
    ...
  ],
  "most_common_failure_patterns": [...],
  "avg_time_before_escalation_minutes": 4.5,
  "common_agent_response_delay_minutes": 1.2,
  "recommended_actions": [
    "Improve agent response time...",
    ...
  ]
}
```

---

## 5. ML Prediction Tests

### Test 5.1: Early Warning Prediction
```bash
curl -X POST http://localhost:8000/predict/early-warning \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "prediction_test_001",
    "customer_messages": [
      "I received a broken product",
      "This is your second time sending me bad items",
      "I demand a refund for this!"
    ]
  }'

# Expected Response (200):
{
  "thread_id": "prediction_test_001",
  "escalation_probability": 0.82,
  "confidence": 0.65,
  "risk_level": "high",
  "warning_reasons": [
    "High escalation probability detected",
    "Contains keywords: refund"
  ]
}
```

### Test 5.2: Low-Risk Prediction
```bash
curl -X POST http://localhost:8000/predict/early-warning \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "prediction_test_002",
    "customer_messages": [
      "I have a quick question about billing",
      "When does my subscription renew?",
      "Also, can you confirm my payment method?"
    ]
  }'

# Expected Response (200):
# - escalation_probability: < 0.3
# - risk_level: "low"
# - warning_reasons: empty or minimal
```

### Test 5.3: Invalid Request
```bash
curl -X POST http://localhost:8000/predict/early-warning \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "test",
    "customer_messages": []
  }'

# Expected Response (200 or 400):
# Should handle gracefully, return low probability
```

---

## 6. Error Handling Tests

### Test 6.1: Missing Required Field
```bash
curl -X POST http://localhost:8000/conversations/upload-thread \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "Twitter"
  }'

# Expected Response (422): Validation error
{
  "detail": [
    {
      "loc": ["body", "thread_id"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Test 6.2: Empty Messages Array
```bash
curl -X POST http://localhost:8000/conversations/upload-thread \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "test",
    "platform": "Twitter",
    "messages": []
  }'

# Expected Response (400):
{
  "detail": "Conversation must have at least one message"
}
```

### Test 6.3: Invalid Speaker
```bash
curl -X POST http://localhost:8000/conversations/upload-thread \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "test",
    "messages": [
      {
        "speaker": "bot",
        "text": "Hello",
        "timestamp": "2024-02-21T10:00:00Z"
      }
    ]
  }'

# Expected Response (422): Validation error
```

---

## 7. Frontend UI Tests

### Test 7.1: Dashboard Page
1. Navigate to `http://localhost:5173`
2. **Verify**:
   - Page loads without errors
   - 4 KPI cards visible
   - Charts render (bar, pie, line)
   - Escalation insights panel shows
   - No console errors

### Test 7.2: Upload Conversation Page
1. Navigate to `http://localhost:5173/upload`
2. Click **Load Sample**
3. **Verify**:
   - JSON populates in textarea
   - Button changes to "Analyzing..."
   - Results display in right panel
   - Sentiment distribution shows
   - Can navigate to conversation details
   - No console errors

### Test 7.3: Thread Details Page
1. From upload page results, click conversation link
2. Or navigate directly to `http://localhost:5173/conversation/test_escalation_001`
3. **Verify**:
   - Conversation header displays
   - 4 metric cards show
   - Sentiment trajectory chart renders
   - Messages list displays
   - Sentiment labels color-coded
   - Escalation warnings visible (if applicable)
   - Early warning prediction shows (if data loaded)

### Test 7.4: Responsive Design
1. Open DevTools (F12)
2. Test at different breakpoints:
   - Mobile (375px)
   - Tablet (768px)
   - Desktop (1920px)
3. **Verify**:
   - Layout adapts smoothly
   - Navigation works
   - Charts responsive
   - No overflow/cut-off content

---

## 8. Database Tests

### Test 8.1: Check Indexes
```bash
# In MongoDB Atlas console:
db.conversations.getIndexes()

# Should show:
[
  { key: { _id: 1 } },
  { key: { thread_id: 1 }, unique: true },
  { key: { platform: 1 } },
  { key: { created_at: -1 } },
  ...
]
```

### Test 8.2: Query Conversations
```bash
# In MongoDB console:
db.conversations.find().count()  # Should be > 0

db.conversations.findOne()  # Check structure

db.conversations.find({ escalation_detected: true }).count()  # Escalated count
```

### Test 8.3: Aggregation Pipeline
```bash
# Test sentiment distribution aggregation:
db.conversations.aggregate([
  { $unwind: "$messages" },
  { $group: { _id: "$messages.sentiment_label", count: { $sum: 1 } } }
])

# Verify output matches /analytics/sentiment-distribution API response
```

---

## 9. Performance Tests

### Test 9.1: Response Time
```bash
# Measure API response times
time curl -X GET http://localhost:8000/analytics/overview
# Should be < 500ms for overview

time curl -X POST http://localhost:8000/conversations/upload-thread -d {...}
# Should be < 2s for sentiment analysis

time curl -X GET http://localhost:8000/analytics/escalation-playbook
# Should be < 1s for analytics
```

### Test 9.2: Concurrent Load
```bash
# Using Apache Bench (ab)
ab -n 100 -c 10 http://localhost:8000/health

# Expected: All requests succeed
# Response time: < 100ms per request
```

---

## 10. Integration Tests

### Test 10.1: Full User Flow
1. ✅ Start both servers
2. ✅ Open frontend dashboard
3. ✅ Navigate to upload page
4. ✅ Load sample data
5. ✅ Click analyze
6. ✅ See results
7. ✅ Navigate to conversation details
8. ✅ View sentiment trajectory
9. ✅ Return to dashboard
10. ✅ Verify new data in KPIs

### Test 10.2: Data Persistence
1. Upload conversation with thread_id = "persist_test"
2. Refresh page
3. Navigate to `/conversation/persist_test`
4. **Verify**: Data still exists (from MongoDB)
5. Stop backend, restart backend
6. **Verify**: Data still exists

---

## 11. Test Data Sets

### Positive Sentiment Test
```json
{
  "thread_id": "test_positive",
  "messages": [
    {"speaker": "customer", "text": "Excellent service!", "timestamp": "2024-02-21T10:00:00Z"},
    {"speaker": "agent", "text": "Thank you! Happy to help", "timestamp": "2024-02-21T10:01:00Z"}
  ]
}
```

### Negative Sentiment Test
```json
{
  "thread_id": "test_negative",
  "messages": [
    {"speaker": "customer", "text": "This is terrible!", "timestamp": "2024-02-21T10:00:00Z"},
    {"speaker": "agent", "text": "We apologize", "timestamp": "2024-02-21T10:01:00Z"}
  ]
}
```

### Mixed Sentiment Test
```json
{
  "thread_id": "test_mixed",
  "messages": [
    {"speaker": "customer", "text": "Great product", "timestamp": "2024-02-21T10:00:00Z"},
    {"speaker": "agent", "text": "Thanks for choosing us", "timestamp": "2024-02-21T10:01:00Z"},
    {"speaker": "customer", "text": "But shipping was slow", "timestamp": "2024-02-21T10:02:00Z"},
    {"speaker": "agent", "text": "We'll improve", "timestamp": "2024-02-21T10:03:00Z"}
  ]
}
```

---

## 12. Success Criteria Checklist

- [ ] All health checks pass
- [ ] Sentiment analysis labels are correct (Positive/Neutral/Negative)
- [ ] Escalation detection triggers for trigger words
- [ ] Escalation detection triggers for consecutive negatives
- [ ] Analytics endpoints return correct data
- [ ] ML predictions work (< 1s response time)
- [ ] Frontend dashboard loads without errors
- [ ] Upload form validates JSON correctly
- [ ] Charts render properly
- [ ] Responsive design works
- [ ] Data persists in MongoDB
- [ ] No console errors in browser
- [ ] No exception logs in backend
- [ ] Response times acceptable (< 2s for complex ops)

---

## Automation Scripts

### Run All API Tests (Bash)
```bash
#!/bin/bash
echo "Running Sentiment Analysis API Tests..."

# Test health
curl -s http://localhost:8000/health | jq .

# Test analytics
curl -s http://localhost:8000/analytics/overview | jq .

# Test upload (requires valid JSON file)
curl -X POST http://localhost:8000/conversations/upload-thread \
  -H "Content-Type: application/json" \
  -d @sample_conversation.json | jq .

echo "Tests complete!"
```

---

Great! You now have a comprehensive testing guide for the entire system.
