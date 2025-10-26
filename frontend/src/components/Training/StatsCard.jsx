import React from 'react'

export default function StatsCard({ title, value, change, subtitle, color = 'indigo' }) {
  const colors = {
    indigo: 'bg-indigo-50 text-indigo-600',
    cyan: 'bg-cyan-50 text-cyan-600',
    green: 'bg-green-50 text-green-600',
    orange: 'bg-orange-50 text-orange-600',
  }

  return (
    <div className={`${colors[color]} p-4 rounded-xl transition-transform hover:scale-105`}>
      <div className={`text-xs font-medium mb-1 ${color === 'indigo' ? 'text-indigo-600' : ''}`}>
        {title}
      </div>
      <div className={`text-2xl font-bold ${color === 'indigo' ? 'text-indigo-900' : ''}`}>
        {value}
      </div>
      {change && <div className="text-xs text-green-600 mt-1">{change}</div>}
      {subtitle && <div className="text-xs opacity-75 mt-1">{subtitle}</div>}
    </div>
  )
}
