from sqlalchemy import insert, select, update
from app.database import async_session_maker, async_session_maker_nullpool


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            inserted_id = result.scalar()
            return inserted_id

    @classmethod
    async def set_blocked(cls, model_id):
        async with async_session_maker_nullpool() as session:
            query = update(cls.model).where(cls.model.id == model_id).values(
                is_blocked=True,
                is_checked=True
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def set_checked(cls, model_id):
        async with async_session_maker_nullpool() as session:
            query = update(cls.model).where(cls.model.id == model_id).values(is_checked=True)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_one_or_none_for_tasks(cls, **filter_by):
        async with async_session_maker_nullpool() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
