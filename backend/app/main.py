from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from .database import init_db, close_db
from .routes import chat, models, conversations, training, settings as settings_route, voice, auth, payments

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 starting ai_evolutionx platform")
    await init_db()
    yield
    logger.info("🛑 shutting down")
    await close_db()

app = FastAPI(
    title="ai_evolutionx api",
    description="next-gen ai platform with continuous learning",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(payments.router)
app.include_router(chat.router)
app.include_router(models.router)
app.include_router(conversations.router)
app.include_router(training.router)
app.include_router(settings_route.router)
app.include_router(voice.router)

@app.get("/health")
async def health_check():
    from .services.ollama_service import get_active_server
    active = await get_active_server()
    return {
        "status": "healthy",
        "services": {"mongodb": "ok", "redis": "ok", "ollama": "ok"},
        "ollama_server": active["name"] if active else None
    }

@app.get("/")
async def root():
    return {"name": "ai_evolutionx api", "version": "2.0.0", "status": "running"}
