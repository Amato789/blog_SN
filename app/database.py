from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

if settings.MODE == "TEST":
    DATABASE_URL = settings.get_test_database_url
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = settings.get_database_url
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

DATABASE_PARAMS_nullpool = {"poolclass": NullPool}
engine_nullpool = create_async_engine(DATABASE_URL, **DATABASE_PARAMS_nullpool)

async_session_maker_nullpool = sessionmaker(engine_nullpool, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
