from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_role, get_current_user
from app.models.users import User, UserRole
from app.schemas.user import UserCreateIn, UserUpdateRoleIn, UserOut
from app.services.auth import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _ = Depends(require_role(UserRole.super_admin))):
    return db.query(User).all()

@router.post("", response_model=UserOut, status_code=201)
def create_user(data: UserCreateIn, db: Session = Depends(get_db), _ = Depends(require_role(UserRole.super_admin))):
    if db.query(User).filter(User.login == data.login).first():
        raise HTTPException(400, "user already exists")

    user = User(
        login=data.login,
        password_hash=get_password_hash(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        role=data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.patch("/{user_id}/deactivate", response_model=UserOut)
def deactivate_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.super_admin))):
    if user_id == current_user.id: raise HTTPException(400, "бляяя себя захуярил")
    user = db.query(User).filter(User.id == user_id).first()
    if not user: raise HTTPException(404, "oh shit, i fucked myself")
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user

@router.patch("/{user_id}/role", response_model=UserOut)
def update_role(user_id: int, data: UserUpdateRoleIn, db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.super_admin))):
    if user_id == current_user.id: raise HTTPException(400, "didn't merit it")
    user = db.query(User).filter(User.id == user_id).first()
    if not user: raise HTTPException(404, "user not found")
    user.role = data.role
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=402)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.super_admin))
):
    user = db.query(User).filter(User.id == user_id)
    if user_id == current_user.id: raise HTTPException(400, "бляя, себя захуярил")
    if not user: raise HTTPException(404, "User not found")

    db.delete(user)
    db.commit()