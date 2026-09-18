from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.item_logs import LogAction

class ItemLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_id: int | None
    item_inventory_num: str
    action: LogAction
    details: str
    editor_id: int
    created_at: datetime