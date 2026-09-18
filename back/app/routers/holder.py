from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.holders import Holder
from app.models.users import UserRole
from app.schemas.holder import HolderOut, HolderUpdateIn

router = APIRouter(prefix="/holders", tags=["holders"])


@router.get("", response_model=list[HolderOut])
def list_holders(
    search: str | None = Query(None, description="Поиск по ФИО, для автокомплита"), db: Session = Depends(get_db),
    _=Depends(require_role(UserRole.guest)),
):
    query = db.query(Holder)
    if search:
        like = f"%{search}%"
        query = query.filter(
            (Holder.first_name.ilike(like))
            | (Holder.last_name.ilike(like))
            | (Holder.patronymic.ilike(like))
        )
    return query.order_by(Holder.last_name, Holder.first_name).all()


@router.patch("/{holder_id}", response_model=HolderOut)
def update_holder(
    holder_id: int,
    data: HolderUpdateIn,
    db: Session = Depends(get_db),
    _=Depends(require_role(UserRole.admin)),
):
    holder = db.query(Holder).filter(Holder.id == holder_id).first()
    if not holder:
        raise HTTPException(404, "Holder not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(holder, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Holder with this full name already exists")

    db.refresh(holder)
    return holder


@router.delete("/{holder_id}", status_code=204)
def delete_holder(
    holder_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_role(UserRole.admin)),
):
    holder = db.query(Holder).filter(Holder.id == holder_id).first()
    if not holder:
        raise HTTPException(404, "Holder not found")

    try:
        db.delete(holder)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Cannot delete: holder has items assigned")