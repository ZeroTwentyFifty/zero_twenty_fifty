import pytest

from schemas.user import UserCreate, ShowUser


def test_user_create_schema_validation():
    """Test successful validation for valid user create data."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "somepassword"
    }
    user = UserCreate(**user_data)
    assert user.username == user_data["username"]
    assert user.email == user_data["email"]
    assert user.password == user_data["password"]


def test_user_create_schema_invalid_email():
    """Test validation error for invalid email."""
    invalid_data = {
        "username": "testuser",
        "email": "invalidemail",
        "password": "somepassword"
    }
    with pytest.raises(ValueError):
        UserCreate(**invalid_data)


def test_show_user_schema():
    """Test successful creation of ShowUser model."""
    show_user = ShowUser(username="testuser", email="test@example.com", is_active=True)
    assert show_user.username == "testuser"
    assert show_user.email == "test@example.com"
    assert show_user.is_active is True


# def test_show_user_schema_orm_mode():
#     """Test ORM mode for ShowUser model."""
#     # Assuming a User model with username, email, and is_active attributes
#     user_obj = User(username="testuser", email="test@example.com", is_active=True)
#     show_user = ShowUser.from_orm(user_obj)
#     assert show_user.dict() == user_obj.__dict__  # Assuming similar attribute names
