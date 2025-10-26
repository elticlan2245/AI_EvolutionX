import redis.asyncio as redis
from loguru import logger
from typing import Optional, Any
import json

from app.config.settings import settings


class RedisClient:
    """Cliente asíncrono de Redis para AI EvolutionX"""

    client: Optional[redis.Redis] = None

    async def connect(self):
        """Conexión a Redis"""
        try:
            logger.info("🔌 Conectando a Redis...")

            # Crear conexión sin await (Redis usa conexiones perezosas)
            self.client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password,
                max_connections=settings.redis_max_connections,
                decode_responses=True
            )

            # Prueba de conexión
            await self.client.ping()
            logger.success(f"✅ Redis conectado: {settings.redis_host}:{settings.redis_port}")

        except Exception as e:
            logger.error(f"❌ Error conectando a Redis: {str(e)}")
            raise

    async def disconnect(self):
        """Desconexión de Redis"""
        if self.client:
            await self.client.close()
            logger.info("✅ Redis desconectado correctamente.")

    async def ping(self) -> bool:
        """Verifica si Redis está activo"""
        try:
            return await self.client.ping()
        except Exception:
            return False

    async def get(self, key: str) -> Optional[str]:
        """Obtiene un valor de Redis"""
        return await self.client.get(key)

    async def set(self, key: str, value: Any, expire: int = None):
        """Guarda un valor con expiración opcional"""
        await self.client.set(key, value, ex=expire)

    async def delete(self, key: str):
        """Elimina una clave"""
        await self.client.delete(key)

    async def exists(self, key: str) -> bool:
        """Verifica si una clave existe"""
        return await self.client.exists(key) > 0

    async def incr(self, key: str) -> int:
        """Incrementa el valor de una clave numérica"""
        return await self.client.incr(key)

    async def cache_json(self, key: str, data: dict, expire: int = 3600):
        """Almacena datos JSON en caché"""
        await self.client.set(key, json.dumps(data), ex=expire)

    async def get_json(self, key: str) -> Optional[dict]:
        """Obtiene datos JSON desde caché"""
        data = await self.client.get(key)
        return json.loads(data) if data else None


# Instancia global accesible
redis_client = RedisClient()
