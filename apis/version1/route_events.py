
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from apis.version1.route_login import security
from db.models.user import User
from db.session import get_db


router = APIRouter()


@router.post("")
def get_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(security.access_token_required),
):
    return JSONResponse({"message": "The specified Action or header you provided implies functionality that is not implemented", "code": "NotImplemented"}, status_code=400)
