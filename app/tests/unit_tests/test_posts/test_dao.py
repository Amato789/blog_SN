import pytest
from app.posts.dao import PostDAO


@pytest.mark.parametrize("post_id, user_id, title, is_exist", [
    (1, 1, "Post # 1", True),
    (2, 2, "Post # 2", True),
    (30, 1, "Post # 30", False),
])
async def test_find_post_by_id(post_id: int, user_id: int, title: str, is_exist: bool):
    post = await PostDAO.find_by_id(post_id)

    if is_exist:
        assert post
        assert post.id == post_id
        assert post.user_id == user_id
        assert post.title == title
    else:
        assert not post
