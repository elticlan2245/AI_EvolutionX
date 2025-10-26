import React, { useState, useEffect } from 'react'
import { MessageSquare, History as HistoryIcon, TrendingUp, Settings as SettingsIcon, LogOut, Plus, Crown } from 'lucide-react'
import ChatInterface from './components/ChatInterface'
import ChatHistory from './pages/ChatHistory'
import TrainingDashboard from './pages/TrainingDashboard'
import Settings from './pages/Settings'
import Auth from './pages/Auth'
import ModelSelector from './components/ModelSelector'
import { useStore } from './stores/useStore'
import axios from 'axios'
import { API_BASE_URL } from './config/api'

export default function App() {
  const [currentPage, setCurrentPage] = useState('chat')
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const { loadModels, checkHealth, createConversation, clearMessages } = useStore()

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token')
      const savedUser = localStorage.getItem('user')
      
      console.log('Verificando autenticación...', { token: !!token, savedUser: !!savedUser })
      
      if (token && savedUser) {
        try {
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
          const response = await axios.get(`${API_BASE_URL}/api/auth/me`, {
            timeout: 5000
          })
          
          console.log('Token válido, usuario:', response.data)
          setIsAuthenticated(true)
          setUser(response.data)
          loadModels()
          checkHealth()
        } catch (error) {
          console.error('Error verificando token:', error.message)
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          delete axios.defaults.headers.common['Authorization']
          setIsAuthenticated(false)
          setUser(null)
        }
      } else {
        console.log('No hay token guardado')
      }
      
      setLoading(false)
    }
    
    // Timeout de seguridad
    const timeout = setTimeout(() => {
      console.log('Timeout alcanzado, mostrando login')
      setLoading(false)
      setIsAuthenticated(false)
    }, 3000)
    
    checkAuth().finally(() => clearTimeout(timeout))
  }, [])

  const handleLogin = (data) => {
    console.log('Login exitoso:', data.user)
    setIsAuthenticated(true)
    setUser(data.user)
    axios.defaults.headers.common['Authorization'] = `Bearer ${data.access_token}`
    loadModels()
    checkHealth()
  }

  const handleLogout = () => {
    console.log('Cerrando sesión...')
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    delete axios.defaults.headers.common['Authorization']
    setIsAuthenticated(false)
    setUser(null)
    clearMessages()
  }

  const handleNewChat = async () => {
    await createConversation()
    clearMessages()
    setCurrentPage('chat')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Verificando sesión...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Auth onLogin={handleLogin} />
  }

  const renderPage = () => {
    switch (currentPage) {
      case 'chat':
        return <ChatInterface />
      case 'history':
        return <ChatHistory />
      case 'training':
        return <TrainingDashboard />
      case 'settings':
        return <Settings />
      default:
        return <ChatInterface />
    }
  }

  const getPlanBadge = (plan) => {
    switch(plan) {
      case 'premium': return 'bg-indigo-100 text-indigo-700'
      case 'pro': return 'bg-purple-100 text-purple-700'
      default: return 'bg-gray-100 text-gray-700'
    }
  }

  return (
    <div className="flex h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
      <div className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
            AI_EvolutionX
          </h1>
          
          <div className="mt-3">
            <div className={`inline-flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-semibold ${getPlanBadge(user?.plan)}`}>
              <Crown className="w-3 h-3" />
              <span>{user?.plan?.toUpperCase() || 'FREE'}</span>
            </div>
          </div>
          
          <div className="mt-2 text-xs text-gray-600">
            <div className="flex items-center justify-between mb-1">
              <span>Messages</span>
              <span className="font-semibold">
                {user?.monthly_messages || 0} / {user?.monthly_limit === -1 ? '∞' : user?.monthly_limit || 100}
              </span>
            </div>
            {user?.monthly_limit !== -1 && (
              <div className="w-full bg-gray-200 rounded-full h-1.5">
                <div 
                  className="bg-indigo-600 h-1.5 rounded-full"
                  style={{ width: `${Math.min(((user?.monthly_messages || 0) / (user?.monthly_limit || 100)) * 100, 100)}%` }}
                />
              </div>
            )}
          </div>
        </div>

        <button
          onClick={handleNewChat}
          className="m-4 flex items-center justify-center space-x-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-4 py-3 rounded-xl font-semibold hover:opacity-90"
        >
          <Plus className="w-5 h-5" />
          <span>New Chat</span>
        </button>

        <div className="px-4 mb-4">
          <label className="text-xs font-medium text-gray-500 mb-2 block">AI Model</label>
          <ModelSelector />
        </div>

        <nav className="flex-1 p-4 space-y-2">
          <button
            onClick={() => setCurrentPage('chat')}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg font-medium transition-colors ${
              currentPage === 'chat' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-700 hover:bg-gray-50'
            }`}
          >
            <MessageSquare className="w-5 h-5" />
            <span>Chat</span>
          </button>

          <button
            onClick={() => setCurrentPage('history')}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg font-medium transition-colors ${
              currentPage === 'history' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-700 hover:bg-gray-50'
            }`}
          >
            <HistoryIcon className="w-5 h-5" />
            <span>History</span>
          </button>

          <button
            onClick={() => setCurrentPage('training')}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg font-medium transition-colors ${
              currentPage === 'training' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-700 hover:bg-gray-50'
            }`}
          >
            <TrendingUp className="w-5 h-5" />
            <span>Training</span>
          </button>

          <button
            onClick={() => setCurrentPage('settings')}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg font-medium transition-colors ${
              currentPage === 'settings' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-700 hover:bg-gray-50'
            }`}
          >
            <SettingsIcon className="w-5 h-5" />
            <span>Settings</span>
          </button>
        </nav>

        <div className="p-4 border-t border-gray-200">
          <div className="text-xs text-gray-600 mb-2 truncate">
            {user?.email}
          </div>
          <button 
            onClick={handleLogout}
            className="w-full flex items-center justify-center space-x-2 px-4 py-2 rounded-lg font-medium text-red-600 hover:bg-red-50 transition-colors"
          >
            <LogOut className="w-4 h-4" />
            <span>Logout</span>
          </button>
        </div>
      </div>

      <div className="flex-1 flex flex-col">
        {renderPage()}
      </div>
    </div>
  )
}
