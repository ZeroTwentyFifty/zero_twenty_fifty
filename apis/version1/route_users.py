from authx import TokenPayload
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from core.auth_config import get_authx_security
from core.error_responses import AccessDeniedError, DuplicateEntryError
from core.logger import logger
from db.repository.users import create_new_user, retrieve_user_by_id
from db.session import get_db
from schemas.user import ShowUser
from schemas.user import UserCreate


router = APIRouter()
security = get_authx_security()


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
        DuplicateEntryError: If a user with the same email or username already exists.
    """
    logger.info(f"Creating a new user with email {user.email}")

    user_id = int(current_user.sub)
    user_info = retrieve_user_by_id(db=db, user_id=user_id)
    if not user_info.is_superuser:
        logger.warning(f"Access denied for user {current_user.sub} trying to create a new user")
        return AccessDeniedError().to_json_response()

    try:
        user = create_new_user(user=user, db=db)
        logger.success(f"New user created with email {user.email}")
        return user
    except ValueError as e:
        logger.error(f"Error creating a new user: {str(e)}")
        return DuplicateEntryError(message=str(e)).to_json_response()
