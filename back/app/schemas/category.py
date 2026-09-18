from pydantic import BaseModel, ConfigDict

class CategoryCreateIn(BaseModel):
    num: str
    name: str

class CategoryUpdateIn(BaseModel):
    num: str | None = None
    name: str | None = None

class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    num: str
    name: str