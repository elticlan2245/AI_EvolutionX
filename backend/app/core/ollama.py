import httpx
import asyncio
import json
from typing import Optional, Dict, Any, List, AsyncIterator, Union
from loguru import logger
import time

from app.config import settings


class OllamaClient:
    """Cliente avanzado de Ollama con failover LAN/WAN, reintentos y logs."""

    def __init__(self):
        self.servers = [
            {
                "url": settings.OLLAMA_LAN_URL,
                "timeout": settings.OLLAMA_TIMEOUT_LAN,
                "name": "LAN",
                "priority": 1,
            },
            {
                "url": settings.OLLAMA_WAN_URL,
                "timeout": settings.OLLAMA_TIMEOUT_WAN,
                "name": "WAN",
                "priority": 2,
            },
        ]
        self.active_server: Optional[Dict[str, Any]] = None
        self.last_check = 0
        self.check_interval = 60  # segundos

        # Log de actividad detallada
        logger.add("logs/ollama_client.log", rotation="10 MB", level="DEBUG")

    # ======================================================
    # 🔍 Detección automática del servidor activo
    # ======================================================
    async def find_active_server(self) -> Optional[Dict[str, Any]]:
        current_time = time.time()

        # Si ya hay un servidor activo y fue verificado hace poco, lo reusamos
        if self.active_server and (current_time - self.last_check) < self.check_interval:
            return self.active_server

        logger.info("🔍 Buscando servidor Ollama activo...")

        for server in sorted(self.servers, key=lambda x: x["priority"]):
            try:
                async with httpx.AsyncClient(timeout=server["timeout"]) as client:
                    start = time.time()
                    response = await client.get(f"{server['url']}/api/tags")
                    latency = time.time() - start

                    if response.status_code == 200:
                        server["latency"] = latency
                        self.active_server = server
                        self.last_check = current_time
                        logger.success(
                            f"✅ Conectado a Ollama {server['name']} ({server['url']}) "
                            f"(latencia: {latency:.2f}s)"
                        )
                        return server
            except Exception as e:
                logger.warning(f"❌ {server['name']} no disponible: {str(e)}")

        logger.error("❌ No hay servidores Ollama disponibles")
        self.active_server = None
        return None

    # ======================================================
    # ⚙️ Garantiza un servidor activo
    # ======================================================
    async def _ensure_server(self):
        if not self.active_server:
            await self.find_active_server()

        if not self.active_server:
            raise Exception("No hay servidores Ollama disponibles")

    # ======================================================
    # 💬 Chat con streaming
    # ======================================================
    async def chat_stream(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> AsyncIterator[str]:
        await self._ensure_server()
        url = f"{self.active_server['url']}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }

        try:
            async with httpx.AsyncClient(timeout=self.active_server["timeout"]) as client:
                async with client.stream("POST", url, json=payload) as response:
                    async for line in response.aiter_lines():
                        if line.strip():
                            try:
                                data = json.loads(line)
                                # Compatibilidad con formatos antiguos/nuevos
                                if "message" in data:
                                    yield data["message"].get("content", "")
                                elif "response" in data:
                                    yield data["response"]
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            logger.error(f"⚠️ Error en chat_stream: {e}")
            self.active_server = None
            await self.find_active_server()
            raise

    # ======================================================
    # 💬 Chat normal (no streaming)
    # ======================================================
    async def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Union[Dict[str, Any], AsyncIterator[str]]:
        if stream:
            return self.chat_stream(model, messages, temperature, max_tokens)

        await self._ensure_server()

        url = f"{self.active_server['url']}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }

        try:
            async with httpx.AsyncClient(timeout=self.active_server["timeout"]) as client:
                logger.debug(f"🧠 Enviando solicitud a Ollama: {payload}")
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()

                # Compatibilidad con diferentes versiones de Ollama
                content = (
                    data.get("message", {}).get("content")
                    or data.get("response")
                    or ""
                )

                if not content.strip():
                    logger.warning("⚠️ Ollama devolvió una respuesta vacía.")
                return data

        except httpx.TimeoutException:
            logger.warning("⚠️ Timeout con Ollama. Reintentando...")
            await self.find_active_server()
            await asyncio.sleep(2)
            return await self.chat(model, messages, stream, temperature, max_tokens)

        except Exception as e:
            logger.error(f"❌ Error en chat(): {e}")
            self.active_server = None
            await self.find_active_server()
            raise

    # ======================================================
    # 🧬 Generación con streaming
    # ======================================================
    async def generate_stream(self, model: str, prompt: str) -> AsyncIterator[str]:
        await self._ensure_server()
        url = f"{self.active_server['url']}/api/generate"
        payload = {"model": model, "prompt": prompt, "stream": True}

        async with httpx.AsyncClient(timeout=self.active_server["timeout"]) as client:
            async with client.stream("POST", url, json=payload) as response:
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            data = json.loads(line)
                            yield data.get("response", "")
                        except json.JSONDecodeError:
                            continue

    # ======================================================
    # 🧬 Generación sin streaming
    # ======================================================
    async def generate(
        self, model: str, prompt: str, stream: bool = False
    ) -> Union[Dict[str, Any], AsyncIterator[str]]:
        if stream:
            return self.generate_stream(model, prompt)

        await self._ensure_server()

        url = f"{self.active_server['url']}/api/generate"
        payload = {"model": model, "prompt": prompt, "stream": False}

        async with httpx.AsyncClient(timeout=self.active_server["timeout"]) as client:
            response = await client.post(url, json=payload)
            return response.json()

    # ======================================================
    # 📦 Listado y gestión de modelos
    # ======================================================
    async def list_models(self) -> Dict[str, Any]:
        await self._ensure_server()
        url = f"{self.active_server['url']}/api/tags"
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            return response.json()

    async def show_model(self, model: str) -> Dict[str, Any]:
        await self._ensure_server()
        url = f"{self.active_server['url']}/api/show"
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json={"name": model})
            return response.json()

    async def pull_model_stream(self, model: str) -> AsyncIterator[Dict[str, Any]]:
        await self._ensure_server()
        url = f"{self.active_server['url']}/api/pull"
        payload = {"name": model, "stream": True}

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=payload) as response:
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            yield json.loads(line)
                        except json.JSONDecodeError:
                            continue

    async def pull_model(self, model: str) -> AsyncIterator[Dict[str, Any]]:
        """Descarga un modelo completo (sin streaming)"""
        return self.pull_model_stream(model)


# ======================================================
# 🌐 Instancia Global
# ======================================================
ollama = OllamaClient()
