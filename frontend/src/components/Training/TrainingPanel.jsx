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
