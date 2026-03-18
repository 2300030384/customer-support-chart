import React, { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { healthAPI } from '@/services/api'
import Dashboard from '@/pages/Dashboard'
import UploadConversation from '@/pages/UploadConversation'
import ThreadDetails from '@/pages/ThreadDetails'
import Chatbot from '@/pages/Chatbot'
import './App.css'

function App() {
  const [isConnected, setIsConnected] = useState(false)
  const [loading, setLoading] = useState(false) // Changed to false to show content immediately

  useEffect(() => {
    // Check health in the background without blocking the UI
    checkHealth()
  }, [])

  const checkHealth = async () => {
    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 5000) // 5 second timeout
      
      const response = await fetch('http://localhost:8000/health', {
        signal: controller.signal
      })
      clearTimeout(timeoutId)
      
      if (response.ok) {
        const data = await response.json()
        setIsConnected(data.status === 'healthy')
      } else {
        setIsConnected(false)
      }
    } catch (error) {
      console.error('Health check failed:', error.message)
      setIsConnected(false)
    }
  }

  // Show loading spinner only briefly, then show dashboard
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
          <p className="text-gray-700 font-medium">Loading...</p>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
          <p className="text-gray-700 font-medium">Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
        {/* Navigation */}
        <nav className="bg-gray-900 border-b border-gray-700 shadow-lg">
          <div className="container mx-auto px-4">
            <div className="flex items-center justify-between h-16">
              <Link to="/" className="flex items-center gap-2">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">SA</span>
                </div>
                <span className="text-white font-bold text-lg">Sentiment AI</span>
              </Link>

              <div className="flex items-center gap-8">
                <Link to="/" className="text-gray-300 hover:text-white transition-colors font-medium">
                  Dashboard
                </Link>
                <Link to="/upload" className="text-gray-300 hover:text-white transition-colors font-medium">
                  Upload
                </Link>
                <Link to="/chatbot" className="text-gray-300 hover:text-white transition-colors font-medium">
                  Chatbot
                </Link>
                <div className={`flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${
                  isConnected 
                    ? 'bg-green-500/20 text-green-400' 
                    : 'bg-red-500/20 text-red-400'
                }`}>
                  <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`}></div>
                  {isConnected ? 'Connected' : 'Disconnected'}
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<UploadConversation />} />
          <Route path="/conversation/:threadId" element={<ThreadDetails />} />
          <Route path="/chatbot" element={<Chatbot />} />
        </Routes>

        {/* Connection Warning */}
        {!isConnected && (
          <div className="fixed bottom-4 right-4 bg-red-500 text-white px-4 py-3 rounded-lg shadow-lg">
            <p className="font-medium">Backend is not connected. Please start the server.</p>
          </div>
        )}
      </div>
    </BrowserRouter>
  )
}

export default App
