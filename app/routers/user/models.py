from typing import Optional

from pydantic import BaseModel


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]
    full_name: Optional[str]
    scores: Optional[str]
    password: Optional[str]
