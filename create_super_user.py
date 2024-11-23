import os
import getpass
from sqlalchemy.orm import Session
from core.hashing import Hasher
from db.models.user import User
from schemas.user import UserCreate

def create_superuser(db: Session):
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match")
        return

    user = User(
        username=username,
        email=email,
        hashed_password=Hasher.get_password_hash(password=password),
        is_active=True,
        is_superuser=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    print("Superuser created successfully")

if __name__ == "__main__":
    from db.session import engine

    with Session(engine) as db:
        create_superuser(db)