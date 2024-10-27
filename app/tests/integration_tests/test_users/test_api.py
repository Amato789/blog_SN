import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("email, password, status_code", [
    ("kot@pes.com", "kotopes", 201),
    ("kot@pes.com", "kot0pes", 409),
    ("pes@kot.com", "kotopes", 201),
    ("vdfxcv", "kotopes", 422),
])
async def test_register_user(email: str, password: str, status_code: int, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password,
    })
    assert response.status_code == status_code


@pytest.mark.parametrize("email, password, status_code", [
    ("test@example.com", "test", 200),
    ("admin@example.com", "artem", 200),
    ("wrong_person@example.com", "test2", 401),
])
async def test_login_user(email: str, password: str, status_code: int, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password,
    })
    assert response.status_code == status_code
