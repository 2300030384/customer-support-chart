import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts'
import { conversationAPI, predictionAPI } from '@/services/api'

export default function ThreadDetails() {
  const { threadId } = useParams()
  const navigate = useNavigate()
  const [conversation, setConversation] = useState(null)
  const [trajectory, setTrajectory] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadConversation()
  }, [threadId])

  const loadConversation = async () => {
    try {
      setLoading(true)
      setError(null)

      const [convRes, trajRes] = await Promise.all([
        conversationAPI.getConversation(threadId),
        conversationAPI.getSentimentTrajectory(threadId),
      ])

      setConversation(convRes.data)
      setTrajectory(trajRes.data.trajectory)

      // Get early warning prediction
      const customerMessages = convRes.data.messages
        .filter((m) => m.speaker === 'customer')
        .map((m) => m.text)

      if (customerMessages.length > 0) {
        const predRes = await predictionAPI.predictEarlyWarning(threadId, customerMessages)
        setPrediction(predRes.data)
      }
    } catch (err) {
      console.error('Error loading conversation:', err)
      setError(err.response?.data?.detail || 'Failed to load conversation')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="container my-8 text-center text-white">Loading conversation...</div>
  }

  if (error) {
    return (
      <div className="container my-8">
        <button
          onClick={() => navigate('/')}
          className="mb-6 btn btn-secondary"
        >
          ← Back to Dashboard
        </button>
        <div className="bg-red-500/20 border border-red-500 text-red-400 px-4 py-3 rounded-lg">
          {error}
        </div>
      </div>
    )
  }

  if (!conversation) {
    return (
      <div className="container my-8">
        <button onClick={() => navigate('/')} className="mb-6 btn btn-secondary">
          ← Back to Dashboard
        </button>
        <div className="text-center text-gray-400">No conversation found</div>
      </div>
    )
  }

  const messages = conversation.messages || []
  const sentimentTrend = conversation.overall_sentiment_trend || []

  return (
    <div className="container my-8">
      <button onClick={() => navigate('/')} className="mb-6 btn btn-secondary">
        ← Back to Dashboard
      </button>

      <div className="max-w-6xl">
        {/* Header */}
        <div className="card mb-6 bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-blue-500/30">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-white">{conversation.thread_id}</h1>
              <p className="text-gray-400 mt-1">
                Platform: <span className="text-gray-300">{conversation.platform}</span>
              </p>
            </div>
            <div className="text-right">
              <div className={`badge ${
                conversation.escalation_detected ? 'badge-danger' : 'badge-success'
              }`}>
                {conversation.escalation_detected ? 'Escalated' : 'Not Escalated'}
              </div>
              <p className="text-gray-400 text-sm mt-2">
                Created: {new Date(conversation.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="card text-center">
            <p className="text-gray-400 text-sm">Messages</p>
            <p className="text-2xl font-bold text-white">{messages.length}</p>
          </div>
          <div className="card text-center">
            <p className="text-gray-400 text-sm">Avg Sentiment</p>
            <p className={`text-2xl font-bold ${
              conversation.overall_sentiment_trend
                ? conversation.overall_sentiment_trend.reduce((a, b) => a + b, 0) / conversation.overall_sentiment_trend.length > 0
                  ? 'text-green-400'
                  : 'text-red-400'
                : 'text-gray-300'
            }`}>
              {(conversation.overall_sentiment_trend?.reduce((a, b) => a + b, 0) / (conversation.overall_sentiment_trend?.length || 1))?.toFixed(2)}
            </p>
          </div>
          <div className="card text-center">
            <p className="text-gray-400 text-sm">Positive Messages</p>
            <p className="text-2xl font-bold text-green-400">
              {messages.filter((m) => m.sentiment_label === 'Positive').length}
            </p>
          </div>
          <div className="card text-center">
            <p className="text-gray-400 text-sm">Negative Messages</p>
            <p className="text-2xl font-bold text-red-400">
              {messages.filter((m) => m.sentiment_label === 'Negative').length}
            </p>
          </div>
        </div>

        {/* Escalation Alert */}
        {conversation.escalation_detected && (
          <div className="card bg-red-500/20 border border-red-500/50 mb-6">
            <h3 className="font-bold text-red-300 mb-3">⚠️ Escalation Warnings</h3>
            <ul className="space-y-2">
              {conversation.escalation_reasons?.map((reason, idx) => (
                <li key={idx} className="flex items-start gap-2 text-red-200 text-sm">
                  <span className="mt-1">•</span>
                  <span>{reason}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Early Warning Prediction */}
        {prediction && (
          <div className={`card mb-6 border ${
            prediction.risk_level === 'high'
              ? 'bg-red-500/20 border-red-500/50'
              : prediction.risk_level === 'medium'
              ? 'bg-orange-500/20 border-orange-500/50'
              : 'bg-green-500/20 border-green-500/50'
          }`}>
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-bold text-white">🤖 Early Warning Prediction</h3>
              <div className={`badge ${
                prediction.risk_level === 'high'
                  ? 'badge-danger'
                  : prediction.risk_level === 'medium'
                  ? 'badge-warning'
                  : 'badge-success'
              }`}>
                {prediction.risk_level.toUpperCase()} RISK
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <p className="text-gray-300 text-sm">Escalation Probability</p>
                <p className="text-2xl font-bold text-white">
                  {(prediction.escalation_probability * 100).toFixed(1)}%
                </p>
              </div>
              <div>
                <p className="text-gray-300 text-sm">Confidence</p>
                <p className="text-2xl font-bold text-white">
                  {(prediction.confidence * 100).toFixed(1)}%
                </p>
              </div>
            </div>
            {prediction.warning_reasons?.length > 0 && (
              <div>
                <p className="text-gray-300 text-sm mb-2">Warning Reasons:</p>
                <ul className="space-y-1">
                  {prediction.warning_reasons.map((reason, idx) => (
                    <li key={idx} className="text-sm text-gray-200">• {reason}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Sentiment Trajectory Chart */}
        {trajectory && trajectory.length > 0 && (
          <div className="card mb-6">
            <h3 className="text-lg font-bold text-white mb-4">Sentiment Trajectory</h3>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={trajectory}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="turn" stroke="#9ca3af" />
                <YAxis domain={[-1, 1]} stroke="#9ca3af" />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                  labelStyle={{ color: '#fff' }}
                  formatter={(value) => value.toFixed(2)}
                />
                <Legend />
                <ReferenceLine y={0} stroke="#6b7280" strokeDasharray="3 3" />
                <Line
                  type="monotone"
                  dataKey="sentiment"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  dot={(props) => {
                    const { cx, cy, payload } = props
                    const isEscalation = payload.escalation_point
                    return (
                      <circle
                        cx={cx}
                        cy={cy}
                        r={isEscalation ? 6 : 4}
                        fill={isEscalation ? '#ef4444' : '#3b82f6'}
                        stroke="#fff"
                        strokeWidth={1}
                      />
                    )
                  }}
                  name="Sentiment Score"
                />
              </LineChart>
            </ResponsiveContainer>
            <p className="text-xs text-gray-400 mt-2">
              <span className="inline-block w-3 h-3 bg-red-500 rounded-full mr-2"></span>
              Red dots indicate escalation points
            </p>
          </div>
        )}

        {/* Messages */}
        <div className="card">
          <h3 className="text-lg font-bold text-white mb-4">Messages ({messages.length})</h3>
          <div className="space-y-4">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`p-4 rounded-lg border ${
                  msg.speaker === 'customer'
                    ? 'bg-blue-500/10 border-blue-500/30'
                    : 'bg-gray-700/30 border-gray-600/30'
                }`}
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-3">
                    <span className={`font-semibold ${
                      msg.speaker === 'customer' ? 'text-blue-300' : 'text-gray-300'
                    }`}>
                      {msg.speaker === 'customer' ? '👤 Customer' : '🤖 Agent'}
                    </span>
                    <div className={`badge ${
                      msg.sentiment_label === 'Positive'
                        ? 'badge-success'
                        : msg.sentiment_label === 'Negative'
                        ? 'badge-danger'
                        : 'badge-info'
                    }`}>
                      {msg.sentiment_label}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-400">
                      {msg.sentiment_score.toFixed(2)}
                    </span>
                    {msg.escalation_flag && (
                      <span className="text-lg">⚠️</span>
                    )}
                  </div>
                </div>
                <p className="text-gray-300 text-sm mb-2">{msg.text}</p>
                <p className="text-xs text-gray-500">
                  {new Date(msg.timestamp).toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
