"""
This module contains functions for creating and retrieving users from the database.
"""

from sqlalchemy.orm import Session

from core.hashing import Hasher
from core.logger import logger
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

    Raises:
        ValueError: If a user with the same email or username already exists.
    """
    logger.info(f"Creating a new user with email {user.email}")

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        logger.error(f"A user with email {user.email} already exists")
        raise ValueError("A user with this email already exists")

    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        logger.error(f"A user with username {user.username} already exists")
        raise ValueError("A user with this username already exists")

    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(password=user.password),
        is_active=True,
        is_superuser=False,
    )
    logger.debug(f"Adding user {user.email} to the database")
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.debug(f"Added user {user} to the database")
    logger.success(f"New superuser created with email {user.email}")
    return user


def create_new_superuser(user: UserCreate, db: Session) -> User:
    """
    Creates a new superuser and adds it to the database.

    Args:
        user (UserCreate): The user data to create the new superuser with.
        db (Session): The database session to use.

    Returns:
        User: The newly created superuser.

    Raises:
        ValueError: If a user with the same email or username already exists.
    """
    logger.info(f"Creating a new superuser with email {user.email}")

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        logger.error(f"A user with email {user.email} already exists")
        raise ValueError("A user with this email already exists")

    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        logger.error(f"A user with username {user.username} already exists")
        raise ValueError("A user with this username already exists")

    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(password=user.password),
        is_active=True,
        is_superuser=True,
    )
    logger.debug(f"Adding superuser {user.email} to the database")
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.debug(f"Added superuser {user} to the database")
    logger.success(f"New superuser created with email {user.email}")
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
    logger.info(f"Retrieving user with ID {user_id}")
    item = db.query(User).filter(User.id == user_id).first()
    if item:
        logger.success(f"User with ID {user_id} retrieved successfully")
    else:
        logger.warning(f"No user with ID {user_id} found")
    return item
