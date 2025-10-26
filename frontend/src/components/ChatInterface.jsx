import React, { useState, useRef, useEffect } from 'react'
import { Send, Paperclip, Mic, MicOff, Image as ImageIcon, X, Volume2, VolumeX, Camera, Bot } from 'lucide-react'
import { useStore } from '../stores/useStore'
import ReactMarkdown from 'react-markdown'

export default function ChatInterface() {
  const { 
    messages, 
    loading, 
    sendMessage, 
    currentModel, 
    isRecording, 
    startContinuousRecording, 
    stopContinuousRecording,
    isSpeaking,
    voiceEnabled,
    toggleVoice,
    continuousVoiceMode,
    toggleContinuousVoice
  } = useStore()
  
  const [input, setInput] = useState('')
  const [selectedFile, setSelectedFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [showCamera, setShowCamera] = useState(false)
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)
  const videoRef = useRef(null)
  const streamRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      const reader = new FileReader()
      reader.onload = (e) => setPreviewUrl(e.target.result)
      reader.readAsDataURL(file)
    } else {
      alert('Solo imágenes permitidas')
    }
  }

  const removeFile = () => {
    setSelectedFile(null)
    setPreviewUrl(null)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true })
      streamRef.current = stream
      if (videoRef.current) videoRef.current.srcObject = stream
      setShowCamera(true)
    } catch (error) {
      alert('No se pudo acceder a la cámara: ' + error.message)
    }
  }

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop())
      streamRef.current = null
    }
    setShowCamera(false)
  }

  const capturePhoto = () => {
    if (videoRef.current) {
      const canvas = document.createElement('canvas')
      canvas.width = videoRef.current.videoWidth
      canvas.height = videoRef.current.videoHeight
      canvas.getContext('2d').drawImage(videoRef.current, 0, 0)
      canvas.toBlob((blob) => {
        const file = new File([blob], `photo-${Date.now()}.jpg`, { type: 'image/jpeg' })
        setSelectedFile(file)
        setPreviewUrl(canvas.toDataURL())
        stopCamera()
      }, 'image/jpeg')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if ((!input.trim() && !selectedFile) || loading) return

    let finalMessage = input.trim()
    if (selectedFile) {
      finalMessage = `${finalMessage}\n[Imagen: ${selectedFile.name}]`
    }

    await sendMessage(finalMessage, selectedFile)
    setInput('')
    removeFile()
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <div className="flex-1 flex flex-col bg-white">
      {/* Header */}
      <div className="border-b border-gray-200 p-4 bg-gradient-to-r from-indigo-50 to-purple-50">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full flex items-center justify-center">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900">AI Assistant</h2>
              <p className="text-xs text-gray-500">{currentModel}</p>
            </div>
          </div>
          
          {/* Controles de Voz */}
          <div className="flex items-center space-x-2">
            {/* Voz Normal */}
            <button
              onClick={toggleVoice}
              className={`p-2 rounded-lg transition-all ${
                voiceEnabled 
                  ? 'bg-green-100 text-green-600 ring-2 ring-green-500' 
                  : 'bg-gray-100 text-gray-600'
              }`}
              title="Activar/Desactivar respuestas en voz"
            >
              {voiceEnabled ? <Volume2 className="w-5 h-5" /> : <VolumeX className="w-5 h-5" />}
            </button>

            {/* VOZ CONTINUA */}
            <button
              onClick={continuousVoiceMode ? stopContinuousRecording : startContinuousRecording}
              className={`px-4 py-2 rounded-lg font-semibold flex items-center space-x-2 transition-all ${
                continuousVoiceMode
                  ? 'bg-red-500 text-white animate-pulse'
                  : 'bg-indigo-600 text-white hover:bg-indigo-700'
              }`}
              title="Modo voz continua: Tu voz → texto, Respuesta → voz"
            >
              {continuousVoiceMode ? (
                <>
                  <MicOff className="w-5 h-5" />
                  <span>Detener</span>
                </>
              ) : (
                <>
                  <Mic className="w-5 h-5" />
                  <span>Voz Continua</span>
                </>
              )}
            </button>

            {/* Indicadores */}
            {isRecording && (
              <div className="flex items-center space-x-2 px-3 py-1 bg-red-100 rounded-full">
                <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                <span className="text-xs font-medium text-red-700">Escuchando...</span>
              </div>
            )}
            
            {isSpeaking && (
              <div className="flex items-center space-x-2 px-3 py-1 bg-blue-100 rounded-full">
                <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                <span className="text-xs font-medium text-blue-700">Hablando...</span>
              </div>
            )}
          </div>
        </div>

        {/* Info Voz Continua */}
        {continuousVoiceMode && (
          <div className="mt-3 p-3 bg-gradient-to-r from-red-50 to-orange-50 border border-red-200 rounded-lg">
            <p className="text-sm text-red-800 font-medium">
              🎙️ Modo Voz Continua Activo
            </p>
            <p className="text-xs text-red-600 mt-1">
              Habla y se enviará automáticamente como texto • La respuesta se leerá en voz alta
            </p>
          </div>
        )}
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="w-24 h-24 mx-auto mb-4 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full flex items-center justify-center">
                <Bot className="w-12 h-12 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-gray-700 mb-2">
                ¡Hola! Soy tu asistente AI
              </h3>
              <p className="text-gray-500 mb-4">
                ¿En qué puedo ayudarte hoy?
              </p>
              <div className="space-y-2 text-sm text-gray-600">
                <p>💬 Escribe un mensaje</p>
                <p>🎤 Activa la voz continua para conversar</p>
                <p>📷 Envía imágenes para análisis</p>
              </div>
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className="flex items-start space-x-2 max-w-[75%]">
                  {msg.role === 'assistant' && (
                    <div className="w-8 h-8 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                      <Bot className="w-5 h-5 text-white" />
                    </div>
                  )}
                  
                  <div className={`rounded-2xl px-4 py-3 ${
                    msg.role === 'user'
                      ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}>
                    {msg.role === 'assistant' ? (
                      <div className="prose prose-sm max-w-none">
                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                      </div>
                    ) : (
                      <p className="whitespace-pre-wrap">{msg.content}</p>
                    )}
                    <div className={`text-xs mt-2 ${msg.role === 'user' ? 'text-indigo-200' : 'text-gray-500'}`}>
                      {formatTime(msg.timestamp)}
                    </div>
                  </div>
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="flex justify-start">
                <div className="flex items-start space-x-2">
                  <div className="w-8 h-8 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full flex items-center justify-center">
                    <Bot className="w-5 h-5 text-white" />
                  </div>
                  <div className="bg-gray-100 rounded-2xl px-4 py-3">
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Camera Modal */}
      {showCamera && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold">Capturar Foto</h3>
              <button onClick={stopCamera} className="text-gray-500 hover:text-gray-700">
                <X className="w-6 h-6" />
              </button>
            </div>
            <video ref={videoRef} autoPlay playsInline className="w-full rounded-lg mb-4" />
            <div className="flex justify-center space-x-4">
              <button onClick={capturePhoto} className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700">
                📸 Capturar
              </button>
              <button onClick={stopCamera} className="bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-semibold hover:bg-gray-300">
                Cancelar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4 bg-white">
        {previewUrl && (
          <div className="mb-3 relative inline-block">
            <img src={previewUrl} alt="Preview" className="h-20 w-20 object-cover rounded-lg" />
            <button onClick={removeFile} className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600">
              <X className="w-4 h-4" />
            </button>
            <div className="text-xs text-gray-600 mt-1">{selectedFile?.name}</div>
          </div>
        )}

        <form onSubmit={handleSubmit} className="flex items-end space-x-2">
          <input type="file" ref={fileInputRef} onChange={handleFileSelect} accept="image/*" className="hidden" />
          
          <div className="flex space-x-2">
            <button type="button" onClick={() => fileInputRef.current?.click()} className="p-3 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200" title="Adjuntar imagen">
              <ImageIcon className="w-5 h-5" />
            </button>
            
            <button type="button" onClick={startCamera} className="p-3 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200" title="Tomar foto">
              <Camera className="w-5 h-5" />
            </button>
          </div>

          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={continuousVoiceMode ? "Modo voz continua activo..." : "Escribe un mensaje..."}
            disabled={continuousVoiceMode}
            className="flex-1 resize-none border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-gray-100"
            rows="1"
            style={{ minHeight: '48px', maxHeight: '120px' }}
          />

          <button
            type="submit"
            disabled={(!input.trim() && !selectedFile) || loading || continuousVoiceMode}
            className="p-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:opacity-90 disabled:opacity-50 transition-opacity"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
      </div>
    </div>
  )
}
