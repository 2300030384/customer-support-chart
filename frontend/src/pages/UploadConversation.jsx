import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { conversationAPI } from '@/services/api'

export default function UploadConversation() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    threadId: '',
    platform: 'Twitter',
    messages: [],
  })
  const [jsonText, setJsonText] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)
  const [analysisResult, setAnalysisResult] = useState(null)

  const sampleData = {
    thread_id: 'chat_12345',
    platform: 'Twitter',
    messages: [
      {
        speaker: 'customer',
        text: 'Hi, I have an issue with my order #5678',
        timestamp: new Date().toISOString(),
      },
      {
        speaker: 'agent',
        text: 'Hello! I would be happy to help you with your order. Can you tell me what the issue is?',
        timestamp: new Date(Date.now() + 60000).toISOString(),
      },
      {
        speaker: 'customer',
        text: "It's been 2 days and the item hasn't arrived yet. Your shipping is terrible!",
        timestamp: new Date(Date.now() + 120000).toISOString(),
      },
      {
        speaker: 'agent',
        text: 'I apologize for the delay. Let me check the tracking status for you.',
        timestamp: new Date(Date.now() + 180000).toISOString(),
      },
      {
        speaker: 'customer',
        text: 'I want a full refund now. This is unacceptable!',
        timestamp: new Date(Date.now() + 240000).toISOString(),
      },
    ],
  }

  const handleLoadSample = () => {
    setJsonText(JSON.stringify(sampleData, null, 2))
    setError(null)
  }

  const handleJsonChange = (e) => {
    setJsonText(e.target.value)
    setError(null)
  }

  const validateJson = () => {
    try {
      const data = JSON.parse(jsonText)

      if (!data.thread_id) {
        throw new Error('Missing required field: thread_id')
      }
      if (!Array.isArray(data.messages) || data.messages.length === 0) {
        throw new Error('messages must be a non-empty array')
      }

      for (const message of data.messages) {
        if (!message.speaker || !message.text || !message.timestamp) {
          throw new Error('Each message must have speaker, text, and timestamp')
        }
        if (!['customer', 'agent'].includes(message.speaker)) {
          throw new Error('speaker must be either "customer" or "agent"')
        }
      }

      return data
    } catch (err) {
      throw new Error(`JSON validation error: ${err.message}`)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError(null)
    setSuccess(null)
    setAnalysisResult(null)

    try {
      setLoading(true)

      // Validate and parse JSON
      const data = validateJson()

      // Convert timestamp strings to Date objects for API
      const messages = data.messages.map((msg) => ({
        ...msg,
        timestamp: new Date(msg.timestamp),
      }))

      // Submit to API
      const response = await conversationAPI.uploadThread({
        thread_id: data.thread_id,
        platform: data.platform || 'unknown',
        messages: messages,
      })

      setSuccess(`✓ Conversation uploaded successfully!`)
      setAnalysisResult(response.data)
      setJsonText('')

      // Optionally redirect after success
      setTimeout(() => {
        navigate(`/conversation/${data.thread_id}`)
      }, 2000)
    } catch (err) {
      const message =
        err.response?.data?.detail || err.message || 'Failed to upload conversation'
      setError(`Error: ${message}`)
      console.error('Upload error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container my-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-2">Upload Conversation</h1>
        <p className="text-gray-400 mb-8">Paste customer support conversation JSON or load a sample</p>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* JSON Input */}
          <div className="lg:col-span-2">
            <form onSubmit={handleSubmit}>
              <div className="card mb-6">
                <div className="flex items-center justify-between mb-4">
                  <label className="block text-white font-semibold">Conversation JSON</label>
                  <button
                    type="button"
                    onClick={handleLoadSample}
                    className="btn btn-secondary text-sm"
                  >
                    Load Sample
                  </button>
                </div>

                <textarea
                  value={jsonText}
                  onChange={handleJsonChange}
                  placeholder="Paste conversation JSON here..."
                  className="w-full h-96 bg-gray-800 text-white border border-gray-600 rounded-lg p-4 font-mono text-sm focus:outline-none focus:border-blue-500"
                />

                <div className="mt-4 text-xs text-gray-400">
                  <p>Format:</p>
                  <pre className="bg-gray-800 p-2 rounded mt-2 overflow-x-auto">
{`{
  "thread_id": "unique_id",
  "platform": "Twitter",
  "messages": [
    {
      "speaker": "customer|agent",
      "text": "message text",
      "timestamp": "2024-02-21T10:00:00Z"
    }
  ]
}`}
                  </pre>
                </div>
              </div>

              {error && (
                <div className="card bg-red-500/20 border border-red-500/50 text-red-300 mb-6">
                  {error}
                </div>
              )}

              {success && (
                <div className="card bg-green-500/20 border border-green-500/50 text-green-300 mb-6">
                  {success}
                </div>
              )}

              <button
                type="submit"
                disabled={loading || !jsonText.trim()}
                className="btn btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Analyzing...' : 'Analyze Conversation'}
              </button>
            </form>
          </div>

          {/* Analysis Result */}
          <div>
            {analysisResult && (
              <div className="card bg-gradient-to-br from-blue-500/20 to-purple-500/20 border border-blue-500/30 sticky top-8">
                <h3 className="text-lg font-bold text-white mb-4">Analysis Result</h3>

                <div className="space-y-4">
                  <div>
                    <p className="text-gray-400 text-sm">Messages Analyzed</p>
                    <p className="text-2xl font-bold text-white">
                      {analysisResult.message_count}
                    </p>
                  </div>

                  <div>
                    <p className="text-gray-400 text-sm">Overall Sentiment</p>
                    <p className="text-2xl font-bold text-white">
                      {analysisResult.overall_sentiment?.toFixed(2)}
                    </p>
                  </div>

                  {analysisResult.escalation_detected && (
                    <div className="bg-red-500/30 border border-red-500/50 rounded-lg p-3">
                      <p className="text-red-300 font-semibold text-sm mb-2">⚠️ Escalation Detected</p>
                      <ul className="text-xs text-red-200 space-y-1">
                        {analysisResult.escalation_reasons?.map((reason, idx) => (
                          <li key={idx}>• {reason}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {!analysisResult.escalation_detected && (
                    <div className="bg-green-500/30 border border-green-500/50 rounded-lg p-3">
                      <p className="text-green-300 font-semibold text-sm">✓ No Escalation</p>
                    </div>
                  )}

                  <div>
                    <p className="text-gray-400 text-sm mb-2">Sentiment Distribution</p>
                    <div className="space-y-1 text-sm">
                      {['Positive', 'Neutral', 'Negative'].map((label) => {
                        const count =
                          analysisResult.messages_with_sentiment?.filter(
                            (m) => m.sentiment_label === label
                          ).length || 0
                        const percentage =
                          analysisResult.message_count > 0
                            ? ((count / analysisResult.message_count) * 100).toFixed(0)
                            : 0
                        return (
                          <div key={label} className="flex items-center justify-between">
                            <span className="text-gray-300">{label}</span>
                            <span className="text-white font-medium">
                              {count} ({percentage}%)
                            </span>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
