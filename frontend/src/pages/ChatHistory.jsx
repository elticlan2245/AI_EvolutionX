import React, { useEffect, useState } from 'react'
import { Trash2, MessageSquare, Calendar, Search } from 'lucide-react'
import { useStore } from '../stores/useStore'

export default function ChatHistory() {
  const { conversations, loadConversations, deleteConversation, selectConversation } = useStore()
  const [search, setSearch] = useState('')
  const [filtered, setFiltered] = useState([])

  useEffect(() => {
    loadConversations()
  }, [])

  useEffect(() => {
    if (search) {
      setFiltered(conversations.filter(c => 
        c.title?.toLowerCase().includes(search.toLowerCase()) ||
        c.model?.toLowerCase().includes(search.toLowerCase())
      ))
    } else {
      setFiltered(conversations)
    }
  }, [search, conversations])

  return (
    <div className="flex-1 p-6 overflow-y-auto bg-gray-50">
      <div className="max-w-4xl mx-auto">
        <h2 className="text-2xl font-bold mb-6">Historial de Conversaciones</h2>
        
        <div className="mb-6 relative">
          <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Buscar conversaciones..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <div className="space-y-4">
          {filtered.map((conv) => (
            <div key={conv._id} className="bg-white rounded-lg p-4 shadow hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div className="flex-1 cursor-pointer" onClick={() => selectConversation(conv._id)}>
                  <h3 className="font-semibold text-gray-900 mb-1">{conv.title || 'Sin título'}</h3>
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <span className="flex items-center">
                      <MessageSquare className="w-4 h-4 mr-1" />
                      {conv.messages?.length || 0} mensajes
                    </span>
                    <span className="flex items-center">
                      <Calendar className="w-4 h-4 mr-1" />
                      {new Date(conv.updated_at).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mt-2">Modelo: {conv.model}</p>
                </div>
                <button
                  onClick={() => deleteConversation(conv._id)}
                  className="text-red-600 hover:text-red-700 p-2"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
