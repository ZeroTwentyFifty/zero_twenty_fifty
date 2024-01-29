from db.models.product_footprint import ProductFootprint, ProductFootprintStatus


def test_product_footprint_creation(db_session):
    product_footprint = ProductFootprint(
        id="test_id",
        specVersion="1.0",
        version=1,
        created="2022-01-01",
        status="Active",
        companyName="Test Company",
        companyIds=[],
        productDescription="Test Product",
        productIds=[],
        productCategoryCpc="Test Category",
        productNameCompany="Test Product Name",
        comment="Test Comment",
        pcf={}
    )
    db_session.add(product_footprint)
    db_session.commit()

    assert product_footprint.id == "test_id"
    assert product_footprint.specVersion == "1.0"
    assert product_footprint.version == 1
    assert product_footprint.created == "2022-01-01"
    assert product_footprint.status == "Active"
    assert product_footprint.companyName == "Test Company"
    assert product_footprint.companyIds == []
    assert product_footprint.productDescription == "Test Product"
    assert product_footprint.productIds == []
    assert product_footprint.productCategoryCpc == "Test Category"
    assert product_footprint.productNameCompany == "Test Product Name"
    assert product_footprint.comment == "Test Comment"
    assert product_footprint.pcf == {}


def test_product_footprint_status_values():
    assert ProductFootprintStatus.ACTIVE == "Active"
    assert ProductFootprintStatus.DEPRECATED == "Deprecated"
