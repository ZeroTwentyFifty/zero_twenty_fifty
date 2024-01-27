from db.repository.users import create_new_user
from schemas.user import UserCreate


def test_create_new_user(db_session, test_user):
    user_data = {"username": "newuser", "email": "newuser@example.com", "password": "newuser"}
    created_user = create_new_user(user=UserCreate(**user_data), db=db_session)
    assert created_user.username == "newuser"
    assert created_user.email == "newuser@example.com"
