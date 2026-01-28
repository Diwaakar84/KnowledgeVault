from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from app.db.session import get_db
from app.models.user import User, RefreshToken
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token, create_refresh_token

# Router for these APIs prefixing all endpoints with /auth
router = APIRouter(prefix="/auth", tags=["auth"])

# API request format
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int

# Endpoint to register new user
@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"id": str(user.id), "email": user.email}

# Create a session for an existing user
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    expires_at = datetime.utcnow() + timedelta(days=7)
    rt = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=expires_at
    )

    db.add(rt)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 900
    }

# Refresh the user session once the access token expired and refresh token is yet to expire
@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    token_row = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not token_row or token_row.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token(str(token_row.user_id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 900
    }

# Terminate the current session
@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    db.query(RefreshToken).filter(RefreshToken.token == refresh_token).delete()
    db.commit()
    return {"status": "logged out"}
