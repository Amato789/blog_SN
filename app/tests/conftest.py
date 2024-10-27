import asyncio
import json
from datetime import datetime
import pytest
from httpx import ASGITransport, AsyncClient
from fastapi.testclient import TestClient  # noqa
from sqlalchemy import insert
from app.posts.models import Posts, Comments
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.main import app as fastapi_app
from app.users.models import Users


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r") as file:
            return json.load(file)

    users = open_mock_json("users")
    posts = open_mock_json("posts")

    for post in posts:
        post["created_at"] = datetime.strptime(post["created_at"], "%Y-%m-%d")

    async with async_session_maker() as session:
        for Model, values in [
            (Users, users),
            (Posts, posts),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac():
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "email": "test@example.com",
            "password": "test",
        })
        assert ac.cookies["blog_access_token"]
        yield ac
