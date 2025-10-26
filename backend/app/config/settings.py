from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    # ⚙️ General server configuration
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    debug: bool = Field(default=True)
    workers: int = Field(default=4)
    reload: bool = Field(default=True)


    # 🧠 Ollama configuration
    ollama_lan_url: str = Field(default="http://192.168.50.123:11434", description="Dirección LAN del servidor Ollama")
    ollama_wan_url: str = Field(default="http://192.168.50.123:11434", description="Dirección WAN o pública del servidor Ollama")
    ollama_timeout_lan: int = Field(default=120, description="Timeout para conexión LAN en segundos")
    ollama_timeout_wan: int = Field(default=180, description="Timeout para conexión WAN en segundos")
    ollama_models: str = Field(default="/home/kali/Disco8TB/ollama_models", description="Ruta local donde se almacenan los modelos Ollama")
    ollama_default_model: str = Field(default="llama3.1:8b", description="Modelo predeterminado de Ollama")


    # 🗄️ MongoDB configuration
    mongodb_url: str = Field(default="mongodb://localhost:27017")
    mongodb_db: str = Field(default="aievolutionx")
    mongodb_max_pool_size: int = Field(default=100)
    mongodb_min_pool_size: int = Field(default=10)

    # ⚡ Redis configuration
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_db: int = Field(default=0)
    redis_password: str = Field(default="")
    redis_max_connections: int = Field(default=50)

    # 🔐 JWT security
    secret_key: str = Field(default="f8135c8249a823186887eb8e555797d56f185b6e61ad472")
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=43200)
    refresh_token_expire_days: int = Field(default=30)

    # 🌐 CORS
    cors_origins: List[str] = Field(default=["http://localhost:3000", "http://localhost:5173"])

    # 🧩 Training and AI config
    auto_training_enabled: bool = Field(default=True)
    min_samples_for_training: int = Field(default=100)
    max_samples_per_training: int = Field(default=500)
    training_interval_hours: int = Field(default=12)
    quality_threshold: float = Field(default=0.7)
    lora_rank: int = Field(default=8)
    lora_alpha: int = Field(default=16)
    learning_rate: float = Field(default=1e-5)
    batch_size: int = Field(default=4)
    epochs: int = Field(default=1)

    # 📂 Paths
    data_dir: str = Field(default="../data")
    models_dir: str = Field(default="../models")
    logs_dir: str = Field(default="../logs")
    cache_dir: str = Field(default="../data/cache")

    # ⏱️ Rate limits
    rate_limit_per_minute: int = Field(default=60)
    rate_limit_per_hour: int = Field(default=1000)

    # 📊 Metrics
    enable_metrics: bool = Field(default=True)
    metrics_port: int = Field(default=9090)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# ✅ Global instance
settings = Settings()

if __name__ == "__main__":
    print("✅ Configuración cargada correctamente\n")
    for key, value in settings.__dict__.items():
        print(f"{key} = {value}")
