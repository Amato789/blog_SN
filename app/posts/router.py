from fastapi import APIRouter, Depends
from typing import Optional
from app.exceptions import CommentNotFoundException, PostNotFoundException
from app.posts.dao import PostDAO, CommentDAO
from app.posts.schemas import PostSchema, NewPostSchema, CommentSchema, NewCommentSchema, CurrentCommentSchema
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.tasks.tasks import post_to_moderate
from app.tasks.tasks import comment_to_moderate, make_answer_from_ai

router = APIRouter(
    prefix="/posts",
    tags=["Posts & Comments"],
)


@router.get("")
async def get_posts() -> list[PostSchema]:
    posts = await PostDAO.find_all()
    if not posts:
        raise PostNotFoundException
    return posts


@router.get("/{post_id}")
async def get_post(post_id: int) -> PostSchema:
    post = await PostDAO.find_one_or_none(id=post_id)
    if not post:
        raise PostNotFoundException
    return post


@router.post("")
async def add_post(
        post: NewPostSchema,
        user: Users = Depends(get_current_user),
) -> None:
    added_post = await PostDAO.add(
        user_id=user.id,
        title=post.title,
        text=post.text,
        created_at=post.created_at,
        autoresponder_enabled=post.autoresponder_enabled,
        autoresponder_delay=post.autoresponder_delay,
        is_blocked=False,
        is_checked=False
    )
    post_to_moderate.delay(
        model_id=added_post,
        string_to_check=f"Post title: {post.title}\nPost text: {post.text}"
    )


@router.delete("/{post_id}")
async def remove_post(
        post_id: int,
        user: Users = Depends(get_current_user)
) -> None:
    if await PostDAO.find_one_or_none(user_id=user.id, id=post_id):
        await PostDAO.remove(user_id=user.id, post_id=post_id)


@router.get("/{post_id}/comments")
async def get_comments(post_id: int) -> list[CommentSchema]:
    comments = await CommentDAO.find_comments_with_replies(post_id)
    if not comments:
        raise CommentNotFoundException
    return comments


@router.get("/{post_id}/comments/{comment_id}")
async def get_comment(post_id: int, comment_id: int) -> CurrentCommentSchema:
    comment = await CommentDAO.find_one_or_none(id=comment_id, post_id=post_id)
    if not comment:
        raise CommentNotFoundException
    return comment


@router.post("/{post_id}/comments/")
async def add_comment(
        post_id: int,
        comment: NewCommentSchema,
        user: Users = Depends(get_current_user),
        parent_id: Optional[int] = None
) -> None:
    added_comment = await CommentDAO.add(
        user_id=user.id,
        post_id=post_id,
        text=comment.text,
        created_at=comment.created_at,
        is_blocked=False,
        is_checked=False,
        parent_id=parent_id
    )
    comment_to_moderate.delay(model_id=added_comment, string_to_check=comment.text)
    post = await PostDAO.find_one_or_none(id=post_id)
    if post and post.autoresponder_enabled:
        make_answer_from_ai.apply_async(
            args=[post_id, added_comment, comment.text],
            countdown=post.autoresponder_delay
        )


@router.delete("/{post_id}/comments/{comment_id}")
async def remove_comment(
        post_id: int,
        comment_id: int,
        user: Users = Depends(get_current_user)
) -> None:
    if await CommentDAO.find_one_or_none(user_id=user.id, id=comment_id, post_id=post_id):
        await CommentDAO.remove(user_id=user.id, comment_id=comment_id, post_id=post_id)
