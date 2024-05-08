"""
This module contains functions for creating and retrieving users from the database.
"""

from sqlalchemy.orm import Session

from core.hashing import Hasher
from db.models.user import User
from schemas.user import UserCreate


def create_new_user(user: UserCreate, db: Session) -> User:
    """
    Creates a new user and adds it to the database.

    Args:
        user (UserCreate): The user data to create the new user with.
        db (Session): The database session to use.

    Returns:
        User: The newly created user.
    """
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(password=user.password),
        is_active=True,
        is_superuser=False,
    )
    print(user)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_new_superuser(user: UserCreate, db: Session) -> User:
    """
    Creates a new superuser and adds it to the database.

    Args:
        user (UserCreate): The user data to create the new superuser with.
        db (Session): The database session to use.

    Returns:
        User: The newly created superuser.
    """
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(password=user.password),
        is_active=True,
        is_superuser=True,
    )
    print(user)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def retrieve_user(*, db: Session, user_id: int) -> User:
    """
    Retrieves a user from the database by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session): The database session to use.

    Returns:
        User: The retrieved user, or None if no user was found.
    """
    item = db.query(User).filter(User.id == user_id).first()
    return item
