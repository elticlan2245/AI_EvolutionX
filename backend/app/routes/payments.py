from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Optional
import stripe
from ..auth import get_current_user
from ..database import get_db
from ..config_payments import STRIPE_SECRET_KEY, PLANS
from datetime import datetime
import os

router = APIRouter(prefix="/api/payments", tags=["payments"])

# Configurar Stripe
stripe.api_key = STRIPE_SECRET_KEY

@router.get("/plans")
async def get_plans():
    """Get available subscription plans"""
    return {"plans": PLANS}

@router.post("/create-checkout-session")
async def create_checkout_session(
    plan: str,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Create Stripe checkout session"""
    try:
        if plan not in PLANS or plan == "free":
            raise HTTPException(status_code=400, detail="Invalid plan")
        
        plan_config = PLANS[plan]
        
        # Obtener usuario
        user = await db.users.find_one({"email": current_user["sub"]})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Crear sesión de Stripe Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'{plan_config["name"]} Plan',
                        'description': '\n'.join(plan_config['features']),
                    },
                    'unit_amount': int(plan_config['price'] * 100),  # Stripe usa centavos
                    'recurring': {
                        'interval': 'month',
                    }
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url='http://iaevolutionxm.asuscomm.com/?success=true&plan=' + plan,
            cancel_url='http://iaevolutionxm.asuscomm.com/?canceled=true',
            client_reference_id=str(user["_id"]),
            customer_email=user["email"],
            metadata={
                'user_id': str(user["_id"]),
                'plan': plan
            }
        )
        
        return {"sessionId": session.id, "url": session.url}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request, db = Depends(get_db)):
    """Handle Stripe webhooks"""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET', 'whsec_...')
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Handle different event types
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Actualizar usuario con plan pagado
        user_id = session['metadata']['user_id']
        plan = session['metadata']['plan']
        plan_config = PLANS[plan]
        
        await db.users.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "plan": plan,
                    "monthly_limit": plan_config["monthly_limit"],
                    "voice_enabled": plan_config["voice_enabled"],
                    "subscription_id": session['subscription'],
                    "subscription_status": "active",
                    "subscription_start": datetime.utcnow()
                }
            }
        )
    
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        
        # Downgrade a free
        await db.users.update_one(
            {"subscription_id": subscription['id']},
            {
                "$set": {
                    "plan": "free",
                    "monthly_limit": 100,
                    "voice_enabled": False,
                    "subscription_status": "canceled"
                }
            }
        )
    
    return {"status": "success"}

@router.post("/cancel-subscription")
async def cancel_subscription(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Cancel user subscription"""
    try:
        user = await db.users.find_one({"email": current_user["sub"]})
        
        if not user.get("subscription_id"):
            raise HTTPException(status_code=400, detail="No active subscription")
        
        # Cancelar en Stripe
        subscription = stripe.Subscription.delete(user["subscription_id"])
        
        # Actualizar usuario
        await db.users.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "plan": "free",
                    "monthly_limit": 100,
                    "voice_enabled": False,
                    "subscription_status": "canceled",
                    "subscription_end": datetime.utcnow()
                }
            }
        )
        
        return {"message": "Subscription canceled successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/billing-portal")
async def create_billing_portal(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Create Stripe billing portal session"""
    try:
        user = await db.users.find_one({"email": current_user["sub"]})
        
        if not user.get("subscription_id"):
            raise HTTPException(status_code=400, detail="No active subscription")
        
        # Obtener customer de Stripe
        subscription = stripe.Subscription.retrieve(user["subscription_id"])
        
        # Crear portal session
        session = stripe.billing_portal.Session.create(
            customer=subscription.customer,
            return_url='http://iaevolutionxm.asuscomm.com/settings'
        )
        
        return {"url": session.url}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
