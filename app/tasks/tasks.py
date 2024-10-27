import asyncio
from datetime import datetime
from app.tasks.celery_setup import celery
from app.posts.dao import PostDAO, CommentDAO
from app.utils import moderate_string_by_openai, create_answer_by_openai
from app.exceptions import ModerateByOpenAIError


@celery.task
def post_to_moderate(model_id, string_to_check):
    result = moderate_string_by_openai(string_to_check=string_to_check)
    if result is None:
        raise ModerateByOpenAIError
    elif result:
        asyncio.run(PostDAO.set_blocked(model_id))
    else:
        asyncio.run(PostDAO.set_checked(model_id))


@celery.task
def comment_to_moderate(model_id, string_to_check):
    result = moderate_string_by_openai(string_to_check=string_to_check)
    if result is None:
        raise ModerateByOpenAIError
    elif result:
        asyncio.run(CommentDAO.set_blocked(model_id))
    else:
        asyncio.run(CommentDAO.set_checked(model_id))


@celery.task
def make_answer_from_ai(post_id, parent_id, comment_text):
    post = asyncio.run(PostDAO.find_one_or_none_for_tasks(id=post_id, autoresponder_enabled=True))
    if post:
        result = create_answer_by_openai(post=post.text, comment=comment_text)
        if result is not None:
            added_comment = asyncio.run(CommentDAO.add_answer(
                user_id=1,
                post_id=post_id,
                text=result,
                created_at=datetime.now(),
                parent_id=parent_id,
                is_blocked=False,
                is_checked=True
            ))
