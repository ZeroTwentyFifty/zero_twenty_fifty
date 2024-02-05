from fastapi import APIRouter

from apis.version1 import route_login
from apis.version1 import route_users
from apis.version1 import route_events
from apis.version1 import route_product_footprints


api_router = APIRouter(
    redirect_slashes=False
)
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_login.router, prefix="/auth", tags=["auth"])
api_router.include_router(route_events.router, prefix="/events", tags=["events"])
api_router.include_router(route_product_footprints.router, prefix="/footprints", tags=["product_footprints"])
