from sqlalchemy import Enum, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base, int_pk, str_uniq
from datetime import datetime
import enum

class ItemStatus(str, enum.Enum):
    issued = "issued"
    written_off = "written_off"
    in_stock = "in_stock"

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int_pk]
    model: Mapped[str]
    holder_id: Mapped[int | None] = mapped_column(ForeignKey("holders.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    serial_num: Mapped[str_uniq]
    inventory_num: Mapped[str_uniq]
    status: Mapped[ItemStatus] = mapped_column(Enum(ItemStatus, name="in_stock"), default=ItemStatus.in_stock, server_default="in_stock", nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())
    editor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    category: Mapped["Category"] = relationship()
    holder: Mapped["Holder | None"] = relationship()
    editor: Mapped["User"] = relationship()