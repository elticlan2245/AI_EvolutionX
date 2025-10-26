import { BarChart, Users, MessageSquare, Zap, TrendingUp } from 'lucide-react';

export default function Dashboard() {
  const stats = [
    { label: 'Mensajes Usados', value: '45 / 100', icon: MessageSquare, color: 'blue' },
    { label: 'Plan Actual', value: 'Free', icon: Zap, color: 'yellow' },
    { label: 'Referidos', value: '0', icon: Users, color: 'green' },
    { label: 'Ganado', value: '$0', icon: TrendingUp, color: 'purple' }
  ];

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>
      
      {/* Stats */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => (
          <div key={stat.label} className="bg-white p-6 rounded-xl shadow-lg">
            <stat.icon className={`w-8 h-8 text-${stat.color}-600 mb-2`} />
            <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
            <div className="text-gray-600 text-sm">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Upgrade prompt */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl p-8 text-white">
        <h3 className="text-2xl font-bold mb-2">🚀 ¡Mejora a Pro!</h3>
        <p className="mb-4 opacity-90">
          Desbloquea Claude 3.5, GPT-4, y 5,000 mensajes/mes por solo $10/mes
        </p>
        <button className="bg-white text-indigo-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition">
          Ver Planes
        </button>
      </div>
    </div>
  );
}
