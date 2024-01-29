from sqlalchemy import Column, Integer, String, DateTime, Enum
from enum import Enum as PyEnum
from sqlalchemy.dialects.postgresql import JSON
from db.base_class import Base
from enum import Enum as PyEnum
from sqlalchemy import String as String
from sqlalchemy import DateTime


from enum import Enum


class ProductFootprintStatus(str, Enum):
    """
    Status of a product footprint.

    Attributes:
        ACTIVE: The default status of a product footprint. A product footprint with
                status Active can be used by data recipients, e.g., for product
                footprint calculations.
        DEPRECATED: The product footprint is deprecated and should not be used for
                    e.g., product footprint calculations by data recipients.
    """

    ACTIVE = "Active"
    DEPRECATED = "Deprecated"

from sqlalchemy import Column, Integer, String, JSON


class ProductFootprint(Base):
    __tablename__ = "productfootprints"

    pk = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, index=True, comment="The product footprint identifier.")
    specVersion = Column(String, comment="The version of the ProductFootprint data specification.")
    version = Column(Integer, comment="The version of the ProductFootprint.")
    created = Column(String, comment="The timestamp of the creation of the ProductFootprint.")
    status = Column(String, comment="The status of the product footprint.")
    companyName = Column(String, comment="The name of the company that is the ProductFootprint Data Owner.")
    companyIds = Column(JSON, comment="The set of Uniform Resource Names (URN) identifying the ProductFootprint Data Owner.")
    productDescription = Column(String, comment="The free-form description of the product.")
    productIds = Column(JSON, comment="The set of ProductIds that uniquely identify the product.")
    productCategoryCpc = Column(String, comment="A UN Product Classification Code (CPC) that the given product belongs to.")
    productNameCompany = Column(String, comment="The trade name of the product.")
    comment = Column(String, comment="Additional information related to the product footprint.")
    pcf = Column(JSON, comment="The carbon footprint of the given product.")


# TODO: Replace the above model with this one, originally removed to vastly simplify
#       testing across the stack. Ultimately there is a lot of work involved in
#       getting the data model to be more realistic. I focused mainly on getting a
#       working Alpha completed first, tightening the data model is a Beta focus.
#       Utilising the pydantic data models keeps input kinda clean anyway for the time
#       being.
# class ProductFootprint(Base):
#     __tablename__ = 'product_footprint'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     pfid = Column(String)
#     spec_version = Column(String)
#     preceding_pfids = Column(ARRAY(String))  # Can store list of strings
#     version = Column(Integer)
#     created = Column(DateTime)
#     updated = Column(DateTime)
#     status = Column(PgEnum(ProductFootprintStatus))
#     status_comment = Column(String)
#     validity_period_start = Column(DateTime)
#     validity_period_end = Column(DateTime)
#     company_name = Column(String)
#     company_ids = Column(ARRAY(String))  # Can store complex JSON objects
#     product_description = Column(String)
#     product_ids = Column(ARRAY(String))  # Can store complex JSON objects
#     product_category_cpc = Column(String)
#     product_name_company = Column(String)
#     comment = Column(String)
#     pcf = Column(PydanticType(CarbonFootprint))  # Can store complex JSON objects

