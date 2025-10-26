from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Configuración completa de AI EvolutionX Platform
    Configuración profesional para producción con sistema de afiliados y pagos
    """
    
    # ==========================================
    # CONFIGURACIÓN DE BASE DE DATOS
    # ==========================================
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "ai_evolutionx"
    
    # ==========================================
    # CONFIGURACIÓN DE AUTENTICACIÓN JWT
    # ==========================================
    jwt_secret: str = "aievolutionx_super_secret_key_change_in_production_2025"
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 86400  # 24 horas
    
    # ==========================================
    # CONFIGURACIÓN DE OLLAMA
    # ==========================================
    ollama_host: str = "http://localhost:11434"
    
    # ==========================================
    # API KEYS EXTERNAS
    # ==========================================
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    # ==========================================
    # STRIPE (SISTEMA DE PAGOS)
    # ==========================================
    stripe_secret_key: Optional[str] = None
    stripe_publishable_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None
    
    # ==========================================
    # CONFIGURACIÓN DE LA PLATAFORMA
    # ==========================================
    platform_name: str = "AI EvolutionX"
    platform_url: str = "https://iaevolutionxm.asuscomm.com"
    admin_email: str = "elgalatico2280@gmail.com"
    
    # ==========================================
    # LÍMITES DE PLANES
    # ==========================================
    free_plan_messages: int = 100
    pro_plan_messages: int = 5000
    enterprise_plan_messages: int = -1  # Ilimitado
    
    # ==========================================
    # SISTEMA DE AFILIADOS
    # ==========================================
    affiliate_commission_rate: float = 0.20  # 20% de comisión
    minimum_payout: float = 50.00  # Mínimo $50 para pagar
    
    # ==========================================
    # PRECIOS DE PLANES (en centavos)
    # ==========================================
    pro_plan_price: int = 1000  # $10.00
    enterprise_plan_price: int = 5000  # $50.00
    
    # ==========================================
    # IDS DE PRECIOS DE STRIPE
    # ==========================================
    stripe_pro_price_id: Optional[str] = None
    stripe_enterprise_price_id: Optional[str] = None
    
    # ==========================================
    # CONFIGURACIÓN DE EMAIL
    # ==========================================
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_from_email: Optional[str] = None
    
    # ==========================================
    # CONFIGURACIÓN DE ALMACENAMIENTO
    # ==========================================
    max_file_size_mb: int = 10
    allowed_file_types: str = "image/jpeg,image/png,image/gif,image/webp"
    
    # ==========================================
    # RATE LIMITING
    # ==========================================
    rate_limit_requests_per_minute: int = 60
    rate_limit_requests_per_hour: int = 1000
    
    # ==========================================
    # CONFIGURACIÓN DE LOGS
    # ==========================================
    log_level: str = "INFO"
    log_file_path: str = "../logs/backend_app.log"
    
    # ==========================================
    # CONFIGURACIÓN DE SEGURIDAD
    # ==========================================
    cors_origins: str = "*"
    allow_credentials: bool = True
    
    # ==========================================
    # FEATURES FLAGS
    # ==========================================
    enable_voice_synthesis: bool = True
    enable_image_analysis: bool = True
    enable_affiliates: bool = True
    enable_payments: bool = True
    enable_api_access: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = False
        extra = "ignore"  # Ignora variables extras que no estén definidas

settings = Settings()

# Validaciones post-inicialización
if settings.enable_payments and not settings.stripe_secret_key:
    print("⚠️  WARNING: Payments enabled but Stripe not configured")

if settings.enable_affiliates and settings.affiliate_commission_rate > 1.0:
    raise ValueError("Affiliate commission rate must be between 0 and 1")

if settings.minimum_payout < 10:
    raise ValueError("Minimum payout must be at least $10")
