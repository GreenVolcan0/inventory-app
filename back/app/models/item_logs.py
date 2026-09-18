from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base, int_pk
from datetime import datetime
import enum

class LogAction(str, enum.Enum):
    created = "created"
    updated = "updated"
    deleted = "deleted"

class ItemLog(Base):
    __tablename__ = "item_logs"

    id: Mapped[int_pk]
    item_id: Mapped[int | None] = mapped_column(ForeignKey("items.id", ondelete="SET NULL"), nullable=True)
    item_inventory_num: Mapped[str]
    action: Mapped[LogAction] = mapped_column(Enum(LogAction, name="log_action"), nullable=False)
    details: Mapped[str]
    editor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())