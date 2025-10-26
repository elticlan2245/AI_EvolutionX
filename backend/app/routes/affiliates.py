from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from datetime import datetime
import secrets
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(prefix="/api/affiliates", tags=["affiliates"])

class AffiliateSignup(BaseModel):
    name: str
    payout_email: EmailStr
    
class PayoutRequest(BaseModel):
    amount: float

@router.post("/signup")
async def signup_affiliate(
    request: AffiliateSignup,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Registrarse como afiliado"""
    user = await db.users.find_one({"email": current_user["sub"]})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verificar si ya es afiliado
    existing = await db.affiliates.find_one({"user_id": str(user["_id"])})
    if existing:
        return {
            "success": True,
            "affiliate_code": existing["code"],
            "referral_url": f"https://iaevolutionxm.asuscomm.com/?ref={existing['code']}"
        }
    
    # Generar código único
    affiliate_code = f"AEX{secrets.token_hex(4).upper()}"
    
    affiliate_data = {
        "user_id": str(user["_id"]),
        "name": request.name,
        "code": affiliate_code,
        "payout_email": request.payout_email,
        "commission_rate": 0.20,  # 20% comisión
        "total_referrals": 0,
        "active_referrals": 0,
        "total_earnings": 0.0,
        "pending_payout": 0.0,
        "paid_out": 0.0,
        "created_at": datetime.utcnow(),
        "status": "active"
    }
    
    result = await db.affiliates.insert_one(affiliate_data)
    
    return {
        "success": True,
        "affiliate_code": affiliate_code,
        "referral_url": f"https://iaevolutionxm.asuscomm.com/?ref={affiliate_code}"
    }

@router.get("/stats")
async def get_affiliate_stats(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Obtener estadísticas de afiliado"""
    user = await db.users.find_one({"email": current_user["sub"]})
    affiliate = await db.affiliates.find_one({"user_id": str(user["_id"])})
    
    if not affiliate:
        raise HTTPException(status_code=404, detail="Not an affiliate")
    
    # Contar referidos
    total_referrals = await db.users.count_documents({"referred_by": affiliate["code"]})
    
    # Contar referidos activos (con plan de pago)
    active_referrals = await db.users.count_documents({
        "referred_by": affiliate["code"],
        "plan": {"$in": ["pro", "enterprise"]}
    })
    
    # Calcular earnings mensuales
    referred_users = await db.users.find({"referred_by": affiliate["code"]}).to_list(1000)
    
    monthly_earnings = 0.0
    for ref_user in referred_users:
        if ref_user.get("plan") == "pro":
            monthly_earnings += 10.0 * 0.20  # $2 por usuario pro
        elif ref_user.get("plan") == "enterprise":
            monthly_earnings += 50.0 * 0.20  # $10 por usuario enterprise
    
    # Actualizar en base de datos
    await db.affiliates.update_one(
        {"_id": affiliate["_id"]},
        {"$set": {
            "total_referrals": total_referrals,
            "active_referrals": active_referrals,
            "monthly_earnings": monthly_earnings
        }}
    )
    
    return {
        "code": affiliate["code"],
        "referral_url": f"https://iaevolutionxm.asuscomm.com/?ref={affiliate['code']}",
        "total_referrals": total_referrals,
        "active_paying": active_referrals,
        "monthly_earnings": monthly_earnings,
        "lifetime_earnings": affiliate.get("total_earnings", 0.0),
        "pending_payout": affiliate.get("pending_payout", 0.0),
        "commission_rate": affiliate.get("commission_rate", 0.20)
    }

@router.post("/payout")
async def request_payout(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Solicitar pago de comisiones"""
    user = await db.users.find_one({"email": current_user["sub"]})
    affiliate = await db.affiliates.find_one({"user_id": str(user["_id"])})
    
    if not affiliate:
        raise HTTPException(status_code=404, detail="Not an affiliate")
    
    pending = affiliate.get("pending_payout", 0.0)
    
    if pending < 50.0:
        raise HTTPException(
            status_code=400, 
            detail=f"Minimum payout is $50. You have ${pending:.2f}"
        )
    
    # Crear solicitud de pago
    payout_request = {
        "affiliate_id": str(affiliate["_id"]),
        "affiliate_code": affiliate["code"],
        "amount": pending,
        "payout_email": affiliate["payout_email"],
        "status": "pending",
        "requested_at": datetime.utcnow(),
        "processed_at": None,
        "transaction_id": None
    }
    
    await db.payouts.insert_one(payout_request)
    
    # Resetear pending_payout
    await db.affiliates.update_one(
        {"_id": affiliate["_id"]},
        {"$set": {"pending_payout": 0.0}}
    )
    
    return {
        "success": True,
        "message": "Payout requested successfully. It will be processed within 5-7 business days.",
        "amount": pending
    }

@router.get("/dashboard")
async def get_affiliate_dashboard(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Dashboard completo para afiliados"""
    user = await db.users.find_one({"email": current_user["sub"]})
    affiliate = await db.affiliates.find_one({"user_id": str(user["_id"])})
    
    if not affiliate:
        raise HTTPException(status_code=404, detail="Not an affiliate")
    
    # Obtener referidos recientes
    recent_referrals = await db.users.find(
        {"referred_by": affiliate["code"]},
        {"email": 1, "plan": 1, "created_at": 1}
    ).sort("created_at", -1).limit(10).to_list(10)
    
    # Historial de pagos
    payout_history = await db.payouts.find(
        {"affiliate_id": str(affiliate["_id"])}
    ).sort("requested_at", -1).limit(10).to_list(10)
    
    return {
        "affiliate": {
            "code": affiliate["code"],
            "referral_url": f"https://iaevolutionxm.asuscomm.com/?ref={affiliate['code']}",
            "commission_rate": affiliate.get("commission_rate", 0.20),
            "status": affiliate.get("status", "active")
        },
        "stats": {
            "total_referrals": affiliate.get("total_referrals", 0),
            "active_referrals": affiliate.get("active_referrals", 0),
            "monthly_earnings": affiliate.get("monthly_earnings", 0.0),
            "lifetime_earnings": affiliate.get("total_earnings", 0.0),
            "pending_payout": affiliate.get("pending_payout", 0.0)
        },
        "recent_referrals": recent_referrals,
        "payout_history": payout_history
    }
