from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class Faculty(Base):
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    average_mark: Mapped[float] = mapped_column(nullable=False)
