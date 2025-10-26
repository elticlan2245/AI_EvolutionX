from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://192.168.50.123",
        "http://192.168.50.123:3000",
        "http://iaevolutionxm.asuscomm.com",
        "http://iaevolutionxm.asuscomm.com:3000",
        "https://iaevolutionxm.asuscomm.com"
    ]
    
    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db: str = "aievolutionx"
    
    class Config:
        env_file = ".env"

settings = Settings()
