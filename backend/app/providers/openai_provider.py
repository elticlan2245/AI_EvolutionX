from openai import AsyncOpenAI
from typing import List, Dict, AsyncGenerator
import logging
import os

logger = logging.getLogger(__name__)

class OpenAIProvider:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=self.api_key) if self.api_key else None
        self.available_models = [
            "gpt-4-turbo-preview",
            "gpt-4",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k"
        ]
    
    def is_available(self) -> bool:
        return self.client is not None
    
    async def chat(self, model: str, messages: List[Dict], temperature: float = 0.7) -> Dict:
        if not self.is_available():
            raise Exception("OpenAI API key not configured")
        
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature
            )
            
            return {
                "message": {
                    "role": "assistant",
                    "content": response.choices[0].message.content
                },
                "provider": "openai",
                "model": model
            }
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            raise
    
    async def chat_stream(self, model: str, messages: List[Dict], temperature: float = 0.7) -> AsyncGenerator:
        if not self.is_available():
            raise Exception("OpenAI API key not configured")
        
        try:
            stream = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"OpenAI stream error: {e}")
            raise

openai_provider = OpenAIProvider()
