import pprint

from sqlalchemy.orm import Session

from db.models.product_footprint import ProductFootprint
from schemas.product_footprint import ProductFootprint as ProductFootprintSchema


pp = pprint.PrettyPrinter(depth=4)


def create_new_product_footprint(product_footprint: ProductFootprintSchema, db: Session):
    # TODO: Log this action
    pp.pprint(product_footprint.model_dump())
    product_footprint_dict = product_footprint.model_dump()
    # TODO: This is extremely ugly, we should be using some of the internal functionality
    #      of pydantic here instead of mutating and casting the UUID id field.
    product_footprint_dict['id'] = str(product_footprint_dict['id'])
    product_footprint_object = ProductFootprint(**product_footprint_dict)

    db.add(product_footprint_object)
    db.commit()
    db.refresh(product_footprint_object)
    return product_footprint_object


def retrieve_product_footprint(id: str, db: Session):
    # TODO: I suspect another Pydantic field here to validate that a UUID formatted
    #   string is being passed here would be a winner, improve input validation
    item = db.query(ProductFootprint).filter(ProductFootprint.id == id).first()
    return item


def list_product_footprints(db: Session):
    product_footprints = db.query(ProductFootprint).all()
    return product_footprints


def count_product_footprints(db: Session):
    count = db.query(ProductFootprint).count()
    return count


def update_product_footprint_by_id(id: int, product_footprint: ProductFootprintSchema, db: Session, owner_id):
    existing_product_footprint = db.query(ProductFootprint).filter(ProductFootprint.id == id)
    if not existing_product_footprint.first():
        return 0
    product_footprint.__dict__.update(
        owner_id=owner_id
    )  # update dictionary with new key value of owner_id
    existing_product_footprint.update(product_footprint.__dict__)
    db.commit()
    return 1


def delete_product_footprint_by_id(id: int, db: Session, owner_id):
    existing_product_footprint = db.query(ProductFootprint).filter(ProductFootprint.id == id)
    if not existing_product_footprint.first():
        return 0
    existing_product_footprint.delete(synchronize_session=False)
    db.commit()
    return 1
