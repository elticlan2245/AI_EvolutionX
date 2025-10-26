import React, { useState, useEffect } from 'react'
import { Save, User, Palette, Globe, Bell, Lock } from 'lucide-react'
import axios from 'axios'

export default function Settings() {
  const [settings, setSettings] = useState({
    theme: 'light',
    language: 'es',
    voice_enabled: false,
    voice_language: 'es',
    voice_speed: 1.0,
    notifications: true,
    auto_save: true
  })
  const [saved, setSaved] = useState(false)

  const handleSave = async () => {
    try {
      await axios.put('/api/settings/', settings)
      setSaved(true)
      setTimeout(() => setSaved(false), 3000)
    } catch (error) {
      console.error('Error saving settings:', error)
    }
  }

  return (
    <div className="flex-1 p-6 overflow-y-auto bg-gray-50">
      <div className="max-w-2xl mx-auto">
        <h2 className="text-2xl font-bold mb-6">Configuración</h2>

        <div className="space-y-6">
          {/* Apariencia */}
          <div className="bg-white rounded-lg p-6 shadow">
            <div className="flex items-center mb-4">
              <Palette className="w-5 h-5 mr-2 text-indigo-600" />
              <h3 className="text-lg font-semibold">Apariencia</h3>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Tema</label>
                <select
                  value={settings.theme}
                  onChange={(e) => setSettings({...settings, theme: e.target.value})}
                  className="w-full border rounded-lg px-4 py-2"
                >
                  <option value="light">Claro</option>
                  <option value="dark">Oscuro</option>
                  <option value="auto">Automático</option>
                </select>
              </div>
            </div>
          </div>

          {/* Idioma */}
          <div className="bg-white rounded-lg p-6 shadow">
            <div className="flex items-center mb-4">
              <Globe className="w-5 h-5 mr-2 text-indigo-600" />
              <h3 className="text-lg font-semibold">Idioma</h3>
            </div>
            <select
              value={settings.language}
              onChange={(e) => setSettings({...settings, language: e.target.value})}
              className="w-full border rounded-lg px-4 py-2"
            >
              <option value="es">Español</option>
              <option value="en">English</option>
            </select>
          </div>

          {/* Voz */}
          <div className="bg-white rounded-lg p-6 shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <Bell className="w-5 h-5 mr-2 text-indigo-600" />
                <h3 className="text-lg font-semibold">Voz</h3>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={settings.voice_enabled}
                  onChange={(e) => setSettings({...settings, voice_enabled: e.target.checked})}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-indigo-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
              </label>
            </div>
            {settings.voice_enabled && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Velocidad</label>
                  <input
                    type="range"
                    min="0.5"
                    max="2"
                    step="0.1"
                    value={settings.voice_speed}
                    onChange={(e) => setSettings({...settings, voice_speed: parseFloat(e.target.value)})}
                    className="w-full"
                  />
                  <span className="text-sm text-gray-600">{settings.voice_speed}x</span>
                </div>
              </div>
            )}
          </div>

          {/* Botón Guardar */}
          <button
            onClick={handleSave}
            className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-3 rounded-lg font-semibold hover:opacity-90 flex items-center justify-center"
          >
            <Save className="w-5 h-5 mr-2" />
            {saved ? '✓ Guardado' : 'Guardar Cambios'}
          </button>
        </div>
      </div>
    </div>
  )
}
