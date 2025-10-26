from loguru import logger
import sys
import os
from app.config.settings import settings  # ✅ Import correcto

def setup_logger():
    """Configura Loguru para consola y archivo."""
    logger.remove()
    
    # Asegura que el directorio de logs exista
    os.makedirs(settings.logs_dir, exist_ok=True)

    # Handler de consola
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level="DEBUG" if settings.debug else "INFO",  # ✅ minúsculas
    )

    # Handler de archivo
    logger.add(
        f"{settings.logs_dir}/backend_app.log",  # ✅ ruta corregida
        rotation="100 MB",
        retention="7 days",
        level="DEBUG" if settings.debug else "INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
    )

    logger.success("📄 Logger inicializado correctamente.")

    return logger
