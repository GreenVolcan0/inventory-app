from sqlalchemy import Enum, text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base, str_uniq, int_pk
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    guest = "guest"
    admin = "admin"
    super_admin = "super_admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    login: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    password_hash: Mapped[str]
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), default=UserRole.guest, server_default="guest", nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
