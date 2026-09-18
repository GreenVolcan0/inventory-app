from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.users import User, UserRole
from app.services.auth import get_password_hash, check_password, create_access_token, create_refresh_token, decode_token
from app.schemas.auth import TokenOut

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == form.username).first()
    if not user or not check_password(form.password, user.password_hash):
        raise HTTPException(401, "wrong login or password")
    if not user.is_active:
        raise HTTPException(403, "account is deactivated")

    return TokenOut(
        access_token=create_access_token(user.id, user.role.value),
        refresh_token=create_refresh_token(user.id),
    )

@router.post("/refresh", response_model=TokenOut)
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh": raise HTTPException(401, "invalid token type")
    except Exception: raise HTTPException(401, "invalid refresh token")

    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user or not user.is_active:
        raise HTTPException(401, "user not found")

    return TokenOut(
        access_token=create_access_token(user.id, user.role.value),
        refresh_token=create_refresh_token(user.id)
    )