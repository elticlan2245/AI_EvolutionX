import { useState } from 'react';
import { Check, Zap, Crown, Rocket } from 'lucide-react';

export default function Pricing() {
  const [billingPeriod, setBillingPeriod] = useState('monthly');

  const plans = [
    {
      name: 'Free',
      icon: Zap,
      price: billingPeriod === 'monthly' ? 0 : 0,
      description: 'Perfecto para empezar',
      features: [
        '100 mensajes/mes',
        'Solo modelos Ollama (local)',
        'Acceso básico al chat',
        'Historial de 7 días',
        'Soporte por email'
      ],
      cta: 'Comenzar Gratis',
      popular: false
    },
    {
      name: 'Pro',
      icon: Crown,
      price: billingPeriod === 'monthly' ? 10 : 96,
      description: 'Para profesionales',
      features: [
        '5,000 mensajes/mes',
        'Claude 3 Haiku',
        'GPT-3.5 Turbo',
        'Gemini Pro',
        'Todos los modelos Ollama',
        'Historial ilimitado',
        'Entrenamientos personalizados',
        'Sin anuncios',
        'Soporte prioritario'
      ],
      cta: 'Comenzar Ahora',
      popular: true
    },
    {
      name: 'Enterprise',
      icon: Rocket,
      price: billingPeriod === 'monthly' ? 50 : 480,
      description: 'Para equipos y empresas',
      features: [
        'Mensajes ilimitados',
        'Claude 3.5 Sonnet (mejor IA)',
        'GPT-4 Turbo',
        'Todos los modelos premium',
        'API privada',
        'Modelos personalizados',
        'Integración con tu negocio',
        'Soporte 24/7',
        'Onboarding personalizado',
        'SLA garantizado'
      ],
      cta: 'Contactar Ventas',
      popular: false
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 py-20 px-4">
      <div className="max-w-7xl mx-auto">
        
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Planes para cada necesidad
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Elige el plan perfecto para ti. Actualiza o cancela cuando quieras.
          </p>

          {/* Toggle de facturación */}
          <div className="inline-flex items-center bg-white rounded-full p-1 shadow-md">
            <button
              onClick={() => setBillingPeriod('monthly')}
              className={`px-6 py-2 rounded-full transition ${
                billingPeriod === 'monthly'
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-600'
              }`}
            >
              Mensual
            </button>
            <button
              onClick={() => setBillingPeriod('yearly')}
              className={`px-6 py-2 rounded-full transition ${
                billingPeriod === 'yearly'
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-600'
              }`}
            >
              Anual
              <span className="ml-2 text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                Ahorra 20%
              </span>
            </button>
          </div>
        </div>

        {/* Planes */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative bg-white rounded-2xl shadow-xl overflow-hidden transition transform hover:scale-105 ${
                plan.popular ? 'ring-4 ring-indigo-600' : ''
              }`}
            >
              {plan.popular && (
                <div className="absolute top-0 right-0 bg-indigo-600 text-white px-4 py-1 text-sm font-semibold rounded-bl-lg">
                  MÁS POPULAR
                </div>
              )}

              <div className="p-8">
                <div className="flex items-center mb-4">
                  <plan.icon className="w-10 h-10 text-indigo-600 mr-3" />
                  <h3 className="text-2xl font-bold text-gray-900">{plan.name}</h3>
                </div>

                <p className="text-gray-600 mb-6">{plan.description}</p>

                <div className="mb-6">
                  <span className="text-5xl font-bold text-gray-900">
                    ${plan.price}
                  </span>
                  <span className="text-gray-600">
                    /{billingPeriod === 'monthly' ? 'mes' : 'año'}
                  </span>
                </div>

                <button
                  className={`w-full py-3 rounded-lg font-semibold transition ${
                    plan.popular
                      ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                      : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                  }`}
                >
                  {plan.cta}
                </button>

                <ul className="mt-8 space-y-4">
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start">
                      <Check className="w-5 h-5 text-green-500 mr-3 flex-shrink-0 mt-0.5" />
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>

        {/* Garantía */}
        <div className="text-center bg-white rounded-2xl p-8 shadow-lg">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            🛡️ Garantía de 30 días
          </h3>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Prueba cualquier plan sin riesgo. Si no estás satisfecho en los primeros 30 días,
            te devolvemos el 100% de tu dinero. Sin preguntas.
          </p>
        </div>

        {/* FAQ */}
        <div className="mt-16 text-center">
          <h3 className="text-3xl font-bold text-gray-900 mb-8">
            Preguntas Frecuentes
          </h3>
          <div className="grid md:grid-cols-2 gap-6 text-left max-w-4xl mx-auto">
            {[
              {
                q: '¿Puedo cambiar de plan en cualquier momento?',
                a: 'Sí, puedes actualizar o degradar tu plan cuando quieras. Los cambios se aplican inmediatamente.'
              },
              {
                q: '¿Qué métodos de pago aceptan?',
                a: 'Aceptamos todas las tarjetas de crédito/débito, PayPal y transferencias bancarias.'
              },
              {
                q: '¿Los mensajes sin usar se acumulan?',
                a: 'No, los mensajes se reinician cada mes. Recomendamos el plan que mejor se ajuste a tu uso mensual.'
              },
              {
                q: '¿Hay descuentos para equipos?',
                a: 'Sí, contacta ventas para descuentos en licencias múltiples (5+ usuarios).'
              }
            ].map((faq, idx) => (
              <div key={idx} className="bg-white p-6 rounded-lg shadow">
                <h4 className="font-semibold text-gray-900 mb-2">{faq.q}</h4>
                <p className="text-gray-600">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
