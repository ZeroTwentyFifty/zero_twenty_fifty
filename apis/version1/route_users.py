from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from authx import AuthX, AuthXConfig, TokenPayload

from core.config import settings
from core.error_responses import AccessDeniedError
from db.repository.users import create_new_user, retrieve_user
from db.session import get_db
from schemas.user import ShowUser
from schemas.user import UserCreate


router = APIRouter()

config = AuthXConfig()
config.JWT_SECRET_KEY = settings.SECRET_KEY
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=2)
security = AuthX(config=config)


@router.post("/", response_model=ShowUser)
def create_user(
        user: UserCreate,
        db: Session = Depends(get_db),
        current_user: TokenPayload = Depends(security.access_token_required),
):
    """
    Creates a new user.

    Args:
        user (UserCreate): The user to create.
        db (Session): The database session to use.
        current_user (TokenPayload): The current user.

    Returns:
        ShowUser: The created user.

    Raises:
        AccessDeniedError: If the current user is not a superuser.
    """
    user_info = retrieve_user(db=db, user_id=int(current_user.sub))
    if not user_info.is_superuser:
        return AccessDeniedError().to_json_response()

    user = create_new_user(user=user, db=db)
    return user
