from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from .database import init_db, close_db

# Importar solo routers que EXISTEN
from .api.auth import router as auth_router
from .api.chat import router as chat_router
from .api.models import router as models_router
from .api.conversations import router as conversations_router
from .api.voice import router as voice_router

# Routers adicionales (si existen)
try:
    from .routes.affiliates import router as affiliates_router
    HAS_AFFILIATES = True
except ImportError:
    HAS_AFFILIATES = False

try:
    from .routes.billing import router as billing_router
    HAS_BILLING = True
except ImportError:
    HAS_BILLING = False

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicialización y cierre de la aplicación"""
    logger.info("🚀 Starting AI EvolutionX Platform")
    await init_db()
    yield
    logger.info("👋 Shutting down AI EvolutionX Platform")
    await close_db()

app = FastAPI(
    title="AI EvolutionX Platform",
    description="Advanced AI Platform with Continuous Learning",
    version="2.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.0.0",
        "platform": "AI EvolutionX"
    }

# Routers principales
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(models_router)
app.include_router(conversations_router)
app.include_router(voice_router)

# Routers opcionales
if HAS_AFFILIATES:
    app.include_router(affiliates_router)
    logger.info("✅ Affiliates module loaded")

if HAS_BILLING:
    app.include_router(billing_router)
    logger.info("✅ Billing module loaded")

# Root
@app.get("/")
async def root():
    return {
        "message": "AI EvolutionX API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
