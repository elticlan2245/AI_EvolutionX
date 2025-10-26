import { useState } from 'react';
import { DollarSign, Users, TrendingUp, Copy, Gift } from 'lucide-react';

export default function Affiliates() {
  const [copied, setCopied] = useState(false);
  const affiliateLink = 'https://aievolutionx.com/ref/ABC123';

  const copyLink = () => {
    navigator.clipboard.writeText(affiliateLink);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-blue-50 py-20 px-4">
      <div className="max-w-7xl mx-auto">
        
        {/* Hero */}
        <div className="text-center mb-16">
          <div className="inline-block bg-green-100 text-green-700 px-4 py-2 rounded-full mb-4">
            💰 Gana hasta $1,000/mes pasivo
          </div>
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Programa de Afiliados
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Gana <span className="text-green-600 font-bold">20% de comisión de por vida</span> por
            cada usuario que refieras. Sin límites, sin vencimientos.
          </p>
        </div>

        {/* Stats */}
        <div className="grid md:grid-cols-4 gap-6 mb-16">
          {[
            { label: 'Comisión', value: '20%', icon: DollarSign, color: 'green' },
            { label: 'Usuarios Referidos', value: '0', icon: Users, color: 'blue' },
            { label: 'Ingresos Mensuales', value: '$0', icon: TrendingUp, color: 'purple' },
            { label: 'Pago Mínimo', value: '$50', icon: Gift, color: 'orange' }
          ].map((stat) => (
            <div key={stat.label} className="bg-white p-6 rounded-xl shadow-lg">
              <stat.icon className={`w-8 h-8 text-${stat.color}-600 mb-2`} />
              <div className="text-3xl font-bold text-gray-900">{stat.value}</div>
              <div className="text-gray-600 text-sm">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Link de afiliado */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-16">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            Tu Link de Afiliado
          </h3>
          <div className="flex gap-4">
            <input
              type="text"
              value={affiliateLink}
              readOnly
              className="flex-1 px-4 py-3 border rounded-lg bg-gray-50"
            />
            <button
              onClick={copyLink}
              className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition flex items-center gap-2"
            >
              <Copy className="w-5 h-5" />
              {copied ? '¡Copiado!' : 'Copiar'}
            </button>
          </div>
        </div>

        {/* Cómo funciona */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-16">
          <h3 className="text-3xl font-bold text-gray-900 mb-8 text-center">
            ¿Cómo Funciona?
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: '1',
                title: 'Comparte tu link',
                desc: 'Comparte tu link único en redes sociales, blog, o con amigos.'
              },
              {
                step: '2',
                title: 'Ellos se suscriben',
                desc: 'Cuando alguien se suscribe usando tu link, se registra como tu referido.'
              },
              {
                step: '3',
                title: 'Tú ganas dinero',
                desc: 'Ganas 20% de su suscripción CADA MES mientras sigan activos.'
              }
            ].map((item) => (
              <div key={item.step} className="text-center">
                <div className="w-16 h-16 bg-indigo-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                  {item.step}
                </div>
                <h4 className="text-xl font-semibold text-gray-900 mb-2">{item.title}</h4>
                <p className="text-gray-600">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Ejemplos de ganancias */}
        <div className="bg-gradient-to-r from-green-600 to-blue-600 rounded-2xl p-8 text-white mb-16">
          <h3 className="text-3xl font-bold mb-6 text-center">
            Potencial de Ingresos
          </h3>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              { refs: 10, plan: 'Pro ($10/mes)', monthly: '$20', yearly: '$240' },
              { refs: 50, plan: 'Pro ($10/mes)', monthly: '$100', yearly: '$1,200' },
              { refs: 100, plan: 'Pro ($10/mes)', monthly: '$200', yearly: '$2,400' }
            ].map((example) => (
              <div key={example.refs} className="bg-white/10 backdrop-blur rounded-xl p-6">
                <div className="text-4xl font-bold mb-2">{example.refs}</div>
                <div className="text-sm opacity-90 mb-4">{example.plan}</div>
                <div className="text-3xl font-bold mb-1">{example.monthly}/mes</div>
                <div className="text-sm opacity-90">{example.yearly}/año</div>
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="text-center">
          <button className="bg-indigo-600 text-white px-8 py-4 rounded-lg text-xl font-semibold hover:bg-indigo-700 transition">
            Comenzar a Ganar Ahora
          </button>
        </div>

      </div>
    </div>
  );
}
