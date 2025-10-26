from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure
from loguru import logger
from typing import Optional

from app.config.settings import settings


class MongoDB:
    """Cliente asíncrono de MongoDB para AI EvolutionX"""

    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    async def connect(self):
        """Conexión a MongoDB"""
        try:
            logger.info("🔌 Conectando a MongoDB...")

            self.client = AsyncIOMotorClient(
                settings.mongodb_url,
                maxPoolSize=settings.mongodb_max_pool_size,
                minPoolSize=settings.mongodb_min_pool_size
            )
            self.db = self.client[settings.mongodb_db]

            # Test de conexión
            await self.client.admin.command("ping")

            # Crear índices
            await self._create_indexes()

            logger.success(f"✅ MongoDB conectado: {settings.mongodb_url}")

        except ConnectionFailure as e:
            logger.error(f"❌ Error conectando a MongoDB: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"❌ Error inesperado de MongoDB: {str(e)}")
            raise

    async def _create_indexes(self):
        """Crea índices automáticos en las colecciones principales"""
        if self.db is None:
            logger.warning("⚠️ No se puede crear índices: base de datos no inicializada.")
            return

        try:
            # Conversations
            await self.db.conversations.create_index("user_id")
            await self.db.conversations.create_index("created_at")
            await self.db.conversations.create_index(
                [("user_id", 1), ("created_at", -1)]
            )

            # Training data
            await self.db.training_data.create_index("quality_score")
            await self.db.training_data.create_index("created_at")
            await self.db.training_data.create_index("used_in_training")

            # Users
            await self.db.users.create_index("email", unique=True)
            await self.db.users.create_index("username", unique=True)

            logger.info("✅ Índices MongoDB creados correctamente.")

        except Exception as e:
            logger.error(f"⚠️ No se pudieron crear los índices: {str(e)}")

    async def disconnect(self):
        """Desconexión de MongoDB"""
        if self.client:
            self.client.close()
            logger.info("✅ MongoDB desconectado correctamente.")

    async def ping(self) -> bool:
        """Verifica si la conexión está activa"""
        try:
            await self.client.admin.command("ping")
            return True
        except Exception:
            return False


# Instancia global
mongodb = MongoDB()
