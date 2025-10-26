from anthropic import AsyncAnthropic
from typing import List, Dict, AsyncGenerator
import logging
import os

logger = logging.getLogger(__name__)

class AnthropicProvider:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = AsyncAnthropic(api_key=self.api_key) if self.api_key else None
        self.available_models = [
            "claude-3-5-sonnet-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]
    
    def is_available(self) -> bool:
        return self.client is not None
    
    def _convert_messages(self, messages: List[Dict]) -> tuple:
        """Convert OpenAI format to Claude format"""
        system = ""
        claude_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                claude_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        return system, claude_messages
    
    async def chat(self, model: str, messages: List[Dict], temperature: float = 0.7) -> Dict:
        if not self.is_available():
            raise Exception("Anthropic API key not configured")
        
        try:
            system, claude_messages = self._convert_messages(messages)
            
            response = await self.client.messages.create(
                model=model,
                max_tokens=4096,
                temperature=temperature,
                system=system if system else None,
                messages=claude_messages
            )
            
            return {
                "message": {
                    "role": "assistant",
                    "content": response.content[0].text
                },
                "provider": "anthropic",
                "model": model
            }
        except Exception as e:
            logger.error(f"Anthropic error: {e}")
            raise
    
    async def chat_stream(self, model: str, messages: List[Dict], temperature: float = 0.7) -> AsyncGenerator:
        if not self.is_available():
            raise Exception("Anthropic API key not configured")
        
        try:
            system, claude_messages = self._convert_messages(messages)
            
            async with self.client.messages.stream(
                model=model,
                max_tokens=4096,
                temperature=temperature,
                system=system if system else None,
                messages=claude_messages
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        except Exception as e:
            logger.error(f"Anthropic stream error: {e}")
            raise

anthropic_provider = AnthropicProvider()
