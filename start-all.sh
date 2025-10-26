#!/bin/bash

export TERM=xterm-256color
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Activar venv si existe
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "../venv" ]; then
    source ../venv/bin/activate
fi

echo -e "${CYAN}╔═══════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}     ${BOLD}🚀 AI_EVOLUTIONX PLATFORM 🚀${NC}     ${CYAN}║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════╝${NC}"

# Check services
echo -e "[$(date '+%H:%M:%S')] ${YELLOW}🔍 Verificando servicios...${NC}"
if pgrep -x mongod > /dev/null; then
    echo -e "${GREEN}ℹ ✓ MongoDB running${NC}"
else
    echo -e "${RED}✗ MongoDB not running${NC}"
    exit 1
fi

if pgrep -x redis-server > /dev/null; then
    echo -e "${GREEN}ℹ ✓ Redis running${NC}"
else
    echo -e "${RED}✗ Redis not running${NC}"
    exit 1
fi

# Start Backend
echo -e "[$(date '+%H:%M:%S')] ${YELLOW}🔧 Starting Backend...${NC}"
cd backend

# Limpiar puerto 8000 si está ocupado
lsof -ti:8000 | xargs kill -9 2>/dev/null

nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > ../logs/backend/app.log 2>&1 &
BACKEND_PID=$!
sleep 3

if ps -p $BACKEND_PID > /dev/null 2>&1; then
    echo -e "${GREEN}ℹ ✓ Backend started (PID: $BACKEND_PID)${NC}"
else
    echo -e "${RED}✗ Backend failed to start${NC}"
    echo -e "${RED}Check logs: tail -f $SCRIPT_DIR/logs/backend/app.log${NC}"
    exit 1
fi
cd ..

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "     ${GREEN}✅ AI_EVOLUTIONX IS RUNNING! ✅${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BOLD}🌐 Public URL:${NC}   http://iaevolutionxm.asuscomm.com"
echo -e "${BOLD}🔧 Backend:${NC}     http://localhost:8000"
echo -e "${BOLD}📚 API Docs:${NC}    http://localhost:8000/docs"
echo -e "${BOLD}🏥 Health:${NC}      http://localhost:8000/health"
echo ""
echo -e "${BOLD}📝 Logs:${NC}"
echo -e "   Backend:  tail -f $SCRIPT_DIR/logs/backend/app.log"
echo ""
echo -e "${BOLD}🛑 To stop:${NC}   ./stop-all.sh"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
