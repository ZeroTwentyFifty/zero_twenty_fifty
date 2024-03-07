from sqlalchemy import Column, Integer, String, JSON, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import relationship

from db.base_class import Base
from schemas.product_footprint import ProductFootprintStatus


class ProductFootprint(Base):
    pk = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, index=True, comment="The product footprint identifier.")
    # need some smarts around this
    precedingPfIds = Column(ARRAY(String), comment="non-empty set of preceding product footprint identifiers without duplicates.")
    specVersion = Column(String, comment="The version of the ProductFootprint data specification.")
    version = Column(Integer, comment="The version of the ProductFootprint.")
    created = Column(DateTime(timezone=True), comment="The timestamp of the creation of the ProductFootprint.")
    updated = Column(DateTime(timezone=True), nullable=True, comment="The timestamp of the ProductFootprint update.")
    status = Column(Enum(ProductFootprintStatus), comment="The status of the product footprint.")
    statusComment = Column(String, comment="If defined, the value should be a message explaining the reason for the current status.")
    validityPeriodStart = Column(DateTime(timezone=True), nullable=True, comment="If defined, the start of the validity period of the ProductFootprint.")
    validityPeriodEnd = Column(DateTime(timezone=True), nullable=True, comment="The end (excluding) of the valid period of the ProductFootprint.")
    companyName = Column(String, comment="The name of the company that is the ProductFootprint Data Owner.")
    companyIds = Column(ARRAY(String), comment="The set of Uniform Resource Names (URN) identifying the ProductFootprint Data Owner.")
    productDescription = Column(String, comment="The free-form description of the product.")
    productIds = Column(ARRAY(String), comment="The set of ProductIds that uniquely identify the product.")
    productCategoryCpc = Column(String, comment="A UN Product Classification Code (CPC) that the given product belongs to.")
    productNameCompany = Column(String, comment="The trade name of the product.")
    comment = Column(String, comment="Additional information related to the product footprint.", nullable=False)
    carbon_footprint = relationship("CarbonFootprintModel", back_populates="product_footprint", uselist=False)
    extensions = Column(JSONB, comment="If defined, 1 or more data model extensions associated with the ProductFootprint.")
