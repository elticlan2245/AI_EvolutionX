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
