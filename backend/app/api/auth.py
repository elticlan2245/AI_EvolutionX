from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt

from ..database import get_db
from ..config.settings import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRegister(BaseModel):
    username: str = None
    email: EmailStr
    password: str
    name: str = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=settings.jwt_expiration)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)

@router.post("/register")
async def register(user: UserRegister, db = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user exists
        existing = await db.users.find_one({"email": user.email})
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password
        hashed_password = pwd_context.hash(user.password)
        
        # Create user
        user_data = {
            "email": user.email,
            "password": hashed_password,
            "name": user.name or user.email.split("@")[0],
            "username": user.username or user.email.split("@")[0],
            "created_at": datetime.utcnow(),
            "plan": "free",
            "monthly_messages": 0,
            "monthly_limit": 100,
            "role": "user"
        }
        
        result = await db.users.insert_one(user_data)
        
        # Create token
        token = create_access_token({"sub": user.email})
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "email": user.email,
                "name": user_data["name"],
                "plan": "free"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login(user: UserLogin, db = Depends(get_db)):
    """Login user"""
    try:
        # Find user
        db_user = await db.users.find_one({"email": user.email})
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify password
        if not pwd_context.verify(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Incorrect password")
        
        # Create token
        token = create_access_token({"sub": user.email})
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "email": db_user["email"],
                "name": db_user.get("name", "User"),
                "plan": db_user.get("plan", "free")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
async def get_current_user(db = Depends(get_db)):
    """Get current user info"""
    # TODO: Implement JWT verification
    return {"message": "Not implemented yet"}
