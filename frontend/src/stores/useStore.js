import { create } from 'zustand'
import axios from 'axios'

// Usar rutas relativas - NGINX se encarga del proxy
const api = axios.create({ 
  baseURL: '', 
  timeout: 120000 
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 || error.response?.status === 403) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.reload()
    }
    return Promise.reject(error)
  }
)

export const useStore = create((set, get) => ({
  currentModel: 'deepseek-coder:6.7b',
  models: [],
  messages: [],
  loading: false,
  conversations: [],
  isRecording: false,
  isSpeaking: false,
  voiceEnabled: false,
  continuousVoiceMode: false,
  recognition: null,

  loadModels: async () => {
    try {
      const response = await api.get('/api/models')
      const models = response.data.models || []
      set({ models })
      if (models.length > 0) set({ currentModel: models[0].name })
    } catch (error) {
      console.error('Error:', error)
    }
  },

  setCurrentModel: (model) => set({ currentModel: model }),

  sendMessage: async (content, file = null) => {
    const { currentModel, messages, voiceEnabled, speak } = get()
    if (!content.trim() && !file) return

    const userMessage = { role: 'user', content, timestamp: new Date() }
    set({ messages: [...messages, userMessage], loading: true })

    try {
      const response = await api.post('/api/chat', {
        model: currentModel,
        messages: [...messages, userMessage].map(m => ({ role: m.role, content: m.content })),
        stream: false,
        capture: true
      })

      const assistantMessage = {
        role: 'assistant',
        content: response.data.message.content,
        timestamp: new Date()
      }

      set({ messages: [...get().messages, assistantMessage], loading: false })

      if (voiceEnabled || get().continuousVoiceMode) {
        speak(response.data.message.content)
      }
    } catch (error) {
      set({ 
        messages: [...get().messages, { 
          role: 'assistant', 
          content: 'Error: ' + (error.response?.data?.detail || error.message), 
          timestamp: new Date() 
        }],
        loading: false 
      })
    }
  },

  speak: async (text) => {
    try {
      set({ isSpeaking: true })
      const response = await api.post('/api/voice/synthesize', { text, language: 'es' }, { responseType: 'blob' })
      const audio = new Audio(URL.createObjectURL(response.data))
      audio.onended = () => set({ isSpeaking: false })
      await audio.play()
    } catch (error) {
      console.error('TTS Error:', error)
      set({ isSpeaking: false })
    }
  },

  startContinuousRecording: () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) return alert('Reconocimiento de voz no soportado en este navegador')

    const recognition = new SpeechRecognition()
    recognition.lang = 'es-ES'
    recognition.continuous = true
    recognition.interimResults = false

    recognition.onstart = () => {
      set({ isRecording: true, continuousVoiceMode: true, voiceEnabled: true })
    }

    recognition.onresult = (event) => {
      const transcript = event.results[event.results.length - 1][0].transcript
      get().sendMessage(transcript)
    }

    recognition.onerror = (event) => {
      console.error('Error voz:', event.error)
    }

    recognition.onend = () => {
      if (get().continuousVoiceMode) {
        setTimeout(() => recognition.start(), 300)
      }
    }

    recognition.start()
    set({ recognition })
  },

  stopContinuousRecording: () => {
    const { recognition } = get()
    if (recognition) recognition.stop()
    set({ isRecording: false, continuousVoiceMode: false, recognition: null })
  },

  toggleVoice: () => set((state) => ({ voiceEnabled: !state.voiceEnabled })),

  loadConversations: async () => {
    try {
      const response = await api.get('/api/conversations/')
      set({ conversations: response.data.conversations || [] })
    } catch (error) {
      console.error('Error:', error)
    }
  },

  deleteConversation: async (id) => {
    try {
      await api.delete(`/api/conversations/${id}`)
      get().loadConversations()
    } catch (error) {
      console.error('Error:', error)
    }
  },

  selectConversation: async (id) => {
    try {
      const response = await api.get(`/api/conversations/${id}`)
      set({ messages: response.data.messages || [] })
    } catch (error) {
      console.error('Error:', error)
    }
  },

  checkHealth: async () => {
    try {
      await api.get('/health')
    } catch (error) {
      console.error('Error:', error)
    }
  },

  clearMessages: () => set({ messages: [] })
}))
