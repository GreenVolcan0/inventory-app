from pydantic import BaseModel, ConfigDict, model_validator
from app.models.items import ItemStatus
from datetime import datetime
from app.schemas.item import ItemStatus
from app.schemas.category import CategoryOut
from app.schemas.holder import HolderOut

class ItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    model: str
    holder: int
    serial_num: str
    inventory_num: str
    status: ItemStatus
    updated_at: datetime
    editor_id: int
    category: CategoryOut

class ItemCreateIn(BaseModel):
    model: str
    category_id: int
    holder_first_name: str | None = None
    holder_last_name: str | None = None
    holder_patronymic: str | None = None
    serial_num: str
    inventory_num: str
    status: ItemStatus = ItemStatus.in_stock

class ItemUpdatedIn(BaseModel):
    model: str | None = None
    category_id: int | None = None
    serial_num: str | None = None
    inventory_num: str | None = None
    status: ItemStatus | None = None
    holder_first_name: str | None = None
    holder_last_name: str | None = None
    holder_patronymic: str | None = None