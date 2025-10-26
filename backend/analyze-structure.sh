#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 ANÁLISIS COMPLETO DE LA ESTRUCTURA"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "1. ESTRUCTURA DE DIRECTORIOS:"
tree -L 3 -I '__pycache__|*.pyc|node_modules' app/

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. ARCHIVOS EN app/:"
find app/ -name "*.py" | sort

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. IMPORTS EN main.py:"
grep "^from\|^import" app/main.py

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. MÓDULOS QUE FALTAN:"
echo ""

# Verificar cada import de main.py
for module in auth chat models conversations voice; do
    if [ -f "app/api/${module}.py" ]; then
        echo "✅ app/api/${module}.py existe"
    else
        echo "❌ app/api/${module}.py FALTA"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. REFERENCIAS A SETTINGS ANTIGUAS:"
grep -r "OLLAMA_LAN_URL\|OLLAMA_WAN_URL\|OLLAMA_TIMEOUT" app/ 2>/dev/null || echo "✅ No hay referencias antiguas"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. ARCHIVOS DE CONFIGURACIÓN:"
ls -la app/config/ 2>/dev/null || echo "❌ No existe app/config/"
ls -la .env 2>/dev/null || echo "❌ No existe .env"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

