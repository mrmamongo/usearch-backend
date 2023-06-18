from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import mapped_column, Mapped

from app.database.models.base import Base


class Colleague(Base):
    long_name: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    tags: Mapped[list[str]] = mapped_column(ARRAY(String))
