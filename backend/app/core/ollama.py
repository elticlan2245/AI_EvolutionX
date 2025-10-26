import httpx
import json
from typing import Dict, List, Optional, AsyncGenerator
import asyncio
from datetime import datetime
import logging

from app.config.settings import settings

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self):
        """Initialize Ollama client with configuration"""
        self.base_url = settings.ollama_host
        self.timeout = httpx.Timeout(300.0, connect=10.0)
        
        # Endpoints
        self.endpoints = {
            "generate": f"{self.base_url}/api/generate",
            "chat": f"{self.base_url}/api/chat",
            "tags": f"{self.base_url}/api/tags",
            "show": f"{self.base_url}/api/show",
            "pull": f"{self.base_url}/api/pull",
            "embeddings": f"{self.base_url}/api/embeddings"
        }
        
        logger.info(f"🤖 Ollama client initialized: {self.base_url}")
    
    async def list_models(self) -> List[Dict]:
        """Get list of available models"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(self.endpoints["tags"])
                response.raise_for_status()
                data = response.json()
                
                models = []
                for model in data.get("models", []):
                    models.append({
                        "name": model.get("name"),
                        "model": model.get("model"),
                        "size": model.get("size"),
                        "modified_at": model.get("modified_at"),
                        "digest": model.get("digest"),
                        "details": model.get("details", {})
                    })
                
                logger.info(f"✅ Found {len(models)} models")
                return models
                
        except Exception as e:
            logger.error(f"❌ Error listing models: {e}")
            return []
    
    async def generate_stream(
        self,
        model: str,
        prompt: str,
        system: Optional[str] = None,
        context: Optional[List] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> AsyncGenerator[str, None]:
        """Generate response with streaming"""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": temperature,
                }
            }
            
            if system:
                payload["system"] = system
            
            if context:
                payload["context"] = context
            
            if max_tokens:
                payload["options"]["num_predict"] = max_tokens
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    self.endpoints["generate"],
                    json=payload
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                if "response" in data:
                                    yield data["response"]
                                
                                if data.get("done", False):
                                    break
                                    
                            except json.JSONDecodeError:
                                continue
                                
        except Exception as e:
            logger.error(f"❌ Error in generate_stream: {e}")
            yield f"Error: {str(e)}"
    
    async def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        stream: bool = False
    ) -> Dict:
        """Chat completion"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": stream,
                "options": {
                    "temperature": temperature
                }
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.endpoints["chat"],
                    json=payload
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"❌ Error in chat: {e}")
            raise
    
    async def chat_stream(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7
    ) -> AsyncGenerator[str, None]:
        """Chat completion with streaming"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": True,
                "options": {
                    "temperature": temperature
                }
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    self.endpoints["chat"],
                    json=payload
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                
                                if "message" in data and "content" in data["message"]:
                                    yield data["message"]["content"]
                                
                                if data.get("done", False):
                                    break
                                    
                            except json.JSONDecodeError:
                                continue
                                
        except Exception as e:
            logger.error(f"❌ Error in chat_stream: {e}")
            yield f"Error: {str(e)}"
    
    async def get_model_info(self, model: str) -> Dict:
        """Get detailed information about a model"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.endpoints["show"],
                    json={"name": model}
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"❌ Error getting model info: {e}")
            return {}
    
    async def pull_model(self, model: str) -> AsyncGenerator[Dict, None]:
        """Pull/download a model with progress"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(3600.0)) as client:
                async with client.stream(
                    "POST",
                    self.endpoints["pull"],
                    json={"name": model, "stream": True}
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                data = json.loads(line)
                                yield data
                                
                                if data.get("status") == "success":
                                    break
                                    
                            except json.JSONDecodeError:
                                continue
                                
        except Exception as e:
            logger.error(f"❌ Error pulling model: {e}")
            yield {"status": "error", "error": str(e)}
    
    async def generate_embeddings(
        self,
        model: str,
        text: str
    ) -> Optional[List[float]]:
        """Generate embeddings for text"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.endpoints["embeddings"],
                    json={
                        "model": model,
                        "prompt": text
                    }
                )
                response.raise_for_status()
                data = response.json()
                return data.get("embedding")
                
        except Exception as e:
            logger.error(f"❌ Error generating embeddings: {e}")
            return None
    
    async def health_check(self) -> bool:
        """Check if Ollama is accessible"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except:
            return False

# Singleton instance
ollama = OllamaClient()
