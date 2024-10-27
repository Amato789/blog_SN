import pytest

from app.users.dao import UserDAO


@pytest.mark.parametrize("user_id, email, is_exist", [
    (1, "test@example.com", True),
    (2, "admin@example.com", True),
    (10, "test@test.com", False),
])
async def test_find_user_by_id(user_id: int, email: str, is_exist: bool):
    user = await UserDAO.find_by_id(user_id)

    if is_exist:
        assert user
        assert user.email == email
        assert user.id == user_id
    else:
        assert not user
