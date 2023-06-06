from pydantic import BaseModel

from app.core.utils import as_form


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserRead(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    scores: str

    hashed_password: str

    class Config:
        orm_mode = True


@as_form
class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    scores: str
    password: str
