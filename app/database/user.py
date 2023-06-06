from typing import List

from sqlalchemy.orm import mapped_column, Mapped

from app.database.base import Base


class User(Base):
    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    full_name: Mapped[str] = mapped_column()
    scores: Mapped[str] = mapped_column()

    hashed_password: Mapped[str] = mapped_column()

    admin: Mapped[bool] = mapped_column(default=False)
