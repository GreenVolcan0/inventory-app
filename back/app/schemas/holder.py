from pydantic import BaseModel, ConfigDict

class HolderUpdateIn(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None

class HolderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    patronymic: str