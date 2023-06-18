from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User


async def get_user(username: str, session: AsyncSession) -> User | None:
    return await session.scalar(select(User).where(User.username == username).limit(1))
