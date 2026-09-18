from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.core.dependencies import require_role
from app.models.categories import Category
from app.models.users import UserRole
from app.schemas.category import CategoryOut, CategoryCreateIn, CategoryUpdateIn


router = APIRouter(prefix="/caregories", tags=["categories"])

@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db), _ = Depends(require_role(UserRole.guest))):
    return db.query(Category).order_by(Category.num).all()

@router.post("", response_model=CategoryOut, status_code=201)
def create_category(data: CategoryCreateIn, db: Session = Depends(get_db), _=Depends(require_role(UserRole.admin))):
    if db.query(Category).filter(Category.num == data.num).first():
        raise HTTPException(400, "Category with this num already exists")
    category = Category(num=data.num, name=data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.patch("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, data: CategoryUpdateIn, db: Session = Depends(get_db), _=Depends(require_role(UserRole.admin))):
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category: raise HTTPException(404, "Category not found")
    for field, val in data.model_dump(exclude_unset=True).items():
        setattr(category, field, val)

    try: db.commit()
    except IntegrityError: db.rollback(); raise HTTPException(400, "Category already exists")

    db.refresh(category)
    return category

@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db), _=Depends(require_role(UserRole.admin))):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category: raise HTTPException(404, "Category not found")

    try:
        db.delete(category)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Cannot delete category")

    