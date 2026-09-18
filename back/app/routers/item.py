from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.items import Item, ItemStatus
from app.models.holders import Holder
from app.models.item_logs import ItemLog, LogAction
from app.models.users import User, UserRole
from app.schemas.item import ItemOut, ItemCreateIn, ItemUpdatedIn
from app.schemas.item_log import ItemLogOut

router = APIRouter(prefix="/items", tags=["items"])


def _get_or_create_holder(db: Session, first_name: str, last_name: str, patronymic: str | None) -> Holder:
    patronymic = patronymic or ""
    holder = (
        db.query(Holder)
        .filter_by(first_name=first_name, last_name=last_name, patronymic=patronymic)
        .first()
    )
    if holder:
        return holder
    holder = Holder(first_name=first_name, last_name=last_name, patronymic=patronymic)
    db.add(holder)
    db.flush()
    return holder


@router.get("", response_model=list[ItemOut])
def list_items(
    category_id: int | None = None,
    holder_id: int | None = None,
    status: ItemStatus | None = None,
    search: str | None = Query(None, description="Поиск по серийному или инв. номеру"),
    limit: int = Query(100, le=500),
    offset: int = 0,
    db: Session = Depends(get_db),
    _=Depends(require_role(UserRole.guest)),
):
    query = db.query(Item)
    if category_id is not None:
        query = query.filter(Item.category_id == category_id)
    if holder_id is not None:
        query = query.filter(Item.holder_id == holder_id)
    if status is not None:
        query = query.filter(Item.status == status)
    if search:
        like = f"%{search}%"
        query = query.filter((Item.serial_num.ilike(like)) | (Item.inventory_num.ilike(like)))

    return query.order_by(Item.id).offset(offset).limit(limit).all()


@router.get("/{item_id}", response_model=ItemOut)
def get_item(item_id: int, db: Session = Depends(get_db), _=Depends(require_role(UserRole.guest))):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(404, "Item not found")
    return item


@router.post("", response_model=ItemOut, status_code=201)
def create_item(
    data: ItemCreateIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin)),
):
    if db.query(Item).filter(Item.serial_num == data.serial_num).first():
        raise HTTPException(400, "serial_num already exists")
    if db.query(Item).filter(Item.inventory_num == data.inventory_num).first():
        raise HTTPException(400, "inventory_num already exists")

    holder = None
    if data.holder_first_name and data.holder_last_name:
        holder = _get_or_create_holder(db, data.holder_first_name, data.holder_last_name, data.holder_patronymic)

    item = Item(
        model=data.model,
        category_id=data.category_id,
        holder_id=holder.id if holder else None,
        serial_num=data.serial_num,
        inventory_num=data.inventory_num,
        status=data.status,
        editor_id=current_user.id,
    )
    db.add(item)

    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Invalid category_id or data conflict")

    db.add(ItemLog(
        item_id=item.id,
        item_inventory_num=item.inventory_num,
        action=LogAction.created,
        details=f"Создана позиция «{item.model}» (инв. №{item.inventory_num})",
        editor_id=current_user.id,
    ))
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{item_id}", response_model=ItemOut)
def update_item(
    item_id: int,
    data: ItemUpdatedIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin)),
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(404, "Item not found")

    payload = data.model_dump(exclude_unset=True)
    changes = []

    holder_fields = {"holder_first_name", "holder_last_name", "holder_patronymic"}
    if holder_fields & payload.keys():
        fn = payload.pop("holder_first_name", None)
        ln = payload.pop("holder_last_name", None)
        pt = payload.pop("holder_patronymic", None)
        if fn and ln:
            holder = _get_or_create_holder(db, fn, ln, pt)
            if holder.id != item.holder_id:
                changes.append(f"держатель: {item.holder_id} -> {holder.id}")
                item.holder_id = holder.id

    for field, new_val in payload.items():
        old_val = getattr(item, field)
        if old_val != new_val:
            changes.append(f"{field}: {old_val!r} -> {new_val!r}")
            setattr(item, field, new_val)

    item.editor_id = current_user.id

    if changes:
        db.add(ItemLog(
            item_id=item.id,
            item_inventory_num=item.inventory_num,
            action=LogAction.updated,
            details="; ".join(changes),
            editor_id=current_user.id,
        ))

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Data conflict (duplicate serial/inventory number)")

    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.admin))
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(404, "Item not found")

    db.add(ItemLog(
        item_id=item.id,
        item_inventory_num=item.inventory_num,
        action=LogAction.deleted,
        details=f"Удалена позиция «{item.model}» (инв. №{item.inventory_num})",
        editor_id=current_user.id,
    ))
    db.delete(item)
    db.commit()


@router.get("/{item_id}/logs", response_model=list[ItemLogOut])
def get_item_logs(item_id: int, db: Session = Depends(get_db), _=Depends(require_role(UserRole.guest))):
    return (
        db.query(ItemLog)
        .filter(ItemLog.item_id == item_id)
        .order_by(ItemLog.created_at.desc())
        .all()
    )