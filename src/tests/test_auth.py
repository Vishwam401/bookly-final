from unittest.mock import AsyncMock, patch

auth_prefix = "/api/v1/auth"


def test_create_user_account(test_client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "StrongPass123!",
        "first_name": "Test",
        "last_name": "User",
    }

    mock_new_user = {
        "uid": "some-uuid",
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "role": "user",
        "is_verified": False,
    }

    # BUG FIX 11: UserService is a module-level instance in auth/routes.py,
    # not a FastAPI dependency — app.dependency_overrides[UserService] has no
    # effect. Must patch at module level just like book_service.
    #
    # BUG FIX 12: send_email.delay() would try to reach Celery/Redis in tests.
    # Patch it so the test stays self-contained.
    with (
        patch("src.auth.routes.user_service") as mock_user_svc,
        patch("src.auth.routes.send_email") as mock_email,
    ):
        mock_user_svc.user_exists = AsyncMock(return_value=False)
        mock_user_svc.create_user = AsyncMock(return_value=mock_new_user)
        mock_email.delay = AsyncMock()

        response = test_client.post(f"{auth_prefix}/signup", json=user_data)

    assert response.status_code == 201


def test_login_user(test_client):
    login_data = {"email": "test@example.com", "password": "StrongPass123!"}

    mock_user = type("User", (), {
        "email": "test@example.com",
        "uid": "some-uid",
        "role": "user",
        "hashed_password": "hashed",
        "is_verified": True,
    })()

    with (
        patch("src.auth.routes.user_service") as mock_user_svc,
        patch("src.auth.routes.verify_password", return_value=True),
    ):
        mock_user_svc.get_user_by_email = AsyncMock(return_value=mock_user)

        response = test_client.post(f"{auth_prefix}/login", json=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_wrong_password(test_client):
    login_data = {"email": "test@example.com", "password": "WrongPass"}

    with (
        patch("src.auth.routes.user_service") as mock_user_svc,
        patch("src.auth.routes.verify_password", return_value=False),
    ):
        mock_user_svc.get_user_by_email = AsyncMock(return_value=None)

        response = test_client.post(f"{auth_prefix}/login", json=login_data)

    # InvalidCredentials -> 400
    assert response.status_code == 400