from typing import Optional

from pydantic import BaseModel

from app.core.utils import as_form


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    full_name: Optional[str]
    scores: Optional[str]
    password: Optional[str]


@as_form
class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    scores: str
    password: str
