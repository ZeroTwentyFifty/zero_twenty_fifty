from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.auth_config import get_authx_security
from core.error_responses import BadRequestError
from core.hashing import Hasher
from core.logger import logger
from core.oauth2_client_credentials import OAuth2ClientCredentialsRequestForm, OAuth2ClientCredentials
from db.repository.login import get_user
from db.session import get_db
from schemas.token import Token

router = APIRouter()
oauth2_scheme = OAuth2ClientCredentials(tokenUrl="/auth/token")

security = get_authx_security()


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(username=username, db=db)
    if not user:
        return None
    if not Hasher.verify_password(plain_password=password, hashed_password=user.hashed_password):
        return None
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(
        form_data: OAuth2ClientCredentialsRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    logger.info(f"Login attempt for client_id {form_data.client_id}")

    if form_data.client_id and form_data.client_secret:
        client_id = form_data.client_id
        client_secret = form_data.client_secret
    else:
        logger.warning("Missing client_id or client_secret")
        return BadRequestError().to_json_response()

    user = authenticate_user(client_id, client_secret, db)
    if not user:
        logger.error(f"Authentication failed for client_id {client_id}")
        return JSONResponse({"error": "invalid_client", "error_description": "Authentication failed"}, status_code=400)

    access_token: str = security.create_access_token(uid=str(user.id), sub=user.email)

    logger.success(f"Access token created for user {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}
