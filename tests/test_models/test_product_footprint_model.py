import pytest
from sqlalchemy.exc import IntegrityError

from db.models.product_footprint import ProductFootprint, ProductFootprintStatus
from db.models.carbon_footprint import CarbonFootprintModel


def test_product_footprint_creation(db_session, valid_product_footprint_model, valid_carbon_footprint_model):

    product_footprint = valid_product_footprint_model
    carbon_footprint = valid_carbon_footprint_model

    product_footprint.carbon_footprint = carbon_footprint

    db_session.add(product_footprint)
    db_session.commit()

    item = db_session.query(ProductFootprint).filter(ProductFootprint.id == 'test_id').first()
    assert item.id == "test_id"
    assert item.specVersion == "1.0"
    assert item.version == 1
    assert item.created.isoformat() == '2023-01-01T00:00:00+00:00'
    # assert product_footprint.status == ProductFootprintStatus.ACTIVE
    # assert product_footprint.companyName == "Test Company"
    # assert product_footprint.companyIds == []
    # assert product_footprint.productDescription == "Test Product"
    # assert product_footprint.productIds == []
    # assert product_footprint.productCategoryCpc == "Test Category"
    # assert product_footprint.productNameCompany == "Test Product Name"
    # assert product_footprint.comment == "Test Comment"
    assert isinstance(item.carbon_footprint, CarbonFootprintModel)


def test_product_footprint_status_values():
    assert ProductFootprintStatus.ACTIVE.value == "Active"
    assert ProductFootprintStatus.DEPRECATED.value == "Deprecated"


def test_product_footprint_id_field_is_unique(db_session):
    # Create a record
    record1 = ProductFootprint(
        id="test_for_uniqueness",
        comment="test"
    )
    db_session.add(record1)
    db_session.commit()

    # Attempt to create another record with the same id
    record2 = ProductFootprint(
        id="test_for_uniqueness",
        comment = "test"
    )
    db_session.add(record2)
    with pytest.raises(IntegrityError, match="duplicate key value violates unique constraint"):
        db_session.commit()

    db_session.close()


def test_product_footprint_deletion_results_in_carbon_footprint_deletion(db_session, valid_product_footprint_model, valid_carbon_footprint_model):
    """Tests if deleting a ProductFootprint cascades to CarbonFootprint"""
    product_footprint = valid_product_footprint_model
    carbon_footprint = valid_carbon_footprint_model

    product_footprint.carbon_footprint = carbon_footprint
    db_session.add(product_footprint)

    db_session.commit()

    db_session.delete(product_footprint)
    db_session.commit()

    assert db_session.query(CarbonFootprintModel).count() == 0
