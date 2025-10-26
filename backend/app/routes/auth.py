from fastapi import APIRouter, HTTPException, Depends, status
from ..models.user import UserRegister, UserLogin, Token, User, UserPlan
from ..auth import get_password_hash, verify_password, create_access_token, get_current_user
from ..database import get_db
from datetime import datetime

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=Token)
async def register(user_data: UserRegister, db = Depends(get_db)):
    """Register new user"""
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = {
        "email": user_data.email,
        "username": user_data.username,
        "hashed_password": get_password_hash(user_data.password),
        "plan": "free",
        "created_at": datetime.utcnow(),
        "is_active": True,
        "is_verified": False,
        "monthly_messages": 0,
        "monthly_limit": 100,
        "voice_enabled": False
    }
    
    result = await db.users.insert_one(user)
    user["_id"] = str(result.inserted_id)
    
    access_token = create_access_token(data={"sub": user["email"], "user_id": str(result.inserted_id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(result.inserted_id),
            "email": user["email"],
            "username": user["username"],
            "plan": user["plan"]
        }
    }

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db = Depends(get_db)):
    """Login user"""
    user = await db.users.find_one({"email": user_data.email})
    
    if not user or not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    await db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    
    access_token = create_access_token(data={"sub": user["email"], "user_id": str(user["_id"])})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "username": user["username"],
            "plan": user.get("plan", "free"),
            "monthly_messages": user.get("monthly_messages", 0),
            "monthly_limit": user.get("monthly_limit", 100),
            "voice_enabled": user.get("voice_enabled", False)
        }
    }

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user), db = Depends(get_db)):
    """Get current user info"""
    user = await db.users.find_one({"email": current_user["sub"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "username": user["username"],
        "plan": user.get("plan", "free"),
        "monthly_messages": user.get("monthly_messages", 0),
        "monthly_limit": user.get("monthly_limit", 100),
        "voice_enabled": user.get("voice_enabled", False),
        "created_at": user["created_at"]
    }
