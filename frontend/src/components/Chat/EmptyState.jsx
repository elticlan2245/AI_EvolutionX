import React from 'react'
import { Code, Lightbulb, BarChart, Bug } from 'lucide-react'

export default function EmptyState() {
  const prompts = [
    { icon: Code, title: 'Build a REST API', desc: 'Create a production-ready API with FastAPI', color: 'indigo' },
    { icon: Lightbulb, title: 'Get Ideas', desc: 'Brainstorm solutions to complex problems', color: 'purple' },
    { icon: BarChart, title: 'Analyze Data', desc: 'Deep dive into datasets and metrics', color: 'cyan' },
    { icon: Bug, title: 'Debug Code', desc: 'Find and fix bugs quickly', color: 'orange' }
  ]

  return (
    <div className="text-center py-20 animate-fade-in">
      <div className="w-20 h-20 bg-gradient-to-br from-purple-600 via-indigo-600 to-blue-600 rounded-3xl mx-auto mb-6 flex items-center justify-center shadow-xl">
        <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
        </svg>
      </div>
      
      <h1 className="text-4xl font-black text-gray-900 mb-3">
        What can I help you build today?
      </h1>
      
      <p className="text-gray-500 mb-8 max-w-lg mx-auto text-lg">
        I'm <span className="font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">AI_EvolutionX</span>, your intelligent assistant that learns from every conversation.
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
