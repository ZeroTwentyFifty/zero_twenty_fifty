
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from apis.version1.route_login import security
from core.error_responses import NotImplementedError
from db.models.user import User
from db.session import get_db


router = APIRouter()


@router.post("")
def get_events(
    db: Session = Depends(get_db),
    current_user: User = Depends(security.access_token_required),
):
    return NotImplementedError().to_json_response()
