from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import stripe
import os
from datetime import datetime
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(prefix="/api/billing", tags=["billing"])

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

class SubscriptionRequest(BaseModel):
    plan: str  # 'pro' or 'enterprise'
    payment_method_id: str

PLANS = {
    'free': {
        'price': 0,
        'messages_per_month': 100,
        'features': ['Basic chat', 'Limited history', '1 modelo']
    },
    'pro': {
        'price_id': 'price_xxxxx',  # Reemplazar con Stripe Price ID real
        'price': 1000,  # $10.00 en centavos
        'messages_per_month': 5000,
        'features': [
            'Unlimited chat',
            'Full history',
            'Voice synthesis',
            'Image analysis',
            'All models',
            'Priority support'
        ]
    },
    'enterprise': {
        'price_id': 'price_yyyyy',  # Reemplazar con Stripe Price ID real
        'price': 5000,  # $50.00
        'messages_per_month': -1,  # Unlimited
        'features': [
            'Everything in Pro',
            'Custom models',
            'API access',
            'Dedicated support',
            'Custom integrations',
            'SLA guarantee'
        ]
    }
}

@router.get("/plans")
async def get_plans():
    """Obtener planes disponibles"""
    return {"plans": PLANS}

@router.post("/subscribe")
async def create_subscription(
    request: SubscriptionRequest,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Crear suscripción con Stripe"""
    if not stripe.api_key:
        raise HTTPException(status_code=503, detail="Stripe not configured")
    
    try:
        user = await db.users.find_one({"email": current_user["sub"]})
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        plan = PLANS.get(request.plan)
        if not plan or request.plan == 'free':
            raise HTTPException(status_code=400, detail="Invalid plan")
        
        # Crear o recuperar customer de Stripe
        if not user.get('stripe_customer_id'):
            customer = stripe.Customer.create(
                email=user['email'],
                payment_method=request.payment_method_id,
                invoice_settings={'default_payment_method': request.payment_method_id}
            )
            
            await db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {"stripe_customer_id": customer.id}}
            )
            customer_id = customer.id
        else:
            customer_id = user['stripe_customer_id']
        
        # Crear suscripción
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': plan['price_id']}],
            expand=['latest_invoice.payment_intent']
        )
        
        # Actualizar usuario
        await db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "plan": request.plan,
                "stripe_subscription_id": subscription.id,
                "monthly_limit": plan['messages_per_month'],
                "monthly_messages": 0,
                "subscription_status": subscription.status,
                "subscription_start": datetime.utcnow()
            }}
        )
        
        # Si el usuario fue referido, actualizar comisiones del afiliado
        if user.get("referred_by"):
            affiliate = await db.affiliates.find_one({"code": user["referred_by"]})
            if affiliate:
                commission = plan['price'] / 100 * affiliate.get("commission_rate", 0.20)
                
                await db.affiliates.update_one(
                    {"_id": affiliate["_id"]},
                    {
                        "$inc": {
                            "pending_payout": commission,
                            "total_earnings": commission
                        }
                    }
                )
        
        return {
            "success": True,
            "subscription_id": subscription.id,
            "client_secret": subscription.latest_invoice.payment_intent.client_secret,
            "status": subscription.status
        }
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/cancel")
async def cancel_subscription(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Cancelar suscripción"""
    if not stripe.api_key:
        raise HTTPException(status_code=503, detail="Stripe not configured")
    
    user = await db.users.find_one({"email": current_user["sub"]})
    
    if not user.get('stripe_subscription_id'):
        raise HTTPException(status_code=400, detail="No active subscription")
    
    try:
        stripe.Subscription.delete(user['stripe_subscription_id'])
        
        await db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {
                "plan": "free",
                "stripe_subscription_id": None,
                "monthly_limit": 100,
                "subscription_status": "cancelled"
            }}
        )
        
        return {"success": True, "message": "Subscription cancelled"}
        
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/usage")
async def get_usage(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Obtener uso actual"""
    user = await db.users.find_one({"email": current_user["sub"]})
    
    plan_info = PLANS.get(user.get("plan", "free"), PLANS["free"])
    
    return {
        "plan": user.get("plan", "free"),
        "messages_used": user.get("monthly_messages", 0),
        "messages_limit": user.get("monthly_limit", 100),
        "percentage": (user.get("monthly_messages", 0) / user.get("monthly_limit", 100)) * 100 if user.get("monthly_limit", 100) > 0 else 0,
        "features": plan_info["features"],
        "subscription_status": user.get("subscription_status", "active")
    }

@router.post("/webhook")
async def stripe_webhook(request: dict, db = Depends(get_db)):
    """Webhook para eventos de Stripe"""
    # Implementar verificación de firma de Stripe
    event_type = request.get("type")
    
    if event_type == "invoice.payment_succeeded":
        # Renovación exitosa
        subscription_id = request["data"]["object"]["subscription"]
        user = await db.users.find_one({"stripe_subscription_id": subscription_id})
        
        if user:
            # Resetear contador mensual
            await db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {"monthly_messages": 0}}
            )
    
    elif event_type == "invoice.payment_failed":
        # Pago fallido
        subscription_id = request["data"]["object"]["subscription"]
        user = await db.users.find_one({"stripe_subscription_id": subscription_id})
        
        if user:
            await db.users.update_one(
                {"_id": user["_id"]},
                {"$set": {"subscription_status": "past_due"}}
            )
    
    return {"received": True}
