import stripe
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.config_payments import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, PLANS

# Configurar Stripe con tu clave secreta
stripe.api_key = STRIPE_SECRET_KEY

router = APIRouter(prefix="/api/payments", tags=["Payments"])

# =============================
# 🧾 Crear sesión de pago
# =============================
@router.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    data = await request.json()
    plan = data.get("plan")

    if plan not in PLANS:
        raise HTTPException(status_code=400, detail="Plan no válido")

    plan_info = PLANS[plan]
    if plan_info["price"] == 0:
        raise HTTPException(status_code=400, detail="El plan gratuito no requiere pago")

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            payment_method_types=["card"],
            line_items=[{"price": plan_info["price_id"], "quantity": 1}],
            success_url="https://iaevolutionxm.asuscomm.com/success",
            cancel_url="https://iaevolutionxm.asuscomm.com/cancel",
            allow_promotion_codes=True
        )
        return {"url": session.url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================
# 🔁 Webhook: Confirmar pago
# =============================
@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Firma inválida")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_details", {}).get("email", "Desconocido")
        print(f"✅ Pago completado por {customer_email}")

    elif event["type"] == "invoice.payment_failed":
        print("⚠️ Pago fallido o suscripción cancelada")

    return JSONResponse(content={"status": "success"})


# =============================
# 🧠 Endpoint opcional: Listar planes
# =============================
@router.get("/plans")
async def get_plans():
    return PLANS
