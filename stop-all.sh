#!/bin/bash

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🛑 Stopping ArchLlama Platform..."

# Kill by PID files
if [ -f "$PROJECT_ROOT/.backend.pid" ]; then
    kill $(cat "$PROJECT_ROOT/.backend.pid") 2>/dev/null
    rm "$PROJECT_ROOT/.backend.pid"
    echo "✓ Backend stopped"
fi

if [ -f "$PROJECT_ROOT/.frontend.pid" ]; then
    kill $(cat "$PROJECT_ROOT/.frontend.pid") 2>/dev/null
    rm "$PROJECT_ROOT/.frontend.pid"
    echo "✓ Frontend stopped"
fi

# Kill by process name
pkill -f "uvicorn app.main" 2>/dev/null
pkill -f "vite" 2>/dev/null

# Kill by port
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

echo "✅ All services stopped"
