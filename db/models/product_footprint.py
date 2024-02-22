from sqlalchemy import Column, Integer, String, JSON, Enum

from db.base_class import Base
from schemas.product_footprint import ProductFootprintStatus


class ProductFootprint(Base):
    pk = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, index=True, comment="The product footprint identifier.")
    precedingPfIds = Column(JSON, comment="non-empty set of preceding product footprint identifiers without duplicates.")
    specVersion = Column(String, comment="The version of the ProductFootprint data specification.")
    version = Column(Integer, comment="The version of the ProductFootprint.")
    created = Column(String, comment="The timestamp of the creation of the ProductFootprint.")
    updated = Column(String, nullable=True, comment="The timestamp of the ProductFootprint update.")  # Keep as String for now
    status = Column(Enum(ProductFootprintStatus), comment="The status of the product footprint.")
    statusComment = Column(String, comment="If defined, the value should be a message explaining the reason for the current status.")
    validityPeriodStart = Column(String, comment="If defined, the start of the validity period of the ProductFootprint.")  # Keep as String for now
    validityPeriodEnd = Column(String, comment="The end (excluding) of the valid period of the ProductFootprint.")  # Keep as String for now
    companyName = Column(String, comment="The name of the company that is the ProductFootprint Data Owner.")
    companyIds = Column(JSON, comment="The set of Uniform Resource Names (URN) identifying the ProductFootprint Data Owner.")
    productDescription = Column(String, comment="The free-form description of the product.")
    productIds = Column(JSON, comment="The set of ProductIds that uniquely identify the product.")
    productCategoryCpc = Column(String, comment="A UN Product Classification Code (CPC) that the given product belongs to.")
    productNameCompany = Column(String, comment="The trade name of the product.")
    comment = Column(String, comment="Additional information related to the product footprint.")
    pcf = Column(JSON, comment="The carbon footprint of the given product.")
    extensions = Column(JSON, comment="If defined, 1 or more data model extensions associated with the ProductFootprint.")
