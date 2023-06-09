from pydantic import BaseModel


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

    password: str

    class Config:
        orm_mode = True


