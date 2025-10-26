#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 DIAGNÓSTICO DE AUTENTICACIÓN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. ¿Backend está corriendo?
echo ""
echo "1. BACKEND STATUS:"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "   ✅ Backend respondiendo"
    curl -s http://localhost:8000/health | jq '.'
else
    echo "   ❌ Backend NO responde"
    echo ""
    echo "   Últimos logs:"
    tail -50 logs/backend_app.log
    exit 1
fi

# 2. Ver la consola del navegador
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. ABRIR CONSOLA DEL NAVEGADOR:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   Abre Firefox y presiona F12"
echo "   Ve a la pestaña 'Console'"
echo "   Intenta registrarte"
echo "   Copia el error COMPLETO que aparezca en rojo"
echo ""
read -p "Presiona Enter cuando hayas visto el error en la consola..."

# 3. Ver logs del backend en tiempo real
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. LOGS DEL BACKEND (últimas 50 líneas):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
tail -50 logs/backend_app.log

# 4. Verificar qué URL está usando el frontend
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. URL DEL API EN EL FRONTEND:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Buscar archivos de servicios
find frontend/src -name "*.js" -o -name "*.ts" | while read file; do
    if grep -q "register\|login\|auth" "$file" 2>/dev/null; then
        echo ""
        echo "Archivo: $file"
        grep -n "localhost\|http.*8000\|/auth\|/api" "$file" | head -10
    fi
done

# 5. Probar las rutas manualmente
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. PROBAR RUTAS MANUALMENTE:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "A) Probando POST /api/auth/register:"
curl -v -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test999@test.com",
    "password": "Test123456",
    "name": "Test User"
  }' 2>&1 | grep -E "HTTP|< |{|}"

echo ""
echo ""
echo "B) Probando POST /auth/register (sin /api):"
curl -v -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test999@test.com",
    "password": "Test123456",
    "name": "Test User"
  }' 2>&1 | grep -E "HTTP|< |{|}"

# 6. Ver todas las rutas disponibles
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. TODAS LAS RUTAS DISPONIBLES:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
curl -s http://localhost:8000/openapi.json | jq -r '.paths | keys[]' | sort

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "7. NETWORK TAB EN EL NAVEGADOR:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   En Firefox, abre F12 → Network"
echo "   Intenta registrarte de nuevo"
echo "   Busca la petición que dice 'register'"
echo "   Click derecho → Copy → Copy as cURL"
echo ""
read -p "Pega el comando cURL aquí y presiona Enter: " CURL_CMD

echo ""
echo "Comando que el frontend está usando:"
echo "$CURL_CMD"

