from fastapi_pagination import paginate
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from apis.version1.route_login import get_current_user_from_token
from core.exceptions import NoSuchFootprintException
from core.pagination import JSONAPIPage
from db.models.user import User
from db.repository.product_footprints import create_new_product_footprint
from db.repository.product_footprints import list_product_footprints
from db.repository.product_footprints import retrieve_product_footprint
from db.session import get_db
from schemas.product_footprint import ProductFootprint


router = APIRouter()


"""
TODO: Implement full CRUD functionality for this module.
"""

@router.post("/create-product-footprint/", status_code=200)
def create_product_footprint(
    product_footprint: ProductFootprint,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    product_footprint = create_new_product_footprint(product_footprint=product_footprint, db=db)
    if product_footprint:
        return "Success"


@router.get("/{id}", response_model=dict[str, ProductFootprint], status_code=200)
def read_product_footprint(id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    product_footprint = retrieve_product_footprint(id=id, db=db)
    if not product_footprint:
        raise NoSuchFootprintException
    return {'data': product_footprint}


@router.get("", response_model=JSONAPIPage[ProductFootprint], status_code=200)
def list_footprints(db: Session = Depends(get_db), current_user: User = Depends(get_current_user_from_token)):
    """
    TODO: This route is currently not tested due to the pagination module being too difficult
        to programmatically interact with, during alpha, it will be tuned up and formed into
        something far more workable, and with that will come tests, currently it is not easy
        to understand, the code was added in so that the PoC could move forward and an ALpha
        release needs to happen sooner rather than later.
    """
    product_footprints = list_product_footprints(db=db)
    if not product_footprints:
        raise NoSuchFootprintException
    return paginate(product_footprints)
