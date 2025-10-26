# AI EvolutionX - Guía de Configuración

## Variables de Entorno Requeridas

### Base de Datos
- `MONGODB_URL`: URL de conexión a MongoDB
- `DATABASE_NAME`: Nombre de la base de datos

### Autenticación
- `JWT_SECRET`: Clave secreta para JWT (CAMBIAR EN PRODUCCIÓN)
- `JWT_ALGORITHM`: Algoritmo de encriptación (HS256)
- `JWT_EXPIRATION`: Tiempo de expiración en segundos

### APIs Externas
- `ANTHROPIC_API_KEY`: Clave de Claude API para afiliados
- `OPENAI_API_KEY`: Clave de OpenAI (opcional)

### Stripe (Pagos)
Para configurar pagos:
1. Crear cuenta en https://stripe.com
2. Ir a https://dashboard.stripe.com/apikeys
3. Copiar Secret Key y Publishable Key
4. Crear productos y precios en Stripe
5. Copiar Price IDs

### Sistema de Afiliados
- `AFFILIATE_COMMISSION_RATE`: Tasa de comisión (0.20 = 20%)
- `MINIMUM_PAYOUT`: Mínimo para solicitar pago ($50)

## Configuración de Producción

### Seguridad
1. Cambiar `JWT_SECRET` a valor único y seguro
2. Configurar CORS con orígenes específicos
3. Habilitar HTTPS
4. Configurar rate limiting apropiado

### Base de Datos
1. Usar MongoDB Atlas o cluster dedicado
2. Habilitar autenticación
3. Configurar backups automáticos

### Monitoring
1. Configurar logs centralizados
2. Habilitar alertas de errores
3. Monitorear uso de API y costos

## Flujo de Afiliados

1. Usuario A se registra como afiliado
2. Obtiene código único (ej: AEX1234)
3. Comparte link: https://iaevolutionxm.asuscomm.com/?ref=AEX1234
4. Usuario B se registra usando ese link
5. Usuario B suscribe a plan Pro ($10/mes)
6. Usuario A recibe $2/mes mientras B mantenga suscripción
7. Cuando Usuario A acumula $50, puede solicitar pago

## Precios y Planes

### Free
- 100 mensajes/mes
- Acceso básico
- 1 modelo

### Pro ($10/mes)
- 5000 mensajes/mes
- Todos los modelos
- Síntesis de voz
- Análisis de imágenes
- Soporte prioritario

### Enterprise ($50/mes)
- Mensajes ilimitados
- Todo de Pro +
- API access
- Modelos custom
- SLA garantizado

## Comisiones de Afiliados

- Pro: $10/mes × 20% = $2/mes por usuario
- Enterprise: $50/mes × 20% = $10/mes por usuario

## Costos de Claude API

Aproximados por conversación:
- Claude 3.5 Sonnet: ~$0.05
- Margen de ganancia: $10 - costos = ~$5-8/usuario
