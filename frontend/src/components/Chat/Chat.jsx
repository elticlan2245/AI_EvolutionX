import React, { useState } from 'react'
import { Send, Paperclip, Image, Mic } from 'lucide-react'
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

      <div className="border-t border-gray-200 bg-white px-6 py-4">
        <div className="max-w-3xl mx-auto">
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
                    <Image className="w-4 h-4" />
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
            AI_EvolutionX can make mistakes. Check important information.
          </div>
        </div>
      </div>
    </div>
  )
}
