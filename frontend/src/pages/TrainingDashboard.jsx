import React, { useState, useEffect } from 'react'
import { useStore } from '../stores/useStore'
import { Play, TrendingUp, Database, Clock, CheckCircle, XCircle } from 'lucide-react'

export default function TrainingDashboard() {
  const { trainingStatus, startTraining, loadTrainingStatus } = useStore()
  const [isStarting, setIsStarting] = useState(false)

  useEffect(() => {
    loadTrainingStatus()
    const interval = setInterval(loadTrainingStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleStartTraining = async () => {
    setIsStarting(true)
    try {
      await startTraining()
    } finally {
      setIsStarting(false)
    }
  }

  const stats = trainingStatus?.statistics || {}
  const session = trainingStatus?.current_session

  return (
    <div className="flex-1 overflow-y-auto p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Training Dashboard</h1>
          
          <button
            onClick={handleStartTraining}
            disabled={isStarting || session?.status === 'training'}
            className="flex items-center space-x-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl font-semibold disabled:opacity-50"
          >
            <Play className="w-5 h-5" />
            <span>{isStarting ? 'Starting...' : 'Start Training'}</span>
          </button>
        </div>

        {/* Statistics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-white rounded-xl p-6 border border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <Database className="w-8 h-8 text-blue-600" />
              <span className="text-sm font-medium text-gray-500">Total</span>
            </div>
            <div className="text-3xl font-bold text-gray-900">{stats.total_samples || 0}</div>
            <div className="text-sm text-gray-500 mt-1">Samples</div>
          </div>

          <div className="bg-white rounded-xl p-6 border border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <CheckCircle className="w-8 h-8 text-green-600" />
              <span className="text-sm font-medium text-gray-500">Ready</span>
            </div>
            <div className="text-3xl font-bold text-gray-900">{stats.ready_samples || 0}</div>
            <div className="text-sm text-green-600 mt-1">High Quality</div>
          </div>

          <div className="bg-white rounded-xl p-6 border border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <TrendingUp className="w-8 h-8 text-purple-600" />
              <span className="text-sm font-medium text-gray-500">Quality</span>
            </div>
            <div className="text-3xl font-bold text-gray-900">{stats.avg_quality || 0}</div>
            <div className="text-sm text-gray-500 mt-1">Average</div>
          </div>

          <div className="bg-white rounded-xl p-6 border border-gray-200">
            <div className="flex items-center justify-between mb-2">
              <Clock className="w-8 h-8 text-orange-600" />
              <span className="text-sm font-medium text-gray-500">Status</span>
            </div>
            <div className="text-xl font-bold text-gray-900">
              {session ? session.status : 'Idle'}
            </div>
            <div className="text-sm text-gray-500 mt-1">Current</div>
          </div>
        </div>

        {/* Current Session */}
        {session && (
          <div className="bg-white rounded-xl p-6 border border-gray-200 mb-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Current Training Session</h2>
            
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <div className="text-sm text-gray-500">Model Name</div>
                <div className="font-semibold text-gray-900">{session.model_name}</div>
              </div>
              <div>
                <div className="text-sm text-gray-500">Base Model</div>
                <div className="font-semibold text-gray-900">{session.base_model}</div>
              </div>
              <div>
                <div className="text-sm text-gray-500">Samples</div>
                <div className="font-semibold text-gray-900">
                  {session.samples_collected} / {session.samples_target}
                </div>
              </div>
              <div>
                <div className="text-sm text-gray-500">Epoch</div>
                <div className="font-semibold text-gray-900">
                  {session.current_epoch} / {session.total_epochs}
                </div>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="mb-4">
              <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
                <span>Training Progress</span>
                <span>{Math.round((session.current_epoch / session.total_epochs) * 100)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-gradient-to-r from-indigo-600 to-purple-600 h-2 rounded-full transition-all"
                  style={{ width: `${(session.current_epoch / session.total_epochs) * 100}%` }}
                />
              </div>
            </div>

            {/* Metrics */}
            {session.metrics && (
              <div className="grid grid-cols-4 gap-4">
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-xs text-gray-500">Loss</div>
                  <div className="text-lg font-bold text-gray-900">
                    {session.metrics.loss.toFixed(3)}
                  </div>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-xs text-gray-500">Accuracy</div>
                  <div className="text-lg font-bold text-gray-900">
                    {(session.metrics.accuracy * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-xs text-gray-500">Perplexity</div>
                  <div className="text-lg font-bold text-gray-900">
                    {session.metrics.perplexity.toFixed(1)}
                  </div>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-xs text-gray-500">Learn Rate</div>
                  <div className="text-lg font-bold text-gray-900">
                    {session.metrics.learning_rate.toExponential(1)}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
