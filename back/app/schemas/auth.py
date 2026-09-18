from pydantic import BaseModel

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"