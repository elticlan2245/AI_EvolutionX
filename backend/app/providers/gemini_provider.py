import google.generativeai as genai
from typing import List, Dict, AsyncGenerator
import logging
import os
import asyncio

logger = logging.getLogger(__name__)

class GeminiProvider:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.available_models = [
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-pro"
        ]
    
    def is_available(self) -> bool:
        return self.api_key is not None
    
    def _convert_messages(self, messages: List[Dict]) -> List[Dict]:
        """Convert to Gemini format"""
        gemini_messages = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            gemini_messages.append({
                "role": role,
                "parts": [msg["content"]]
            })
        return gemini_messages
    
    async def chat(self, model: str, messages: List[Dict], temperature: float = 0.7) -> Dict:
        if not self.is_available():
            raise Exception("Google API key not configured")
        
        try:
            model_instance = genai.GenerativeModel(model)
            gemini_messages = self._convert_messages(messages)
            
            # Start chat
            chat = model_instance.start_chat(history=gemini_messages[:-1])
            
            # Send last message (sync to async wrapper)
            response = await asyncio.to_thread(
                chat.send_message,
                gemini_messages[-1]["parts"][0],
                generation_config=genai.types.GenerationConfig(temperature=temperature)
            )
            
            return {
                "message": {
                    "role": "assistant",
                    "content": response.text
                },
                "provider": "google",
                "model": model
            }
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            raise
    
    async def chat_stream(self, model: str, messages: List[Dict], temperature: float = 0.7) -> AsyncGenerator:
        if not self.is_available():
            raise Exception("Google API key not configured")
        
        try:
            model_instance = genai.GenerativeModel(model)
            gemini_messages = self._convert_messages(messages)
            
            chat = model_instance.start_chat(history=gemini_messages[:-1])
            
            response = await asyncio.to_thread(
                chat.send_message,
                gemini_messages[-1]["parts"][0],
                generation_config=genai.types.GenerationConfig(temperature=temperature),
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            logger.error(f"Gemini stream error: {e}")
            raise

gemini_provider = GeminiProvider()
