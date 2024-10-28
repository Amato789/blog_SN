from app.dao.base import BaseDAO
from app.posts.models import Posts, Comments  # noqa
from app.users.models import Users  # noqa
from app.database import async_session_maker, async_session_maker_nullpool
from sqlalchemy import and_, delete, func, insert, select, case, update
from datetime import date
from sqlalchemy.orm import selectinload
from typing import Dict, Set
from app.posts.schemas import CommentSchema


class PostDAO(BaseDAO):
    model = Posts

    @classmethod
    async def remove(cls, post_id: int, user_id: int):
        async with async_session_maker() as session:
            remove_post = delete(Posts).where(
                and_(
                    Posts.id == post_id,
                    Posts.user_id == user_id,
                )
            )
            await session.execute(remove_post)
            await session.commit()

    @classmethod
    async def get_analytics(cls, date_from: date, date_to: date):
        async with async_session_maker() as session:
            query = select(
                Posts.created_at.label('date'),
                func.count().label('total_posts'),
                func.sum(case((Posts.is_blocked == True, 1), else_=0)).label('blocked_posts')
            ).where(
                Posts.created_at >= date_from,
                Posts.created_at <= date_to
            ).group_by(
                func.date(Posts.created_at)
            )

            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def update(cls, post_id: int, user_id: int, **kwargs) -> None:
        async with async_session_maker() as session:
            query = (
                update(Posts)
                .where(Posts.id == post_id, Posts.user_id == user_id)
                .values(**kwargs)
            )
            await session.execute(query)
            await session.commit()


class CommentDAO(BaseDAO):
    model = Comments

    @classmethod
    async def remove(cls, comment_id: int, user_id: int, post_id: int):
        async with async_session_maker() as session:
            remove_comment = delete(Comments).where(
                and_(
                    Comments.id == comment_id,
                    Comments.user_id == user_id,
                    Comments.post_id == post_id
                )
            )
            await session.execute(remove_comment)
            await session.commit()

    @classmethod
    async def add_answer(cls, **data):
        async with async_session_maker_nullpool() as session:
            query = insert(Comments).values(**data).returning(Comments.id)
            result = await session.execute(query)
            await session.commit()
            inserted_id = result.scalar()
            return inserted_id

    @classmethod
    async def update(cls, comment_id: int, user_id: int, **kwargs) -> None:
        async with async_session_maker() as session:
            query = (
                update(Comments)
                .where(Comments.id == comment_id, Comments.user_id == user_id)
                .values(**kwargs)
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_comments_with_replies(cls, post_id: int):
        async with async_session_maker() as session:
            query = select(Comments).where(Comments.post_id == post_id).options(
                selectinload(Comments.children)).order_by(Comments.created_at)
            comments = await session.execute(query)
            comments = comments.scalars().all()

            if not comments:
                return []

            # Create a dictionary to build a comment tree
            comments_by_id: Dict[int, CommentSchema] = {}
            for comment in comments:
                comment_schema = CommentSchema.model_validate(comment)
                comments_by_id[comment_schema.id] = comment_schema

            # Set to track comments that have already been added as children
            children_ids: Set[int] = set()

            # Building a tree and adding child comment IDs to `children_ids`
            for comment in comments_by_id.values():
                if comment.parent_id:
                    parent_comment = comments_by_id.get(comment.parent_id)
                    if parent_comment:
                        if parent_comment.children is None:
                            parent_comment.children = []
                        children_ids.add(comment.id)

            root_comments = [
                comment for comment in comments_by_id.values() if comment.id not in children_ids
            ]

            return root_comments

    @classmethod
    async def get_analytics(cls, date_from: date, date_to: date):
        async with async_session_maker() as session:
            query = select(
                Comments.created_at.label('date'),
                func.count().label('total_comments'),
                func.sum(case((Comments.is_blocked == True, 1), else_=0)).label('blocked_comments')
            ).where(
                Comments.created_at >= date_from,
                Comments.created_at <= date_to
            ).group_by(
                func.date(Comments.created_at)
            )

            result = await session.execute(query)
            return result.mappings().all()
