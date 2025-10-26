import { Check, X, Zap } from 'lucide-react'

export default function ModelComparison() {
  const models = [
    {
      name: 'Claude 3.5 Sonnet',
      provider: 'Anthropic',
      speed: 'Rápido',
      quality: 'Excelente',
      cost: '$$',
      features: ['Mejor razonamiento', 'Análisis complejo', 'Contexto largo', 'Código experto'],
      available: ['Pro', 'Enterprise']
    },
    {
      name: 'GPT-4 Turbo',
      provider: 'OpenAI',
      speed: 'Medio',
      quality: 'Excelente',
      cost: '$$$',
      features: ['Muy versátil', 'Creatividad alta', 'Multimodal', 'Análisis profundo'],
      available: ['Enterprise']
    },
    {
      name: 'Claude 3 Haiku',
      provider: 'Anthropic',
      speed: 'Muy Rápido',
      quality: 'Buena',
      cost: '$',
      features: ['Económico', 'Respuestas rápidas', 'Tareas simples', 'Alto volumen'],
      available: ['Pro', 'Enterprise']
    },
    {
      name: 'Gemini Pro',
      provider: 'Google',
      speed: 'Rápido',
      quality: 'Muy Buena',
      cost: 'Gratis',
      features: ['Sin costo', 'Multimodal', 'Búsqueda integrada', 'Buen equilibrio'],
      available: ['Pro', 'Enterprise']
    },
    {
      name: 'Llama 3.1 70B',
      provider: 'Meta (Local)',
      speed: 'Medio',
      quality: 'Buena',
      cost: 'Gratis',
      features: ['100% privado', 'Sin límites', 'Open source', 'Local'],
      available: ['Free', 'Pro', 'Enterprise']
    }
  ]

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Comparador de Modelos</h1>
      <p className="text-gray-600 mb-8">Elige el modelo perfecto para tu tarea</p>

      <div className="overflow-x-auto">
        <table className="w-full bg-white rounded-xl shadow-lg">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Modelo</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Velocidad</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Calidad</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Costo</th>
              <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Disponible en</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {models.map((model) => (
              <tr key={model.name} className="hover:bg-gray-50">
                <td className="px-6 py-4">
                  <div className="font-semibold text-gray-900">{model.name}</div>
                  <div className="text-sm text-gray-500">{model.provider}</div>
                </td>
                <td className="px-6 py-4 text-gray-700">{model.speed}</td>
                <td className="px-6 py-4 text-gray-700">{model.quality}</td>
                <td className="px-6 py-4 text-gray-700">{model.cost}</td>
                <td className="px-6 py-4">
                  <div className="flex gap-2">
                    {model.available.map((plan) => (
                      <span
                        key={plan}
                        className="px-2 py-1 text-xs bg-indigo-100 text-indigo-700 rounded-full"
                      >
                        {plan}
                      </span>
                    ))}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Recomendaciones */}
      <div className="grid md:grid-cols-3 gap-6 mt-12">
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <Zap className="w-10 h-10 text-yellow-500 mb-4" />
          <h3 className="text-xl font-bold text-gray-900 mb-2">Tareas Rápidas</h3>
          <p className="text-gray-600 mb-4">Recomendado: Claude 3 Haiku o Gemini Pro</p>
          <ul className="text-sm text-gray-600 space-y-2">
            <li>• Resúmenes</li>
            <li>• Corrección de texto</li>
            <li>• Respuestas simples</li>
          </ul>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-lg">
          <Check className="w-10 h-10 text-green-500 mb-4" />
          <h3 className="text-xl font-bold text-gray-900 mb-2">Análisis Profundo</h3>
          <p className="text-gray-600 mb-4">Recomendado: Claude 3.5 Sonnet</p>
          <ul className="text-sm text-gray-600 space-y-2">
            <li>• Programación compleja</li>
            <li>• Análisis de datos</li>
            <li>• Estrategia de negocio</li>
          </ul>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-lg">
          <X className="w-10 h-10 text-red-500 mb-4" />
          <h3 className="text-xl font-bold text-gray-900 mb-2">Máxima Privacidad</h3>
          <p className="text-gray-600 mb-4">Recomendado: Llama 3.1 (Local)</p>
          <ul className="text-sm text-gray-600 space-y-2">
            <li>• 100% privado</li>
            <li>• Sin límites</li>
            <li>• Datos sensibles</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
