#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 AI_EVOLUTIONX PLATFORM - AUDITORÍA COMPLETA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ============================================
# PARTE 1: SERVICIOS DEL SISTEMA
# ============================================
echo "📋 PARTE 1: VERIFICACIÓN DE SERVICIOS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "1.1 - MongoDB:"
if systemctl is-active --quiet mongodb; then
    echo "   ✅ RUNNING"
    mongo --eval "db.adminCommand('ping')" --quiet 2>/dev/null && echo "   ✅ RESPONDING" || echo "   ⚠️  NOT RESPONDING"
else
    echo "   ❌ NOT RUNNING"
    echo "   💡 Fix: sudo systemctl start mongodb"
fi

echo ""
echo "1.2 - Redis:"
if systemctl is-active --quiet redis-server; then
    echo "   ✅ RUNNING"
    redis-cli ping 2>/dev/null | grep -q PONG && echo "   ✅ RESPONDING" || echo "   ⚠️  NOT RESPONDING"
else
    echo "   ❌ NOT RUNNING"
    echo "   💡 Fix: sudo systemctl start redis-server"
fi

echo ""
echo "1.3 - Ollama:"
if pgrep -x "ollama" > /dev/null; then
    echo "   ✅ RUNNING"
    curl -s http://localhost:11434/api/tags > /dev/null && echo "   ✅ RESPONDING" || echo "   ⚠️  NOT RESPONDING"
else
    echo "   ❌ NOT RUNNING"
    echo "   💡 Fix: systemctl start ollama"
fi

echo ""
echo "1.4 - NGINX:"
if systemctl is-active --quiet nginx; then
    echo "   ✅ RUNNING"
    curl -s -o /dev/null -w "%{http_code}" http://localhost/ | grep -q 200 && echo "   ✅ RESPONDING" || echo "   ⚠️  NOT RESPONDING"
else
    echo "   ❌ NOT RUNNING"
    echo "   💡 Fix: sudo systemctl start nginx"
fi

echo ""
echo "1.5 - Backend (Uvicorn):"
if lsof -i :8000 > /dev/null 2>&1; then
    echo "   ✅ RUNNING on port 8000"
    curl -s http://localhost:8000/health > /dev/null && echo "   ✅ RESPONDING" || echo "   ⚠️  NOT RESPONDING"
else
    echo "   ❌ NOT RUNNING"
    echo "   💡 Fix: cd backend && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
fi

# ============================================
# PARTE 2: ESTRUCTURA DEL BACKEND
# ============================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 PARTE 2: ESTRUCTURA DEL BACKEND"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "2.1 - Archivos principales:"
[ -f "backend/app/main.py" ] && echo "   ✅ main.py" || echo "   ❌ main.py MISSING"
[ -f "backend/app/database.py" ] && echo "   ✅ database.py" || echo "   ❌ database.py MISSING"
[ -f "backend/app/auth.py" ] && echo "   ✅ auth.py" || echo "   ❌ auth.py MISSING"
[ -f "backend/app/config_payments.py" ] && echo "   ✅ config_payments.py" || echo "   ❌ config_payments.py MISSING"

echo ""
echo "2.2 - Rutas (routes):"
for route in chat models conversations training settings voice auth payments; do
    if [ -f "backend/app/routes/${route}.py" ]; then
        echo "   ✅ ${route}.py"
    else
        echo "   ❌ ${route}.py MISSING"
    fi
done

echo ""
echo "2.3 - Modelos (models):"
for model in user conversation training; do
    if [ -f "backend/app/models/${model}.py" ]; then
        echo "   ✅ ${model}.py"
    else
        echo "   ❌ ${model}.py MISSING"
    fi
done

echo ""
echo "2.4 - Servicios:"
[ -f "backend/app/services/ollama_service.py" ] && echo "   ✅ ollama_service.py" || echo "   ❌ ollama_service.py MISSING"

echo ""
echo "2.5 - Test de imports Python:"
cd backend
python3 << 'PYEOF'
import sys
errors = []

print("\n   Testeando imports...\n")

try:
    from app.main import app
    print("   ✅ app.main")
except Exception as e:
    print(f"   ❌ app.main: {e}")
    errors.append(("app.main", str(e)))

try:
    from app.auth import get_current_user
    print("   ✅ app.auth")
except Exception as e:
    print(f"   ❌ app.auth: {e}")
    errors.append(("app.auth", str(e)))

try:
    from app.models.user import User, UserRegister
    print("   ✅ app.models.user")
except Exception as e:
    print(f"   ❌ app.models.user: {e}")
    errors.append(("app.models.user", str(e)))

try:
    from app.routes import chat, auth, models
    print("   ✅ app.routes")
except Exception as e:
    print(f"   ❌ app.routes: {e}")
    errors.append(("app.routes", str(e)))

if errors:
    print("\n   ⚠️  ERRORES DE IMPORTACIÓN:")
    for module, error in errors:
        print(f"      • {module}: {error}")
    sys.exit(1)
else:
    print("\n   ✅ Todos los imports OK")
    sys.exit(0)
PYEOF

BACKEND_IMPORT_STATUS=$?
cd ..

# ============================================
# PARTE 3: ESTRUCTURA DEL FRONTEND
# ============================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 PARTE 3: ESTRUCTURA DEL FRONTEND"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "3.1 - Archivos principales:"
[ -f "frontend/src/App.jsx" ] && echo "   ✅ App.jsx" || echo "   ❌ App.jsx MISSING"
[ -f "frontend/src/main.jsx" ] && echo "   ✅ main.jsx" || echo "   ❌ main.jsx MISSING"
[ -f "frontend/src/config/api.js" ] && echo "   ✅ config/api.js" || echo "   ❌ config/api.js MISSING"

echo ""
echo "3.2 - Páginas:"
for page in Auth ChatHistory TrainingDashboard Settings; do
    if [ -f "frontend/src/pages/${page}.jsx" ]; then
        echo "   ✅ ${page}.jsx"
    else
        echo "   ❌ ${page}.jsx MISSING"
    fi
done

echo ""
echo "3.3 - Componentes:"
for comp in ChatInterface ModelSelector; do
    if [ -f "frontend/src/components/${comp}.jsx" ]; then
        echo "   ✅ ${comp}.jsx"
    else
        echo "   ❌ ${comp}.jsx MISSING"
    fi
done

echo ""
echo "3.4 - Store:"
[ -f "frontend/src/stores/useStore.js" ] && echo "   ✅ useStore.js" || echo "   ❌ useStore.js MISSING"

echo ""
echo "3.5 - Build del frontend:"
if [ -d "frontend/dist" ] && [ -f "frontend/dist/index.html" ]; then
    echo "   ✅ Dist generado"
    echo "   📦 Tamaño: $(du -sh frontend/dist | cut -f1)"
    echo "   📄 Archivos: $(find frontend/dist -type f | wc -l)"
else
    echo "   ❌ Dist NO generado"
    echo "   💡 Fix: cd frontend && npm run build"
fi

# ============================================
# PARTE 4: CONFIGURACIÓN DE NGINX
# ============================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 PARTE 4: CONFIGURACIÓN DE NGINX"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "/etc/nginx/sites-available/aievolutionx" ]; then
    echo ""
    echo "4.1 - Archivo de configuración: ✅ EXISTE"
    echo ""
    echo "4.2 - Contenido relevante:"
    echo "   Root: $(grep -m1 'root' /etc/nginx/sites-available/aievolutionx | awk '{print $2}' | tr -d ';')"
    echo "   Server name: $(grep -m1 'server_name' /etc/nginx/sites-available/aievolutionx | awk '{print $2,$3}' | tr -d ';')"
    
    if [ -L "/etc/nginx/sites-enabled/aievolutionx" ]; then
        echo "   ✅ Symlink habilitado"
    else
        echo "   ❌ Symlink NO habilitado"
        echo "   💡 Fix: sudo ln -s /etc/nginx/sites-available/aievolutionx /etc/nginx/sites-enabled/"
    fi
else
    echo "   ❌ Configuración de NGINX NO EXISTE"
fi

# ============================================
# PARTE 5: TESTS DE ENDPOINTS
# ============================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 PARTE 5: TESTS DE ENDPOINTS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "5.1 - Backend Health:"
HEALTH=$(curl -s -w "\n%{http_code}" http://localhost:8000/health 2>/dev/null)
HTTP_CODE=$(echo "$HEALTH" | tail -1)
RESPONSE=$(echo "$HEALTH" | head -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✅ /health [200]"
    echo "   Response: $RESPONSE"
else
    echo "   ❌ /health [$HTTP_CODE]"
    echo "   💡 Backend no responde"
fi

echo ""
echo "5.2 - Backend Models:"
MODELS=$(curl -s -w "\n%{http_code}" http://localhost:8000/api/models 2>/dev/null)
HTTP_CODE=$(echo "$MODELS" | tail -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✅ /api/models [200]"
    MODEL_COUNT=$(echo "$MODELS" | head -1 | grep -o '"name"' | wc -l)
    echo "   Modelos disponibles: $MODEL_COUNT"
else
    echo "   ❌ /api/models [$HTTP_CODE]"
fi

echo ""
echo "5.3 - Frontend (NGINX):"
FRONTEND=$(curl -s -w "\n%{http_code}" http://localhost/ 2>/dev/null)
HTTP_CODE=$(echo "$FRONTEND" | tail -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✅ Frontend [200]"
    if echo "$FRONTEND" | grep -q "AI_EvolutionX"; then
        echo "   ✅ Contenido correcto detectado"
    else
        echo "   ⚠️  Contenido sospechoso"
    fi
else
    echo "   ❌ Frontend [$HTTP_CODE]"
fi

# ============================================
# PARTE 6: LOGS Y DIAGNÓSTICO
# ============================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 PARTE 6: LOGS Y DIAGNÓSTICO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "6.1 - Últimas líneas del backend log:"
if [ -f "logs/backend/app.log" ]; then
    echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    tail -10 logs/backend/app.log | sed 's/^/   /'
    echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "   ⚠️  Log no encontrado"
fi

echo ""
echo "6.2 - Errores recientes de NGINX:"
if [ -f "/var/log/nginx/error.log" ]; then
    echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    sudo tail -5 /var/log/nginx/error.log | sed 's/^/   /'
    echo "   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "   ⚠️  Log no encontrado"
fi

# ============================================
# RESUMEN FINAL
# ============================================
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 RESUMEN Y DIAGNÓSTICO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ISSUES=0

# Verificar servicios críticos
if ! systemctl is-active --quiet mongodb; then
    echo "❌ MongoDB no está corriendo"
    ISSUES=$((ISSUES + 1))
fi

if ! systemctl is-active --quiet redis-server; then
    echo "❌ Redis no está corriendo"
    ISSUES=$((ISSUES + 1))
fi

if ! lsof -i :8000 > /dev/null 2>&1; then
    echo "❌ Backend no está corriendo en puerto 8000"
    ISSUES=$((ISSUES + 1))
fi

if [ $BACKEND_IMPORT_STATUS -ne 0 ]; then
    echo "❌ Backend tiene errores de importación"
    ISSUES=$((ISSUES + 1))
fi

if [ ! -d "frontend/dist" ]; then
    echo "❌ Frontend no está compilado"
    ISSUES=$((ISSUES + 1))
fi

if [ $ISSUES -eq 0 ]; then
    echo ""
    echo "✅ ¡TODO CORRECTO! La plataforma debería funcionar."
    echo ""
    echo "Accede a: http://localhost/"
else
    echo ""
    echo "⚠️  Se encontraron $ISSUES problemas."
    echo ""
    echo "COMANDOS DE SOLUCIÓN RÁPIDA:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    if ! systemctl is-active --quiet mongodb; then
        echo "sudo systemctl start mongodb"
    fi
    
    if ! systemctl is-active --quiet redis-server; then
        echo "sudo systemctl start redis-server"
    fi
    
    if ! lsof -i :8000 > /dev/null 2>&1; then
        echo "cd backend && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &"
    fi
    
    if [ ! -d "frontend/dist" ]; then
        echo "cd frontend && npm run build && sudo chmod -R 755 dist/"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Auditoría completada - $(date)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
