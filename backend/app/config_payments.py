# Stripe Configuration
STRIPE_SECRET_KEY = "sk_test_51RV4CoRodI4NcmAqsIH0yii7TCPuRM2Q7UhCOwodcnAnUcXi9zKkIGsNAx6PENWFcZzpZmWgAbccommGilWUCrmk00YOhIlTQz"  # Reemplazar con tu clave real
STRIPE_PUBLISHABLE_KEY = "pk_test_51RV4CoRodI4NcmAqtfqzHYTOpqZdzdYyf6kMFpPZAFAidXNZTlsXkWsz1RrgL9yWqqta2GScDX0VHjhzYCaVKgUe00UoaoF3PX"  # Reemplazar con tu clave pública

# Plans Configuration
PLANS = {
    "free": {
        "name": "Free",
        "price": 0,
        "monthly_limit": 100,
        "voice_enabled": False,
        "features": [
            "100 mensajes/mes",
            "Modelos básicos",
            "Historial 7 días"
        ]
    },
    "premium": {
        "name": "Premium",
        "price": 9.99,  # USD
        "price_id": "price_premium_monthly",  # Stripe Price ID
        "monthly_limit": 1000,
        "voice_enabled": True,
        "features": [
            "1000 mensajes/mes",
            "Todos los modelos",
            "Voz en tiempo real",
            "Historial ilimitado",
            "Prioridad en respuestas"
        ]
    },
    "pro": {
        "name": "Pro",
        "price": 29.99,  # USD
        "price_id": "price_pro_monthly",  # Stripe Price ID
        "monthly_limit": -1,  # Unlimited
        "voice_enabled": True,
        "features": [
            "Mensajes ilimitados",
            "Todos los modelos premium",
            "Voz en tiempo real",
            "API access",
            "Entrenamiento personalizado",
            "Soporte prioritario 24/7",
            "Sin anuncios"
        ]
    }
}
