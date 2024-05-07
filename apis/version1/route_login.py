from datetime import timedelta, datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.config import settings
from core.error_responses import BadRequestError
from core.hashing import Hasher
from core.oauth2_client_credentials import OAuth2ClientCredentialsRequestForm, OAuth2ClientCredentials
from db.repository.login import get_user
from db.session import get_db
from schemas.token import Token
from authx import AuthX, AuthXConfig

router = APIRouter()
oauth2_scheme = OAuth2ClientCredentials(tokenUrl="/auth/token")

config = AuthXConfig()
config.JWT_SECRET_KEY = settings.SECRET_KEY
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=2)
security = AuthX(config=config)


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
    if form_data.client_id and form_data.client_secret:
        client_id = form_data.client_id
        client_secret = form_data.client_secret
    else:
        return BadRequestError().to_json_response()

    user = authenticate_user(client_id, client_secret, db)
    if not user:    
        return JSONResponse({"error": "invalid_client", "error_description": "Authentication failed"}, status_code=400)

    # TODO: Remove the sub with user.email, and update the uid to be something more legitimate
    access_token: str = security.create_access_token(uid="USER_ID", sub=user.email)

    return {"access_token": access_token, "token_type": "bearer"}
