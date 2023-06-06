import logging

import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import config

engine = create_async_engine(config.DB_URL, pool_pre_ping=True)
LocalSession = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def active_session():
    """
    A dependency for working with PostgreSQL
    """
    try:
        db = LocalSession()
        yield db
    except Exception as e:
        logging.error(e)
    finally:
        await db.close()
