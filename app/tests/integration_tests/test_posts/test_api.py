import pytest
from httpx import AsyncClient
from app.posts.dao import PostDAO


@pytest.mark.parametrize(
    "title, text, created_at, autoresponder_enabled, autoresponder_delay, "
    "is_blocked, is_checked, total_amount_posts, status_code", *[
    [(f"Post # {i}", f"There are some information about post {i}", "2024-10-27", False, 0,
      False, False, i, 200) for i in range(3, 8)]
])
async def test_add_and_get_post(
        title,
        text,
        created_at,
        autoresponder_enabled,
        autoresponder_delay,
        is_blocked,
        is_checked,
        total_amount_posts,
        status_code,
        authenticated_ac: AsyncClient
):
    response = await authenticated_ac.post("/posts", json={
        "title": title,
        "text": text,
        "created_at": created_at,
        "autoresponder_enabled": autoresponder_enabled,
        "autoresponder_delay": autoresponder_delay,
        "is_blocked": is_blocked,
        "is_checked": is_checked,
    })
    assert response.status_code == status_code

    response = await authenticated_ac.get("/posts")
    assert len(response.json()) == total_amount_posts


async def test_add_and_delete_post(authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/posts", json={
        "title": "Post # 8",
        "text": "There are some information about post 8",
        "created_at": "2024-10-27",
        "autoresponder_enabled": False,
        "autoresponder_delay": 0,
        "is_blocked": False,
        "is_checked": False,
    })
    assert response.status_code == 200

    added_post = await PostDAO.find_one_or_none(user_id=1, title="Post # 8")
    assert added_post is not None
    assert added_post.id == 8

    response = await authenticated_ac.delete(f"/posts/{added_post.id}")
    assert response.status_code == 200
    deleted_booking = await PostDAO.find_one_or_none(id=added_post.id)
    assert deleted_booking is None


async def test_add_delete_blocked_post_and_get_analytics(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get("/analytics/posts/daily-breakdown", params={
        "date_from": "2020-01-01",
        "date_to": "2024-10-27",
    })
    assert response.status_code == 200
    assert response.json()[2]["date"] == "2024-10-27"
    assert response.json()[2]["total_posts"] == 5
    assert response.json()[2]["blocked_posts"] == 0

    response = await authenticated_ac.post("/posts", json={
        "title": "Post # 9",
        "text": "There are some information about post 9",
        "created_at": "2024-10-27",
        "autoresponder_enabled": False,
        "autoresponder_delay": 0,
        "is_blocked": False,
        "is_checked": False,
    })
    assert response.status_code == 200

    added_post = await PostDAO.find_one_or_none(user_id=1, title="Post # 9")
    assert added_post is not None
    assert added_post.id == 9

    await PostDAO.set_blocked(added_post.id)

    response = await authenticated_ac.get("/analytics/posts/daily-breakdown", params={
        "date_from": "2020-01-01",
        "date_to": "2024-10-27",
    })
    assert response.status_code == 200
    assert response.json()[2]["date"] == "2024-10-27"
    assert response.json()[2]["total_posts"] == 6
    assert response.json()[2]["blocked_posts"] == 1

    response = await authenticated_ac.delete(f"/posts/{added_post.id}")
    assert response.status_code == 200
    deleted_booking = await PostDAO.find_one_or_none(id=added_post.id)
    assert deleted_booking is None