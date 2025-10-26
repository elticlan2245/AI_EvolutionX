#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 AI EVOLUTIONX - INICIO PROFESIONAL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Matar procesos anteriores
pkill -9 -f uvicorn 2>/dev/null
sudo lsof -ti:8000 | xargs sudo kill -9 2>/dev/null

# Verificar MongoDB
echo ""
echo "1. Verificando MongoDB..."
sudo docker ps | grep mongodb > /dev/null || {
    echo "   Iniciando MongoDB..."
    sudo docker start mongodb 2>/dev/null || \
    sudo docker run -d --name mongodb --restart always -p 27017:27017 mongo:7.0
}
sleep 3
echo "   ✅ MongoDB OK"

# Iniciar backend
echo ""
echo "2. Iniciando Backend..."
cd /home/kali/aievolution/ai-evolutionx-platform/backend
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > ../logs/backend_app.log 2>&1 &

echo "   Esperando 10 segundos..."
sleep 10

# Verificar
echo ""
echo "3. Verificando Backend..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "   ✅ Backend funcionando"
    curl -s http://localhost:8000/health | jq '.'
else
    echo "   ❌ Backend falló"
    echo ""
    echo "Últimos 50 logs:"
    tail -50 ../logs/backend_app.log
    exit 1
fi

# Registrar usuarios de prueba
echo ""
echo "4. Creando usuarios de prueba..."

# Admin
curl -s -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@aievolutionx.com",
    "password": "Admin123456!",
    "name": "Administrator"
  }' > /dev/null 2>&1

# Usuario de prueba
curl -s -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@aievolutionx.com",
    "password": "Test123456!",
    "name": "Test User"
  }' > /dev/null 2>&1

echo "   ✅ Usuarios creados"

# Resumen
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SISTEMA INICIADO CORRECTAMENTE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 URLs:"
echo "   Frontend:  http://localhost/"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "🔑 Credenciales de Login:"
echo ""
echo "   Usuario Admin:"
echo "     Email:    admin@aievolutionx.com"
echo "     Password: Admin123456!"
echo ""
echo "   Usuario Test:"
echo "     Email:    test@aievolutionx.com"
echo "     Password: Test123456!"
echo ""
echo "📋 Configuración:"
echo "   • MongoDB: Docker (puerto 27017)"
echo "   • Ollama: 15 modelos activos"
echo "   • Sistema de afiliados: Habilitado"
echo "   • Sistema de pagos: Configurar Stripe"
echo ""
echo "📚 Ver CONFIG.md para guía completa"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

