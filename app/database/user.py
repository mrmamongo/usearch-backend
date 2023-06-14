from dataclasses import dataclass

from adaptix import Retort
from sqlalchemy.orm import mapped_column, Mapped

from app.database.adapter import ModelJSON
from app.database.base import Base

RETORT = Retort()


@dataclass
class UserScores:
    rus: int
    lit: int
    in_lang: int
    math_algebra: int
    math_geometry: int
    ikt: int
    history: int
    sociology: int
    geography: int
    physics: int
    chemistry: int
    biology: int
    art: int
    technology: int
    obj: int
    PE: int


class User(Base):
    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    full_name: Mapped[str] = mapped_column()
    scores: Mapped[UserScores] = mapped_column(ModelJSON(UserScores, RETORT))

    hashed_password: Mapped[str] = mapped_column()

    admin: Mapped[bool] = mapped_column(default=False)
