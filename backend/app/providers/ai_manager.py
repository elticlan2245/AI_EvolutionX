from typing import List, Dict, AsyncGenerator
import logging

from .openai_provider import openai_provider
from .anthropic_provider import anthropic_provider
from .gemini_provider import gemini_provider
from ..core.ollama import ollama

logger = logging.getLogger(__name__)

class AIManager:
    def __init__(self):
        self.providers = {
            "openai": openai_provider,
            "anthropic": anthropic_provider,
            "google": gemini_provider,
            "ollama": ollama
        }
    
    def get_provider_for_model(self, model: str) -> tuple:
        """Detecta el provider basándose en el nombre del modelo"""
        if model.startswith("gpt"):
            return "openai", openai_provider
        elif model.startswith("claude"):
            return "anthropic", anthropic_provider
        elif model.startswith("gemini"):
            return "google", gemini_provider
        else:
            return "ollama", ollama
    
    async def get_available_models(self) -> List[Dict]:
        """Obtiene todos los modelos disponibles"""
        models = []
        
        # Ollama models
        try:
            ollama_models = await ollama.list_models()
            for model in ollama_models:
                models.append({
                    **model,
                    "provider": "ollama",
                    "price": "free"
                })
        except Exception as e:
            logger.warning(f"Ollama not available: {e}")
        
        # OpenAI models
        if openai_provider.is_available():
            for model in openai_provider.available_models:
                models.append({
                    "name": model,
                    "provider": "openai",
                    "price": "paid"
                })
        
        # Anthropic models
        if anthropic_provider.is_available():
            for model in anthropic_provider.available_models:
                models.append({
                    "name": model,
                    "provider": "anthropic",
                    "price": "paid"
                })
        
        # Gemini models  
        if gemini_provider.is_available():
            for model in gemini_provider.available_models:
                models.append({
                    "name": model,
                    "provider": "google",
                    "price": "free_limited"
                })
        
        return models
    
    async def chat(self, model: str, messages: List[Dict], temperature: float = 0.7, user_plan: str = "free") -> Dict:
        """Chat unificado"""
        provider_name, provider = self.get_provider_for_model(model)
        
        # Validar permisos
        if provider_name != "ollama" and user_plan == "free":
            raise Exception("API models require a paid plan")
        
        logger.info(f"Using {provider_name} for model {model}")
        
        try:
            return await provider.chat(model, messages, temperature)
        except Exception as e:
            logger.error(f"Error with {provider_name}: {e}")
            # Fallback a Ollama
            if provider_name != "ollama":
                logger.info("Falling back to Ollama")
                ollama_models = await ollama.list_models()
                if ollama_models:
                    return await ollama.chat(ollama_models[0]["name"], messages, temperature)
            raise
    
    async def chat_stream(self, model: str, messages: List[Dict], temperature: float = 0.7, user_plan: str = "free") -> AsyncGenerator:
        """Chat streaming unificado"""
        provider_name, provider = self.get_provider_for_model(model)
        
        if provider_name != "ollama" and user_plan == "free":
            raise Exception("API models require a paid plan")
        
        logger.info(f"Streaming from {provider_name} for model {model}")
        
        try:
            async for chunk in provider.chat_stream(model, messages, temperature):
                yield chunk
        except Exception as e:
            logger.error(f"Stream error: {e}")
            if provider_name != "ollama":
                logger.info("Falling back to Ollama")
                ollama_models = await ollama.list_models()
                if ollama_models:
                    async for chunk in ollama.chat_stream(ollama_models[0]["name"], messages, temperature):
                        yield chunk
            else:
                raise

ai_manager = AIManager()
