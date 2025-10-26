import React from 'react'
import { MessageSquare, History, Settings, BarChart, LogOut, Zap } from 'lucide-react'

export default function Sidebar({ onClose, user, onLogout }) {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
      <div className="h-16 flex items-center justify-between px-5 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 bg-gradient-to-br from-purple-600 via-indigo-600 to-blue-600 rounded-xl flex items-center justify-center shadow-lg">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <span className="text-lg font-black bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 bg-clip-text text-transparent">
            AI_EvolutionX
          </span>
        </div>
      </div>

      <div className="p-4">
        <button className="w-full bg-gradient-to-r from-purple-600 via-indigo-600 to-blue-600 text-white py-3 px-4 rounded-xl font-bold text-sm flex items-center justify-center space-x-2 shadow-md hover:shadow-lg transition-all">
          <MessageSquare className="w-4 h-4" />
          <span>New Chat</span>
        </button>
      </div>

      <nav className="flex-1 overflow-y-auto px-2">
        <div className="space-y-1">
          <div className="px-3 py-2.5 rounded-lg bg-indigo-50 text-indigo-600 cursor-pointer flex items-center space-x-3 transition-all hover:bg-indigo-100">
            <MessageSquare className="w-5 h-5" />
            <span className="text-sm font-semibold">Chat History</span>
          </div>
          
          <div className="px-3 py-2.5 rounded-lg hover:bg-gray-50 text-gray-700 cursor-pointer flex items-center space-x-3 transition-all">
            <BarChart className="w-5 h-5" />
            <span className="text-sm font-medium">Training Dashboard</span>
          </div>

          <div className="px-3 py-2.5 rounded-lg hover:bg-gray-50 text-gray-700 cursor-pointer flex items-center space-x-3 transition-all">
            <History className="w-5 h-5" />
            <span className="text-sm font-medium">History</span>
          </div>

          <div className="px-3 py-2.5 rounded-lg hover:bg-gray-50 text-gray-700 cursor-pointer flex items-center space-x-3 transition-all">
            <Settings className="w-5 h-5" />
            <span className="text-sm font-medium">Settings</span>
          </div>

          <div 
            onClick={onLogout}
            className="px-3 py-2.5 rounded-lg hover:bg-red-50 text-red-600 cursor-pointer flex items-center space-x-3 transition-all mt-4 border-t pt-4"
          >
            <LogOut className="w-5 h-5" />
            <span className="text-sm font-semibold">Logout</span>
          </div>
        </div>
      </nav>

      <div className="border-t border-gray-200 p-4">
        <div className="flex items-center space-x-3 p-2 hover:bg-gray-50 rounded-lg cursor-pointer transition-all">
          <div className="w-10 h-10 bg-gradient-to-br from-purple-600 via-indigo-600 to-blue-600 rounded-full flex items-center justify-center">
            <span className="text-white font-bold text-sm">
              {user?.username ? user.username.substring(0, 2).toUpperCase() : 'AE'}
            </span>
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm font-bold text-gray-900 truncate">
              {user?.username || 'Admin'}
            </div>
            <div className="text-xs text-gray-500 truncate">
              {user?.email || 'admin@aievolutionx.com'}
            </div>
          </div>
        </div>
      </div>
    </aside>
  )
}
