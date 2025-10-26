import React, { useEffect, useState } from 'react'
import { useStore } from '../stores/useStore'
import { Zap } from 'lucide-react'

export default function ModelSelector() {
  const { models, currentModel, setCurrentModel, loadModels } = useStore()
  const [isOpen, setIsOpen] = useState(false)

  useEffect(() => {
    loadModels()
  }, [])

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between space-x-2 px-4 py-2 bg-white border border-gray-200 rounded-lg hover:border-indigo-500 transition-colors"
      >
        <div className="flex items-center space-x-2 flex-1 min-w-0">
          <Zap className="w-4 h-4 text-indigo-600 flex-shrink-0" />
          <span className="text-sm font-medium truncate">{currentModel}</span>
        </div>
        <svg className="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute top-full mt-2 w-full bg-white border border-gray-200 rounded-lg shadow-lg z-50 max-h-96 overflow-y-auto">
          {models.length === 0 ? (
            <div className="p-4 text-center text-gray-500">
              <p className="text-sm">Loading models...</p>
            </div>
          ) : (
            models.map((model) => (
              <button
                key={model.name}
                onClick={() => {
                  setCurrentModel(model.name)
                  setIsOpen(false)
                }}
                className={`w-full text-left px-4 py-3 hover:bg-gray-50 border-b border-gray-100 last:border-b-0 ${
                  currentModel === model.name ? 'bg-indigo-50' : ''
                }`}
              >
                <div className="font-medium text-sm truncate">{model.name}</div>
                <div className="text-xs text-gray-500 mt-1">
                  {(model.size / 1e9).toFixed(1)} GB
                </div>
              </button>
            ))
          )}
        </div>
      )}
    </div>
  )
}
