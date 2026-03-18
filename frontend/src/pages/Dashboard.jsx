import React, { useState, useEffect } from 'react'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { analyticsAPI } from '@/services/api'

export default function Dashboard() {
  const [overview, setOverview] = useState(null)
  const [funnel, setFunnel] = useState(null)
  const [sentimentDist, setSentimentDist] = useState(null)
  const [sentimentTrend, setSentimentTrend] = useState(null)
  const [playbook, setPlaybook] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadAnalytics()
  }, [])

  const loadAnalytics = async () => {
    try {
      setLoading(true)
      setError(null)

      // Create a race between the API calls and a timeout
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Request timeout')), 10000)
      )

      const analyticsPromise = Promise.all([
        analyticsAPI.getOverview(),
        analyticsAPI.getFunnel(),
        analyticsAPI.getSentimentDistribution(),
        analyticsAPI.getSentimentOverTime(30),
        analyticsAPI.getEscalationPlaybook(),
      ])

      const [overviewRes, funnelRes, distRes, trendRes, playbookRes] = await Promise.race([
        analyticsPromise,
        timeoutPromise
      ])

      setOverview(overviewRes.data)
      setFunnel(funnelRes.data)
      setSentimentDist(distRes.data.distribution)
      setSentimentTrend(trendRes.data.data)
      setPlaybook(playbookRes.data)
    } catch (err) {
      console.error('Error loading analytics:', err.message || err)
      setError('Failed to load analytics data: ' + (err.message || 'Unknown error'))
      // Set empty state so app doesn't show loading forever
      setOverview({ total_threads: 0, escalated_threads: 0, unresolved_threads: 0, resolved_threads: 0, escalation_rate: 0, avg_sentiment: 0 })
      setFunnel({ resolved: 0, escalated: 0, unresolved: 0 })
      setSentimentDist({ Positive: 0, Neutral: 0, Negative: 0 })
      setSentimentTrend([])
      setPlaybook({ total_escalated_conversations: 0, top_negative_keywords: [], most_common_failure_patterns: [], avg_time_before_escalation_minutes: 0, common_agent_response_delay_minutes: 0, recommended_actions: [] })
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="container my-8 text-center text-white">Loading analytics...</div>
  }

  if (error) {
    return (
      <div className="container my-8">
        <div className="bg-red-500/20 border border-red-500 text-red-400 px-4 py-3 rounded-lg">
          {error}
        </div>
      </div>
    )
  }

  const COLORS = ['#10b981', '#f59e0b', '#ef4444']
  const sentimentDistData = sentimentDist
    ? [
        { name: 'Positive', value: sentimentDist.Positive || 0, fill: '#10b981' },
        { name: 'Neutral', value: sentimentDist.Neutral || 0, fill: '#6b7280' },
        { name: 'Negative', value: sentimentDist.Negative || 0, fill: '#ef4444' },
      ]
    : []

  const funnelData = funnel
    ? [
        { name: 'Resolved', value: funnel.resolved },
        { name: 'Escalated', value: funnel.escalated },
        { name: 'Unresolved', value: funnel.unresolved },
      ]
    : []

  return (
    <div className="container my-8">
      {/* Analytics Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Total Conversations */}
        <div className="card bg-gradient-to-br from-blue-500/20 to-blue-600/20 border border-blue-500/30">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-300 text-sm font-medium">Total Conversations</p>
              <h3 className="text-3xl font-bold text-white mt-2">
                {overview?.total_threads || 0}
              </h3>
            </div>
            <div className="text-4xl text-blue-400">💬</div>
          </div>
        </div>

        {/* Escalated */}
        <div className="card bg-gradient-to-br from-red-500/20 to-red-600/20 border border-red-500/30">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-red-300 text-sm font-medium">Escalated Threads</p>
              <h3 className="text-3xl font-bold text-white mt-2">
                {overview?.escalated_threads || 0}
              </h3>
            </div>
            <div className="text-4xl text-red-400">⚠️</div>
          </div>
        </div>

        {/* Escalation Rate */}
        <div className="card bg-gradient-to-br from-orange-500/20 to-orange-600/20 border border-orange-500/30">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-orange-300 text-sm font-medium">Escalation Rate</p>
              <h3 className="text-3xl font-bold text-white mt-2">
                {overview?.escalation_rate || 0}%
              </h3>
            </div>
            <div className="text-4xl text-orange-400">📊</div>
          </div>
        </div>

        {/* Avg Sentiment */}
        <div className="card bg-gradient-to-br from-green-500/20 to-green-600/20 border border-green-500/30">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-300 text-sm font-medium">Avg Sentiment</p>
              <h3 className="text-3xl font-bold text-white mt-2">
                {overview?.avg_sentiment?.toFixed(2) || 0}
              </h3>
            </div>
            <div className="text-4xl text-green-400">😊</div>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Funnel Chart */}
        <div className="card">
          <h3 className="text-lg font-bold text-white mb-4">Conversation Outcomes</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={funnelData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="name" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                labelStyle={{ color: '#fff' }}
              />
              <Bar dataKey="value" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Sentiment Distribution */}
        <div className="card">
          <h3 className="text-lg font-bold text-white mb-4">Sentiment Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={sentimentDistData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {sentimentDistData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                labelStyle={{ color: '#fff' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Sentiment Over Time */}
        <div className="card lg:col-span-2">
          <h3 className="text-lg font-bold text-white mb-4">Sentiment Trend (Last 30 Days)</h3>
          {sentimentTrend && sentimentTrend.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={sentimentTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="date" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" domain={[-1, 1]} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
                  labelStyle={{ color: '#fff' }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="avg_sentiment"
                  stroke="#3b82f6"
                  name="Avg Sentiment"
                  strokeWidth={2}
                  dot={{ fill: '#3b82f6' }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-gray-400 text-center py-8">No sentiment data available</p>
          )}
        </div>
      </div>

      {/* Escalation Insights */}
      {playbook && (
        <div className="card">
          <h3 className="text-lg font-bold text-white mb-4">🔥 Escalation Insights</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-gray-700/50 rounded-lg p-4">
              <p className="text-gray-400 text-sm">Total Escalations</p>
              <p className="text-2xl font-bold text-white mt-2">
                {playbook.total_escalated_conversations}
              </p>
            </div>
            <div className="bg-gray-700/50 rounded-lg p-4">
              <p className="text-gray-400 text-sm">Avg Time Before Escalation</p>
              <p className="text-2xl font-bold text-white mt-2">
                {playbook.avg_time_before_escalation_minutes.toFixed(1)}m
              </p>
            </div>
            <div className="bg-gray-700/50 rounded-lg p-4">
              <p className="text-gray-400 text-sm">Avg Response Delay</p>
              <p className="text-2xl font-bold text-white mt-2">
                {playbook.common_agent_response_delay_minutes.toFixed(1)}m
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Top Keywords */}
            <div>
              <h4 className="font-semibold text-white mb-3">🔴 Top Negative Keywords</h4>
              <ul className="space-y-2">
                {playbook.top_negative_keywords?.slice(0, 5).map((kw, idx) => (
                  <li key={idx} className="flex items-center justify-between text-sm">
                    <span className="text-gray-300">{kw.keyword}</span>
                    <span className="badge badge-danger">{kw.frequency}x</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Recommended Actions */}
            <div>
              <h4 className="font-semibold text-white mb-3">💡 Recommended Actions</h4>
              <ul className="space-y-2">
                {playbook.recommended_actions?.map((action, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-gray-300">
                    <span className="text-green-400 mt-1">✓</span>
                    <span>{action}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
