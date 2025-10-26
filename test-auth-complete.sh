#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 TEST COMPLETO DE AUTENTICACIÓN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Test Backend Health
echo ""
echo "1. BACKEND HEALTH:"
curl -s http://localhost:8000/health | jq '.'

# 2. Ver rutas disponibles
echo ""
echo "2. RUTAS DE AUTH DISPONIBLES:"
curl -s http://localhost:8000/openapi.json | jq -r '.paths | keys[] | select(contains("auth"))'

# 3. Test REGISTER con TODOS los campos
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. TEST REGISTER (con username, email, password, name):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

REGISTER_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "newuser@test.com",
    "password": "Test123456",
    "name": "New Test User"
  }')

HTTP_CODE=$(echo "$REGISTER_RESPONSE" | grep "HTTP_CODE" | cut -d: -f2)
BODY=$(echo "$REGISTER_RESPONSE" | grep -v "HTTP_CODE")

echo "HTTP Code: $HTTP_CODE"
echo "Response:"
echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"

# 4. Test LOGIN con usuario existente
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. TEST LOGIN (admin@aievolutionx.com):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

LOGIN_RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@aievolutionx.com",
    "password": "Admin123456"
  }')

HTTP_CODE=$(echo "$LOGIN_RESPONSE" | grep "HTTP_CODE" | cut -d: -f2)
BODY=$(echo "$LOGIN_RESPONSE" | grep -v "HTTP_CODE")

echo "HTTP Code: $HTTP_CODE"
echo "Response:"
echo "$BODY" | jq '.' 2>/dev/null || echo "$BODY"

if echo "$BODY" | grep -q "access_token"; then
    echo ""
    echo "✅ LOGIN EXITOSO"
    TOKEN=$(echo "$BODY" | jq -r '.access_token')
    echo "Token: ${TOKEN:0:50}..."
else
    echo ""
    echo "❌ LOGIN FALLÓ"
fi

# 5. Ver backend logs
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. ÚLTIMOS LOGS DEL BACKEND:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
tail -30 logs/backend_app.log

