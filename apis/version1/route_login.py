from datetime import timedelta

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from jose import jwt
from jose import JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session

from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token
from core.oauth2_client_credentials import OAuth2ClientCredentialsRequestForm, OAuth2ClientCredentials
from db.repository.login import get_user
from db.session import get_db
from schemas.token import Token

router = APIRouter()
oauth2_scheme = OAuth2ClientCredentials(tokenUrl="/auth/token")


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user(username=username, db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(plain_password=password, hashed_password=user.hashed_password):
        return False
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
        return JSONResponse({"message": "Bad Request", "code": "BadRequest"}, status_code=400)

    user = authenticate_user(client_id, client_secret, db)
    if not user:    
        return JSONResponse({"message": "Access Denied", "code": "AccessDenied"}, status_code=403)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        print("username/email extracted is ", username)
        if username is None:
            return JSONResponse({"message": "Access Denied", "code": "AccessDenied"}, status_code=403)
    except ExpiredSignatureError:
        return JSONResponse({"message": "The specified access token has expired", "code": "TokenExpired"}, status_code=401)
    except JWTError:
        raise HTTPException(
                status_code=403,
                detail="AccessDenied OAuth2 Client Credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # return JSONResponse({"message": "Access Denied", "code": "AccessDenied"}, status_code=403)
    
    user = get_user(username=username, db=db)
    if user is None:
        return JSONResponse({"message": "Access Denied", "code": "AccessDenied"}, status_code=403)
    return user
