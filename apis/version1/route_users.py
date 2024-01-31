from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from db.repository.users import create_new_user
from db.session import get_db
from schemas.user import ShowUser
from schemas.user import UserCreate


router = APIRouter()


# TODO: This thing is so crufty it's ridiculous, needs to be locked down under an
#   admin scope or something similar, the only reason it exists currently is to
#   simplify test user generation, and something similar will be required in a beta
#   but it will not look like this.
@router.post("/", response_model=ShowUser)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user
