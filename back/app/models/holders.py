from sqlalchemy import Enum, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base, int_pk, int_uniq, str_uniq

class Holder(Base):
    __tablename__ = "holders"

    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped[str]

    #__table_args__ = (UniqueConstraint("first_name", "last_name", "patronymic", name="uniq_holder"))
    