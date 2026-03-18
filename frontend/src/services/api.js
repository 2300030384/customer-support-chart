import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  timeout: 10000, // Add 10 second timeout
})

export const conversationAPI = {
  uploadThread: (conversation) =>
    api.post('/conversations/upload-thread', conversation),
  
  getConversation: (threadId) =>
    api.get(`/conversations/${threadId}`),
  
  getAllConversations: (limit = 100) =>
    api.get('/conversations', { params: { limit } }),
  
  getSentimentTrajectory: (threadId) =>
    api.get(`/conversations/${threadId}/sentiment-trajectory`),
}

export const analyticsAPI = {
  getOverview: () =>
    api.get('/analytics/overview'),
  
  getFunnel: () =>
    api.get('/analytics/funnel'),
  
  getSentimentDistribution: () =>
    api.get('/analytics/sentiment-distribution'),
  
  getSentimentOverTime: (days = 30) =>
    api.get('/analytics/sentiment-over-time', { params: { days } }),
  
  getEscalationPlaybook: () =>
    api.get('/analytics/escalation-playbook'),
}

export const predictionAPI = {
  predictEarlyWarning: (threadId, customerMessages) =>
    api.post('/predict/early-warning', {
      thread_id: threadId,
      customer_messages: customerMessages,
    }),
}

export const healthAPI = {
  checkHealth: () =>
    api.get('/health'),
}

export default api
