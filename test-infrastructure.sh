#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 PRUEBA DE INFRAESTRUCTURA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ERRORS=0

# 1. Docker
echo ""
echo "1. DOCKER..."
if command -v docker &> /dev/null; then
    echo "   ✅ Docker instalado: $(docker --version)"
    
    # Verificar servicio
    if sudo systemctl is-active docker &> /dev/null; then
        echo "   ✅ Docker service activo"
    else
        echo "   ⚠️  Docker service inactivo, iniciando..."
        sudo systemctl start docker
        sleep 2
    fi
else
    echo "   ❌ Docker NO instalado"
    ERRORS=$((ERRORS + 1))
fi

# 2. MongoDB Docker
echo ""
echo "2. MONGODB..."
if sudo docker ps | grep mongodb &> /dev/null; then
    echo "   ✅ MongoDB container running"
    
    # Test conexión
    if sudo docker exec mongodb mongosh --eval "db.version()" &> /dev/null; then
        VERSION=$(sudo docker exec mongodb mongosh --quiet --eval "db.version()")
        echo "   ✅ MongoDB respondiendo: $VERSION"
    else
        echo "   ❌ MongoDB no responde"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo "   ⚠️  MongoDB container no está corriendo"
    echo "   Intentando iniciar..."
    
    # Limpiar container viejo si existe
    sudo docker rm -f mongodb 2>/dev/null
    
    # Iniciar nuevo
    sudo docker run -d \
      --name mongodb \
      --restart always \
      -p 27017:27017 \
      -v /home/kali/aievolution/mongodb-data:/data/db \
      mongo:7.0
    
    sleep 5
    
    if sudo docker ps | grep mongodb &> /dev/null; then
        echo "   ✅ MongoDB iniciado correctamente"
    else
        echo "   ❌ No se pudo iniciar MongoDB"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 3. Ollama
echo ""
echo "3. OLLAMA..."
if curl -s http://localhost:11434/api/tags &> /dev/null; then
    MODELS=$(curl -s http://localhost:11434/api/tags | jq '.models | length' 2>/dev/null)
    echo "   ✅ Ollama activo con $MODELS modelos"
else
    echo "   ❌ Ollama no responde"
    ERRORS=$((ERRORS + 1))
fi

# 4. Backend
echo ""
echo "4. BACKEND..."
if curl -s http://localhost:8000/health &> /dev/null; then
    echo "   ✅ Backend respondiendo"
    curl -s http://localhost:8000/health | jq '.'
else
    echo "   ⚠️  Backend no responde"
    echo "   Estado del proceso:"
    ps aux | grep uvicorn | grep -v grep || echo "   No hay proceso uvicorn"
    
    echo ""
    echo "   Ver últimos logs:"
    tail -20 /home/kali/aievolution/ai-evolutionx-platform/logs/backend_app.log 2>/dev/null || echo "   No hay logs"
fi

# 5. NGINX
echo ""
echo "5. NGINX..."
if sudo systemctl is-active nginx &> /dev/null; then
    echo "   ✅ NGINX activo"
    
    if curl -I http://localhost/ 2>&1 | grep "200 OK" &> /dev/null; then
        echo "   ✅ Frontend accesible"
    else
        echo "   ⚠️  Frontend no responde correctamente"
    fi
else
    echo "   ❌ NGINX inactivo"
    ERRORS=$((ERRORS + 1))
fi

# 6. Archivos clave
echo ""
echo "6. ARCHIVOS..."
FILES=(
    "/home/kali/aievolution/ai-evolutionx-platform/backend/.env"
    "/home/kali/aievolution/ai-evolutionx-platform/backend/app/main.py"
    "/home/kali/aievolution/ai-evolutionx-platform/frontend/dist/index.html"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (falta)"
        ERRORS=$((ERRORS + 1))
    fi
done

# Resumen
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "✅ TODAS LAS PRUEBAS PASARON"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🎯 SISTEMA LISTO PARA:"
    echo "   1. Agregar sistema de afiliados"
    echo "   2. Integrar pagos con Stripe"
    echo "   3. Conectar Claude API"
    echo "   4. Generar APK"
else
    echo "❌ HAY $ERRORS ERRORES QUE CORREGIR"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "🔧 SIGUIENTE PASO: Arreglar los errores marcados arriba"
fi

echo ""

