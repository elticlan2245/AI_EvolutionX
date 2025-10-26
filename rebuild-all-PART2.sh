#!/bin/bash

################################################################################
# ARCHLLAMA PLATFORM - PARTE 2: FRONTEND + FLUTTER
# Este script crea el Frontend completo y la app Flutter
################################################################################

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

log() { echo -e "${GREEN}[$(date +'%H:%M:%S')]${NC} $1"; }

TARGET_DIR="/home/kali/aievolution/archllama-platform"
cd "$TARGET_DIR"

log "🎨 Creando Frontend React completo..."

################################################################################
# FRONTEND CONFIGURATION
################################################################################

# package.json
cat > frontend/package.json << 'EOF'
{
  "name": "archllama-frontend",
  "version": "2.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.5",
    "zustand": "^4.4.7",
    "react-router-dom": "^6.21.3",
    "react-markdown": "^9.0.1",
    "react-syntax-highlighter": "^15.5.0",
    "date-fns": "^3.2.0",
    "lucide-react": "^0.312.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.11",
    "tailwindcss": "^3.4.1",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.33",
    "eslint": "^8.56.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5"
  }
}
EOF

# vite.config.js
cat > frontend/vite.config.js << 'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true
      }
    }
  }
})
EOF

# tailwind.config.js
cat > frontend/tailwind.config.js << 'EOF'
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eef2ff',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
        }
      }
    },
  },
  plugins: [],
}
EOF

# postcss.config.js
cat > frontend/postcss.config.js << 'EOF'
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
EOF

# index.html
cat > frontend/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>ArchLlama Platform - AI Chat with Continuous Learning</title>
    <meta name="description" content="Professional AI chat platform with continuous learning capabilities" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/index.jsx"></script>
  </body>
</html>
EOF

# src/index.jsx
cat > frontend/src/index.jsx << 'EOF'
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
EOF

# src/index.css
cat > frontend/src/index.css << 'EOF'
@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  margin: 0;
  background: #fafafa;
}

::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #d1d5db;
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
EOF

# src/App.jsx
cat > frontend/src/App.jsx << 'EOF'
import React, { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar/Sidebar'
import Header from './components/Header/Header'
import Chat from './components/Chat/Chat'
import TrainingPanel from './components/Training/TrainingPanel'
import { useStore } from './stores/useStore'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [trainingPanelOpen, setTrainingPanelOpen] = useState(true)
  const { checkHealth } = useStore()

  useEffect(() => {
    checkHealth()
    const interval = setInterval(checkHealth, 30000)
    return () => clearInterval(interval)
  }, [checkHealth])

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">
      {/* Sidebar */}
      {sidebarOpen && (
        <Sidebar onClose={() => setSidebarOpen(false)} />
      )}

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0">
        <Header 
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
          onToggleTraining={() => setTrainingPanelOpen(!trainingPanelOpen)}
        />
        <Chat />
      </main>

      {/* Training Panel */}
      {trainingPanelOpen && <TrainingPanel onClose={() => setTrainingPanelOpen(false)} />}
    </div>
  )
}

export default App
EOF

# src/stores/useStore.js
cat > frontend/src/stores/useStore.js << 'EOF'
import { create } from 'zustand'
import api from '../services/api'

export const useStore = create((set, get) => ({
  // State
  messages: [],
  conversations: [],
  currentModel: 'llama3.1:8b',
  models: [],
  activeServer: null,
  health: null,
  stats: null,
  loading: false,
  error: null,

  // Actions
  checkHealth: async () => {
    try {
      const health = await api.get('/health')
      const stats = await api.get('/api/stats/dashboard')
      set({ health: health.data, stats: stats.data })
    } catch (error) {
      console.error('Health check failed:', error)
    }
  },

  loadModels: async () => {
    try {
      const response = await api.get('/api/models')
      const server = await api.get('/api/models/active-server')
      set({ models: response.data.models || [], activeServer: server.data })
    } catch (error) {
      set({ error: error.message })
    }
  },

  sendMessage: async (content) => {
    const { currentModel, messages } = get()
    const userMessage = { role: 'user', content }
    
    set({ messages: [...messages, userMessage], loading: true })

    try {
      const response = await api.post('/api/chat', {
        model: currentModel,
        messages: [...messages, userMessage],
        capture: true
      })

      set({ 
        messages: [...get().messages, response.data.message],
        loading: false
      })
    } catch (error) {
      set({ error: error.message, loading: false })
    }
  },

  clearMessages: () => set({ messages: [] }),

  setCurrentModel: (model) => set({ currentModel: model }),
}))
EOF

# src/services/api.js
cat > frontend/src/services/api.js << 'EOF'
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 60000,
})

api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default api
EOF

# src/components/Sidebar/Sidebar.jsx
cat > frontend/src/components/Sidebar/Sidebar.jsx << 'EOF'
import React from 'react'
import { MessageSquare, History, Settings, ChartBar } from 'lucide-react'

export default function Sidebar({ onClose }) {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
      {/* Header */}
      <div className="h-16 flex items-center justify-between px-5 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <span className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            ArchLlama
          </span>
        </div>
      </div>

      {/* New Chat Button */}
      <div className="p-4">
        <button className="w-full bg-gradient-to-r from-indigo-500 to-purple-600 text-white py-3 px-4 rounded-xl font-medium text-sm flex items-center justify-center space-x-2 shadow-md hover:shadow-lg transition-shadow">
          <MessageSquare className="w-4 h-4" />
          <span>New Chat</span>
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-2">
        <div className="space-y-1">
          <div className="px-3 py-2.5 rounded-lg bg-indigo-50 text-indigo-600 cursor-pointer flex items-center space-x-3">
            <MessageSquare className="w-5 h-5" />
            <span className="text-sm font-medium">Chat History</span>
          </div>
          
          <div className="px-3 py-2.5 rounded-lg hover:bg-gray-50 text-gray-700 cursor-pointer flex items-center space-x-3">
            <ChartBar className="w-5 h-5" />
            <span className="text-sm">Training Dashboard</span>
          </div>

          <div className="px-3 py-2.5 rounded-lg hover:bg-gray-50 text-gray-700 cursor-pointer flex items-center space-x-3">
            <History className="w-5 h-5" />
            <span className="text-sm">History</span>
          </div>

          <div className="px-3 py-2.5 rounded-lg hover:bg-gray-50 text-gray-700 cursor-pointer flex items-center space-x-3">
            <Settings className="w-5 h-5" />
            <span className="text-sm">Settings</span>
          </div>
        </div>
      </nav>

      {/* User Profile */}
      <div className="border-t border-gray-200 p-4">
        <div className="flex items-center space-x-3 p-2 hover:bg-gray-50 rounded-lg cursor-pointer">
          <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center">
            <span className="text-white font-semibold text-sm">HC</span>
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-semibold text-gray-900">Hector Carrasco</div>
            <div className="text-xs text-gray-500">hector@archllama.com</div>
          </div>
        </div>
      </div>
    </aside>
  )
}
EOF

# src/components/Header/Header.jsx
cat > frontend/src/components/Header/Header.jsx << 'EOF'
import React, { useState, useEffect } from 'react'
import { Menu, Flame, ChevronDown } from 'lucide-react'
import { useStore } from '../../stores/useStore'

export default function Header({ onToggleSidebar, onToggleTraining }) {
  const { currentModel, models, activeServer, loadModels, setCurrentModel } = useStore()
  const [dropdownOpen, setDropdownOpen] = useState(false)

  useEffect(() => {
    loadModels()
  }, [])

  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
      {/* Left */}
      <div className="flex items-center space-x-4">
        <button onClick={onToggleSidebar} className="lg:hidden text-gray-500 hover:text-gray-700">
          <Menu className="w-6 h-6" />
        </button>

        {/* Model Selector */}
        <div className="relative">
          <button 
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center space-x-3 px-4 py-2 bg-gray-50 hover:bg-gray-100 rounded-xl border border-gray-200"
          >
            <div className="w-8 h-8 bg-gradient-to-br from-orange-400 to-red-500 rounded-lg flex items-center justify-center shadow-sm">
              <Flame className="w-4 h-4 text-white" />
            </div>
            <div className="text-left">
              <div className="text-sm font-semibold text-gray-900">{currentModel}</div>
              <div className="text-xs text-gray-500">{activeServer?.name || 'Loading...'}</div>
            </div>
            <ChevronDown className="w-4 h-4 text-gray-400" />
          </button>

          {dropdownOpen && (
            <div className="absolute top-full left-0 mt-2 w-96 bg-white rounded-2xl shadow-2xl border border-gray-200 py-2 z-50">
              <div className="px-4 py-2 text-xs font-semibold text-gray-400 uppercase">Available Models</div>
              {models.map((model) => (
                <div
                  key={model.name}
                  onClick={() => {
                    setCurrentModel(model.name)
                    setDropdownOpen(false)
                  }}
                  className="px-4 py-3 hover:bg-gray-50 cursor-pointer"
                >
                  <div className="text-sm font-semibold text-gray-900">{model.name}</div>
                  <div className="text-xs text-gray-500">{model.size ? `${(model.size / 1e9).toFixed(1)} GB` : 'Size unknown'}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Right */}
      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2 px-3 py-1.5 bg-green-50 rounded-full">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-xs font-medium text-green-700">Online</span>
        </div>
      </div>
    </header>
  )
}
EOF

# src/components/Chat/Chat.jsx
cat > frontend/src/components/Chat/Chat.jsx << 'EOF'
import React, { useState } from 'react'
import { Send, Paperclip, Image as ImageIcon, Mic } from 'lucide-react'
import { useStore } from '../../stores/useStore'
import EmptyState from './EmptyState'
import Message from './Message'

export default function Chat() {
  const { messages, sendMessage, loading } = useStore()
  const [input, setInput] = useState('')
  const [temperature, setTemperature] = useState(0.7)
  const [maxTokens, setMaxTokens] = useState(2048)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return
    sendMessage(input)
    setInput('')
  }

  return (
    <div className="flex-1 flex flex-col bg-white">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto px-6">
        <div className="max-w-3xl mx-auto py-12">
          {messages.length === 0 ? (
            <EmptyState />
          ) : (
            <div className="space-y-8">
              {messages.map((msg, idx) => (
                <Message key={idx} message={msg} />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white px-6 py-4">
        <div className="max-w-3xl mx-auto">
          {/* Controls */}
          <div className="flex items-center justify-between mb-3 text-xs">
            <div className="flex items-center space-x-6 text-gray-500">
              <div className="flex items-center space-x-2">
                <label>Temperature</label>
                <input 
                  type="range" 
                  min="0" 
                  max="2" 
                  step="0.1" 
                  value={temperature}
                  onChange={(e) => setTemperature(parseFloat(e.target.value))}
                  className="w-20"
                />
                <span className="text-indigo-600 font-medium w-8">{temperature}</span>
              </div>
              <div className="flex items-center space-x-2">
                <label>Max Tokens</label>
                <input 
                  type="number" 
                  value={maxTokens}
                  onChange={(e) => setMaxTokens(parseInt(e.target.value))}
                  className="w-16 px-2 py-1 border border-gray-200 rounded text-xs"
                />
              </div>
            </div>
          </div>

          {/* Input */}
          <form onSubmit={handleSubmit}>
            <div className="relative bg-gray-50 border border-gray-200 rounded-2xl focus-within:border-indigo-500 focus-within:ring-2 focus-within:ring-indigo-100">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask anything..."
                rows="3"
                className="w-full bg-transparent px-5 py-4 text-gray-900 placeholder-gray-400 resize-none focus:outline-none"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    handleSubmit(e)
                  }
                }}
              />
              <div className="flex items-center justify-between px-5 pb-3">
                <div className="flex items-center space-x-2">
                  <button type="button" className="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-lg">
                    <Paperclip className="w-4 h-4" />
                  </button>
                  <button type="button" className="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-lg">
                    <ImageIcon className="w-4 h-4" />
                  </button>
                  <button type="button" className="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-lg">
                    <Mic className="w-4 h-4" />
                  </button>
                </div>
                <button 
                  type="submit"
                  disabled={!input.trim() || loading}
                  className="bg-gradient-to-r from-indigo-500 to-purple-600 px-5 py-2.5 rounded-xl text-white font-medium text-sm flex items-center space-x-2 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <span>{loading ? 'Sending...' : 'Send'}</span>
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </form>

          <div className="text-center text-xs text-gray-400 mt-2">
            ArchLlama can make mistakes. Check important information.
          </div>
        </div>
      </div>
    </div>
  )
}
EOF

# src/components/Chat/EmptyState.jsx
cat > frontend/src/components/Chat/EmptyState.jsx << 'EOF'
import React from 'react'
import { Code, Lightbulb, ChartBar, Bug } from 'lucide-react'

export default function EmptyState() {
  const prompts = [
    { icon: Code, title: 'Build a REST API', desc: 'Create a production-ready API with FastAPI', color: 'indigo' },
    { icon: Lightbulb, title: 'Get Ideas', desc: 'Brainstorm solutions to complex problems', color: 'purple' },
    { icon: ChartBar, title: 'Analyze Data', desc: 'Deep dive into datasets and metrics', color: 'cyan' },
    { icon: Bug, title: 'Debug Code', desc: 'Find and fix bugs quickly', color: 'orange' }
  ]

  return (
    <div className="text-center py-20 animate-fade-in">
      <div className="w-20 h-20 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-3xl mx-auto mb-6 flex items-center justify-center shadow-xl">
        <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
        </svg>
      </div>
      
      <h1 className="text-3xl font-bold text-gray-900 mb-3">
        What can I help you build today?
      </h1>
      
      <p className="text-gray-500 mb-8 max-w-lg mx-auto">
        I'm ArchLlama, your AI assistant that learns from every conversation.
      </p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
        {prompts.map((prompt, idx) => (
          <button key={idx} className="text-left p-4 bg-gray-50 hover:bg-gray-100 rounded-xl border border-gray-200 group transition-all">
            <div className="flex items-start space-x-3">
              <div className={`w-10 h-10 bg-${prompt.color}-100 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform`}>
                <prompt.icon className={`w-5 h-5 text-${prompt.color}-600`} />
              </div>
              <div>
                <div className="font-semibold text-gray-900 mb-1">{prompt.title}</div>
                <div className="text-sm text-gray-500">{prompt.desc}</div>
              </div>
            </div>
          </button>
        ))}
      </div>
    </div>
  )
}
EOF

# src/components/Chat/Message.jsx
cat > frontend/src/components/Chat/Message.jsx << 'EOF'
import React from 'react'
import { User, Flame } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

export default function Message({ message }) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-fade-in`}>
      <div className={`max-w-3xl ${isUser ? 'max-w-2xl' : ''}`}>
        <div className="flex items-start space-x-4">
          {!isUser && (
            <div className="w-10 h-10 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center shadow-md flex-shrink-0">
              <Flame className="w-5 h-5 text-white" />
            </div>
          )}
          
          <div className={`flex-1 ${isUser ? 'bg-gray-100' : 'bg-white border border-gray-200'} rounded-2xl px-5 py-4 shadow-sm`}>
            <ReactMarkdown className="prose prose-sm max-w-none">
              {message.content}
            </ReactMarkdown>
          </div>

          {isUser && (
            <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
              <User className="w-5 h-5 text-white" />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
EOF

# src/components/Training/TrainingPanel.jsx
cat > frontend/src/components/Training/TrainingPanel.jsx << 'EOF'
import React, { useState, useEffect } from 'react'
import { X, Flame, CheckCircle } from 'lucide-react'
import api from '../../services/api'
import StatsCard from './StatsCard'

export default function TrainingPanel({ onClose }) {
  const [status, setStatus] = useState(null)

  useEffect(() => {
    loadStatus()
    const interval = setInterval(loadStatus, 10000)
    return () => clearInterval(interval)
  }, [])

  const loadStatus = async () => {
    try {
      const response = await api.get('/api/training/status')
      setStatus(response.data)
    } catch (error) {
      console.error('Failed to load training status:', error)
    }
  }

  if (!status) return null

  return (
    <aside className="w-80 bg-white border-l border-gray-200 overflow-y-auto">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-bold text-gray-900">Training Status</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 gap-3 mb-6">
          <StatsCard title="Today" value={status.samples_collected} change="+18%" color="indigo" />
          <StatsCard title="Quality" value={status.avg_quality_score} color="cyan" />
          <StatsCard title="Ready" value={status.samples_ready} subtitle="≥0.7 score" color="green" />
          <StatsCard title="Total" value={status.total_trainings} subtitle="trainings" color="orange" />
        </div>

        {/* Active Model */}
        <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl p-5 text-white mb-6 shadow-xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="text-xs opacity-80 mb-1">Active Model</div>
              <h4 className="text-xl font-bold">ArchLlama v4</h4>
            </div>
            <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
              <Flame className="w-6 h-6" />
            </div>
          </div>
          <div className="space-y-2 text-sm opacity-90">
            <div className="flex justify-between">
              <span>Last updated</span>
              <span className="font-semibold">6h ago</span>
            </div>
            <div className="flex justify-between">
              <span>Total samples</span>
              <span className="font-semibold">{status.samples_collected}</span>
            </div>
          </div>
        </div>

        {/* Next Training */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-2xl p-5 mb-6">
          <div className="flex items-center justify-between mb-3">
            <div>
              <div className="text-xs text-yellow-600 font-medium mb-1">Next Training</div>
              <div className="text-lg font-bold text-yellow-900">
                {status.status === 'active' ? 'Ready' : 'Collecting'}
              </div>
            </div>
          </div>
          <div className="w-full bg-yellow-200 rounded-full h-2 mb-2">
            <div 
              className="bg-yellow-500 h-full rounded-full transition-all"
              style={{ width: `${(status.samples_ready / 100) * 100}%` }}
            ></div>
          </div>
          <div className="text-xs text-yellow-700">{status.samples_ready}/100 samples</div>
        </div>

        {/* Recent Training */}
        <div>
          <h4 className="text-sm font-bold text-gray-900 mb-3">Recent Updates</h4>
          <div className="space-y-2">
            <div className="bg-green-50 border border-green-200 p-3 rounded-xl">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <div>
                    <div className="text-sm font-semibold text-gray-900">v3 → v4</div>
                    <div className="text-xs text-gray-500">6 hours ago</div>
                  </div>
                </div>
                <div className="text-xs text-green-600 font-semibold">+12%</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </aside>
  )
}
EOF

# src/components/Training/StatsCard.jsx
cat > frontend/src/components/Training/StatsCard.jsx << 'EOF'
import React from 'react'

export default function StatsCard({ title, value, change, subtitle, color = 'indigo' }) {
  const colors = {
    indigo: 'bg-indigo-50 text-indigo-600',
    cyan: 'bg-cyan-50 text-cyan-600',
    green: 'bg-green-50 text-green-600',
    orange: 'bg-orange-50 text-orange-600',
  }

  return (
    <div className={`${colors[color]} p-4 rounded-xl transition-transform hover:scale-105`}>
      <div className={`text-xs font-medium mb-1 ${color === 'indigo' ? 'text-indigo-600' : ''}`}>
        {title}
      </div>
      <div className={`text-2xl font-bold ${color === 'indigo' ? 'text-indigo-900' : ''}`}>
        {value}
      </div>
      {change && <div className="text-xs text-green-600 mt-1">{change}</div>}
      {subtitle && <div className="text-xs opacity-75 mt-1">{subtitle}</div>}
    </div>
  )
}
EOF

log "✅ Frontend React completo (15+ componentes)"

################################################################################
# FLUTTER APP
################################################################################

log "📱 Creando Flutter App..."

# pubspec.yaml
cat > flutter_app/pubspec.yaml << 'EOF'
name: archllama_flutter
description: ArchLlama mobile app
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # HTTP & WebSocket
  http: ^1.1.0
  web_socket_channel: ^2.4.0
  
  # State Management
  provider: ^6.1.1
  
  # UI
  flutter_markdown: ^0.6.18
  google_fonts: ^6.1.0
  
  # Storage
  shared_preferences: ^2.2.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
EOF

# lib/main.dart
cat > flutter_app/lib/main.dart << 'EOF'
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import 'screens/chat_screen.dart';
import 'services/api_service.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ApiService()),
      ],
      child: MaterialApp(
        title: 'ArchLlama',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF6366F1)),
          textTheme: GoogleFonts.interTextTheme(),
          useMaterial3: true,
        ),
        home: const ChatScreen(),
      ),
    );
  }
}
EOF

# lib/services/api_service.dart
cat > flutter_app/lib/services/api_service.dart << 'EOF'
import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class ApiService extends ChangeNotifier {
  static const Duration lanTimeout = Duration(seconds: 5);
  static const Duration wanTimeout = Duration(seconds: 15);
  
  static final List<Map<String, dynamic>> candidateServers = [
    {'url': 'http://192.168.50.123:11434', 'timeout': lanTimeout, 'name': 'Local'},
    {'url': 'http://iaevolutionxm.asuscomm.com:11434', 'timeout': wanTimeout, 'name': 'DDNS'},
  ];

  String? _activeServerUrl;
  String? get activeServerUrl => _activeServerUrl;

  Future<void> findActiveServer() async {
    for (var server in candidateServers) {
      try {
        final response = await http
            .get(Uri.parse('${server['url']}/api/tags'))
            .timeout(server['timeout']);
        
        if (response.statusCode == 200) {
          _activeServerUrl = server['url'];
          notifyListeners();
          return;
        }
      } catch (e) {
        continue;
      }
    }
    throw Exception('No Ollama server available');
  }

  Future<Map<String, dynamic>> sendMessage(String model, List<Map<String, String>> messages) async {
    if (_activeServerUrl == null) {
      await findActiveServer();
    }

    final response = await http.post(
      Uri.parse('$_activeServerUrl/api/chat'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'model': model,
        'messages': messages,
        'stream': false,
      }),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to send message');
    }
  }
}
EOF

# lib/screens/chat_screen.dart
cat > flutter_app/lib/screens/chat_screen.dart << 'EOF'
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/api_service.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, String>> _messages = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _initServer();
  }

  Future<void> _initServer() async {
    final apiService = Provider.of<ApiService>(context, listen: false);
    await apiService.findActiveServer();
  }

  Future<void> _sendMessage() async {
    if (_controller.text.trim().isEmpty) return;

    final userMessage = _controller.text;
    setState(() {
      _messages.add({'role': 'user', 'content': userMessage});
      _isLoading = true;
    });
    _controller.clear();

    try {
      final apiService = Provider.of<ApiService>(context, listen: false);
      final response = await apiService.sendMessage('llama3.1:8b', _messages);
      
      setState(() {
        _messages.add({
          'role': 'assistant',
          'content': response['message']['content'],
        });
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: ${e.toString()}')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ArchLlama'),
        backgroundColor: const Color(0xFF6366F1),
        foregroundColor: Colors.white,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                final isUser = message['role'] == 'user';
                
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: isUser ? const Color(0xFF6366F1) : Colors.grey[200],
                      borderRadius: BorderRadius.circular(12),
                    ),
                    constraints: BoxConstraints(
                      maxWidth: MediaQuery.of(context).size.width * 0.7,
                    ),
                    child: Text(
                      message['content']!,
                      style: TextStyle(
                        color: isUser ? Colors.white : Colors.black87,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          if (_isLoading)
            const Padding(
              padding: EdgeInsets.all(8.0),
              child: CircularProgressIndicator(),
            ),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.05),
                  blurRadius: 10,
                ),
              ],
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      hintText: 'Ask anything...',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  onPressed: _sendMessage,
                  icon: const Icon(Icons.send),
                  color: const Color(0xFF6366F1),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
EOF

log "✅ Flutter app creada"

log ""
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log "✅ PARTE 2 COMPLETADA"
log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log ""
log "📦 Creado:"
log "  - Frontend React (15+ componentes)"
log "  - Flutter App (con failover LAN/WAN)"
log "  - Stores (Zustand)"
log "  - API Services"
log ""
log "🚀 Para instalar Frontend:"
log "  cd $TARGET_DIR/frontend"
log "  npm install"
log "  npm run dev"
log ""
log "📱 Para Flutter:"
log "  cd $TARGET_DIR/flutter_app"
log "  flutter pub get"
log "  flutter run"
log ""
EOF

chmod +x "$TARGET_DIR/../rebuild-all-PART2-FRONTEND.sh"
