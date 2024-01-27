from sqlalchemy.orm import Session

from core.hashing import Hasher
from db.models.user import User
from schemas.user import UserCreate


def create_new_user(user: UserCreate, db: Session):
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
