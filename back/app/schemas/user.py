from pydantic import BaseModel, ConfigDict
from app.models.users import UserRole

class UserCreateIn(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str
    role: UserRole = UserRole.guest

class UserUpdateRoleIn(BaseModel):
    role: UserRole

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    first_name: str
    last_name: str
    role: UserRole
    is_active: bool

class UpdatePasswordIn(BaseModel):
    new_password: str

class UserMe(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    login: str
    first_name: str
    last_name: str
    role: UserRole