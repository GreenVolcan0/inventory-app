from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.database import get_db
from app.services.auth import decode_token
from app.models.users import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

ROLE_LEVEL = {
    UserRole.guest: 0,
    UserRole.admin: 1,
    UserRole.super_admin: 2
}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="wrong creds",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = decode_token(token)
        if payload.get("type") != "access": raise credentials_error

        user_id = payload.get("sub")
        if user_id is None: raise credentials_error
    except JWTError: raise credentials_error

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None or not user.is_active: raise credentials_error

    return user

def require_role(min_role: UserRole):
    def checker(user: User = Depends(get_current_user)):
        if ROLE_LEVEL[user.role] < ROLE_LEVEL[min_role]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="no perms")
        return user
    return checker
