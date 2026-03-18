# MongoDB Atlas Setup & Charts Configuration

## 1. MongoDB Atlas Atlas Setup

### Creating a Cluster
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new account or login
3. Create a new project called "sentiment-analysis"
4. Build a new database:
   - Provider: AWS
   - Region: Choose closest to your location
   - Tier: M0 Sandbox (free for learning)
5. Create a user with username/password
6. Whitelist your IP or use `0.0.0.0/0` for development
7. Copy the connection string:
   - Format: `mongodb+srv://username:password@cluster.mongodb.net/sentiment_db`

### Setting Up the Database

1. In Atlas, go to Collections and create:
   - Database: `sentiment_db`
   - Collection: `conversations`

2. The collection will automatically store documents with this structure:
   ```json
   {
     "_id": ObjectId,
     "thread_id": "string",
     "platform": "string",
     "created_at": Date,
     "updated_at": Date,
     "messages": [
       {
         "message_id": "string",
         "speaker": "customer|agent",
         "text": "string",
         "timestamp": Date,
         "sentiment_score": number,
         "sentiment_label": "Positive|Neutral|Negative",
         "escalation_flag": boolean
       }
     ],
     "overall_sentiment_trend": [number],
     "overall_sentiment_label": "string",
     "escalation_detected": boolean,
     "escalation_reasons": [string],
     "final_outcome": "resolved|escalated|unresolved"
   }
   ```

3. Create indexes for better query performance:
   - **Unique Index**: `thread_id`
   - **Regular Indexes**: `platform`, `created_at`, `escalation_detected`, `final_outcome`

---

## 2. MongoDB Atlas Charts Setup

### Chart 1: Funnel Chart (Conversation Outcomes)

**Purpose**: Visualize the distribution of conversation outcomes

**Aggregation Pipeline**:
```javascript
[
  {
    $group: {
      _id: "$final_outcome",
      count: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      outcome: "$_id",
      count: 1
    }
  },
  {
    $sort: { count: -1 }
  }
]
```

**Chart Configuration**:
- Type: **Bar Chart**
- X-axis: `outcome` (resolved, escalated, unresolved)
- Y-axis: `count`
- Title: "Conversation Outcomes"
- Colors: Green (resolved), Red (escalated), Gray (unresolved)

---

### Chart 2: Sentiment Trajectory Line Chart

**Purpose**: Track sentiment changes across individual conversations

**Aggregation Pipeline**:
```javascript
[
  {
    $match: { _id: ObjectId("conversation_id") }
  },
  {
    $unwind: {
      path: "$overall_sentiment_trend",
      includeArrayIndex: "messageIndex"
    }
  },
  {
    $project: {
      _id: 0,
      thread_id: 1,
      turn: { $add: ["$messageIndex", 1] },
      sentiment: "$overall_sentiment_trend"
    }
  }
]
```

**Chart Configuration**:
- Type: **Line Chart**
- X-axis: `turn` (message sequence number)
- Y-axis: `sentiment` (score from -1 to +1)
- Title: "Sentiment Trajectory"
- Color: Blue gradient
- Grid: Show grid for clarity

---

### Chart 3: Escalation Detection Pie Chart

**Purpose**: Show ratio of escalated vs non-escalated conversations

**Aggregation Pipeline**:
```javascript
[
  {
    $group: {
      _id: "$escalation_detected",
      count: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      status: {
        $cond: [
          { $eq: ["$_id", true] },
          "Escalated",
          "Not Escalated"
        ]
      },
      count: 1
    }
  }
]
```

**Chart Configuration**:
- Type: **Pie Chart**
- Category: `status`
- Value: `count`
- Title: "Escalation Rate"
- Colors: Red (Escalated), Green (Not Escalated)
- Show: Percentages and labels

---

### Chart 4: Sentiment Distribution Histogram

**Purpose**: Show distribution of sentiment labels across all messages

**Aggregation Pipeline**:
```javascript
[
  {
    $unwind: "$messages"
  },
  {
    $group: {
      _id: "$messages.sentiment_label",
      count: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      sentiment: "$_id",
      count: 1
    }
  },
  {
    $sort: { sentiment: 1 }
  }
]
```

**Chart Configuration**:
- Type: **Bar Chart** (or Histogram)
- X-axis: `sentiment` (Negative, Neutral, Positive)
- Y-axis: `count` (number of messages)
- Title: "Sentiment Distribution"
- Colors: Red (Negative), Gray (Neutral), Green (Positive)

---

### Chart 5: Escalation Reasons Analysis

**Purpose**: Show most common reasons for escalation

**Aggregation Pipeline**:
```javascript
[
  {
    $match: { escalation_detected: true }
  },
  {
    $unwind: "$escalation_reasons"
  },
  {
    $group: {
      _id: "$escalation_reasons",
      count: { $sum: 1 }
    }
  },
  {
    $sort: { count: -1 }
  },
  {
    $limit: 10
  },
  {
    $project: {
      _id: 0,
      reason: "$_id",
      frequency: "$count"
    }
  }
]
```

**Chart Configuration**:
- Type: **Horizontal Bar Chart**
- Y-axis: `reason`
- X-axis: `frequency`
- Title: "Top Escalation Reasons"
- Color: Red gradient

---

### Chart 6: Time Series - Average Sentiment Over Time

**Purpose**: Track sentiment trends over days/weeks

**Aggregation Pipeline**:
```javascript
[
  {
    $group: {
      _id: {
        $dateToString: {
          format: "%Y-%m-%d",
          date: "$created_at"
        }
      },
      avg_sentiment: {
        $avg: {
          $avg: "$overall_sentiment_trend"
        }
      },
      conversation_count: { $sum: 1 }
    }
  },
  {
    $sort: { _id: 1 }
  },
  {
    $project: {
      _id: 0,
      date: "$_id",
      avg_sentiment: 1,
      conversation_count: 1
    }
  }
]
```

**Chart Configuration**:
- Type: **Line Chart**
- X-axis: `date` (time series)
- Y-axis: `avg_sentiment` (scale -1 to 1)
- Title: "Sentiment Trend Over Time"
- Color: Blue gradient
- Secondary Y-axis (optional): `conversation_count`

---

### Chart 7: Template Variables (Filters)

To make charts interactive, add these filter variables in MongoDB Charts:

1. **Date Range Filter**:
   ```javascript
   {
     created_at: {
       $gte: ISODate("{{filterDate.start}}"),
       $lte: ISODate("{{filterDate.end}}")
     }
   }
   ```

2. **Platform Filter**:
   ```javascript
   {
     platform: "{{platformFilter}}"
   }
   ```

3. **Escalation Status Filter**:
   ```javascript
   {
     escalation_detected: {{escalationFilter}}
   }
   ```

---

## 3. Creating a Dashboard in MongoDB Atlas Charts

1. Go to **Charts** section in Atlas
2. Click "Create Dashboard"
3. Name it: "Sentiment Analysis Dashboard"
4. Add all charts created above
5. Arrange in grid layout:
   - Row 1: KPI cards (total conversations, escalation rate, etc.)
   - Row 2: Funnel chart, Escalation pie chart
   - Row 3: Sentiment distribution, Sentiment trajectory
   - Row 4: Time series sentiment, Escalation reasons
6. Add filters for interactive exploration
7. Set refresh rate: Auto-refresh every 5 minutes
8. Share dashboard with team

---

## 4. Best Practices for Monitoring

### Query Optimization
- Use indexed fields in `$match` stages
- Use `$limit` to reduce data processed
- Place `$match` early in pipeline

### Real-time Updates
- Enable real-time sync in Charts settings
- Set appropriate refresh intervals
- Use aggregation caching for slower pipelines

### Performance Tips
- Create compound indexes for common queries:
  ```
  { escalation_detected: 1, created_at: -1 }
  { platform: 1, final_outcome: 1 }
  ```
- Use `$project` to select only needed fields
- Use `$facet` to run multiple aggregations in one query

---

## 5. Connecting Backend to Atlas

In your `.env` file:
```
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/sentiment_db
MONGODB_DB_NAME=sentiment_db
```

The backend will automatically create indexes from `database/connection.py` on startup.

---

## 6. Example Queries for Analytics

### Total Conversations by Platform
```javascript
db.conversations.aggregate([
  { $group: { _id: "$platform", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
])
```

### Escalation Rate by Platform
```javascript
db.conversations.aggregate([
  { $group: {
      _id: "$platform",
      total: { $sum: 1 },
      escalated: { $sum: { $cond: ["$escalation_detected", 1, 0] } }
    }
  },
  { $project: {
      platform: "$_id",
      escalation_rate: {
        $multiply: [
          { $divide: ["$escalated", "$total"] },
          100
        ]
      }
    }
  }
])
```

### Average Conversation Duration (by message count)
```javascript
db.conversations.aggregate([
  { $group: {
      _id: "$platform",
      avg_messages: { $avg: { $size: "$messages" } }
    }
  }
])
```

---

## 7. Alerts and Monitoring

### Setting Alerts
1. In Atlas > Alerts, create alerts for:
   - High escalation rate (e.g., > 30%)
   - Low average sentiment (< -0.3)
   - Database connection issues

2. Configure notifications:
   - Email alerts
   - Slack integration
   - PagerDuty for critical issues

---

## Storage & Scaling

- **Free tier (M0)**: 512 MB storage
- **Shared tier (M2/M5)**: 2.5 - 10 GB
- **Dedicated (M10+)**: Scalable

Monitor under **Build** > **Metrics**:
- Storage usage
- Operation count
- Network traffic
- Query performance

---

This setup provides a complete monitoring and analytics platform for your sentiment analysis system!
