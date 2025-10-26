import React, { useState, useEffect } from 'react'
import { Menu, Flame, ChevronDown } from 'lucide-react'
import { useStore } from '../../stores/useStore'

export default function Header({ onToggleSidebar, onToggleTraining }) {
  const { currentModel, models, activeServer, loadModels, setCurrentModel } = useStore()
  const [dropdownOpen, setDropdownOpen] = useState(false)

  useEffect(() => {
    loadModels()
  }, [])

  const handleModelSelect = (modelName) => {
    console.log('Selecting model:', modelName)
    setCurrentModel(modelName)
    setDropdownOpen(false)
  }

  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
      <div className="flex items-center space-x-4">
        <button onClick={onToggleSidebar} className="lg:hidden text-gray-500 hover:text-gray-700">
          <Menu className="w-6 h-6" />
        </button>

        <div className="relative">
          <button 
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center space-x-3 px-4 py-2 bg-gray-50 hover:bg-gray-100 rounded-xl border border-gray-200 transition-colors"
          >
            <div className="w-8 h-8 bg-gradient-to-br from-orange-400 to-red-500 rounded-lg flex items-center justify-center shadow-sm">
              <Flame className="w-4 h-4 text-white" />
            </div>
            <div className="text-left">
              <div className="text-sm font-semibold text-gray-900">{currentModel}</div>
              <div className="text-xs text-gray-500">{activeServer?.name || 'Loading...'}</div>
            </div>
            <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} />
          </button>

          {dropdownOpen && (
            <>
              <div 
                className="fixed inset-0 z-10" 
                onClick={() => setDropdownOpen(false)}
              />
              <div className="absolute top-full left-0 mt-2 w-96 bg-white rounded-2xl shadow-2xl border border-gray-200 py-2 z-20 max-h-96 overflow-y-auto">
                <div className="px-4 py-2 text-xs font-semibold text-gray-400 uppercase">Available Models</div>
                {models && models.length > 0 ? (
                  models.map((model) => (
                    <div
                      key={model.name}
                      onClick={() => handleModelSelect(model.name)}
                      className={`px-4 py-3 hover:bg-gray-50 cursor-pointer transition-colors ${
                        currentModel === model.name ? 'bg-indigo-50' : ''
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <div className="text-sm font-semibold text-gray-900">{model.name}</div>
                          <div className="text-xs text-gray-500">
                            {model.size ? `${(model.size / 1e9).toFixed(1)} GB` : 'Size unknown'}
                          </div>
                        </div>
                        {currentModel === model.name && (
                          <div className="w-2 h-2 bg-indigo-500 rounded-full"></div>
                        )}
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="px-4 py-3 text-sm text-gray-500">Loading models...</div>
                )}
              </div>
            </>
          )}
        </div>
      </div>

      <div className="flex items-center space-x-3">
        <div className="flex items-center space-x-2 px-3 py-1.5 bg-green-50 rounded-full">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-xs font-medium text-green-700">Online</span>
        </div>
      </div>
    </header>
  )
}
