import httpx
import asyncio
from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)

OLLAMA_SERVERS = [
    {"url": "http://192.168.50.123:11434", "timeout": 5, "name": "LAN"},
    {"url": "http://iaevolutionxm.asuscomm.com:11434", "timeout": 15, "name": "WAN"}
]

_active_server = None

async def get_active_server() -> Optional[Dict]:
    """Get active Ollama server with failover"""
    global _active_server
    
    if _active_server:
        try:
            async with httpx.AsyncClient(timeout=2) as client:
                response = await client.get(f"{_active_server['url']}/api/tags")
                if response.status_code == 200:
                    return _active_server
        except:
            pass
    
    for server in OLLAMA_SERVERS:
        try:
            async with httpx.AsyncClient(timeout=server["timeout"]) as client:
                response = await client.get(f"{server['url']}/api/tags")
                if response.status_code == 200:
                    _active_server = server
                    logger.info(f"✅ Connected to {server['name']}: {server['url']}")
                    return server
        except Exception as e:
            logger.warning(f"❌ {server['name']} unavailable")
            continue
    
    return None

async def list_models() -> List[Dict]:
    """List available models"""
    server = await get_active_server()
    if not server:
        return []
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{server['url']}/api/tags")
            if response.status_code == 200:
                data = response.json()
                return data.get("models", [])
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        return []

async def chat_completion(
    model: str,
    messages: List[Dict],
    stream: bool = False,
    temperature: float = 0.7,
    max_tokens: int = 2048
) -> Dict:
    """Send chat completion request"""
    server = await get_active_server()
    if not server:
        raise Exception("No Ollama server available")
    
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{server['url']}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": stream,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Ollama error: {response.status_code}")
    except Exception as e:
        logger.error(f"Chat completion error: {e}")
        raise
