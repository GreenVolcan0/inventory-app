from sqlalchemy.orm import Mapped
from app.core.database import Base, int_pk, int_uniq, str_uniq
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int_pk]
    num: Mapped[str_uniq]
    name: Mapped[str_uniq]