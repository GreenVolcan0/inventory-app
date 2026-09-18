from pydantic import BaseModel, ConfigDict

class CategoryCreateIn(BaseModel):
    num: int
    name: str

class CategoryUpdateIn(BaseModel):
    num: int | None = None
    name: str | None = None

class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    num: int
    name: str