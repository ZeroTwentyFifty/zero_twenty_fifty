from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import AwareDatetime, BaseModel, Field, conint, UUID4

from schemas.carbon_footprint import CarbonFootprint


class ProductFootprintStatus(Enum):
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


class ProductFootprint(BaseModel):
    """
    CompanyIds and ProductIds field validation is wrong, should be a list of URN's,
    not `str`.

    See Also:
        https://wbcsd.github.io/tr/2023/data-exchange-protocol-20231207/#dt-pf
    """
    id: UUID4 = Field(..., description='The product footprint identifier.')
    specVersion: str = Field(
        ...,
        description='The version of the ProductFootprint data specification with value [VERSION]. Advisement: Subsequent revisions will update this value according to Semantic Versioning 2.0.0 (https://semver.org/lang/en/).',
    )
    precedingPfIds: Optional[List[str]] = Field(
        None,
        description='If defined, MUST be a non-empty set of preceding product footprint identifiers without duplicates.',
        min_length=1,
    )
    version: conint(ge=0, le=2147483647) = Field(
        ...,
        description='The version of the ProductFootprint with value an integer in the inclusive range of 0..2^31-1.',
    )
    created: AwareDatetime = Field(
        ...,
        description="A ProductFootprint MUST include the property 'created' with value the timestamp of the creation of the ProductFootprint.",
    )
    updated: Optional[AwareDatetime] = Field(
        None,
        description="A ProductFootprint SHOULD include the property 'updated' with value the timestamp of the ProductFootprint update. A ProductFootprint MUST NOT include this property if an update has never been performed. The timestamp MUST be in UTC.",
    )
    status: ProductFootprintStatus = Field(
        ...,
        description="Each ProductFootprint MUST include the property 'status' with value one of the following values: Active or Deprecated.",
    )
    statusComment: Optional[str] = Field(
        None,
        description='If defined, the value should be a message explaining the reason for the current status.',
    )
    validityPeriodStart: Optional[AwareDatetime] = Field(
        None,
        description='If defined, the start of the validity period of the ProductFootprint.',
    )
    validityPeriodEnd: Optional[AwareDatetime] = Field(
        None,
        description='The end (excluding) of the valid period of the ProductFootprint.',
    )
    companyName: str = Field(
        ...,
        description='The name of the company that is the ProductFootprint Data Owner, with value a non-empty String.',
    )
    companyIds: List[str] = Field(
        ...,
        description='The non-empty set of Uniform Resource Names (URN). Each value of this set is supposed to uniquely identify the ProductFootprint Data Owner.',
    )
    productDescription: str = Field(
        ...,
        description='The free-form description of the product plus other information related to it such as production technology or packaging.',
    )
    productIds: List[str] = Field(
        ...,
        description='The non-empty set of ProductIds. Each of the values in the set is supposed to uniquely identify the product. What constitutes a suitable product identifier depends on the product, the conventions, contracts, and agreements between the Data Owner and a Data Recipient and is out of the scope of this specification.',
        min_length=1,
    )
    productCategoryCpc: str = Field(
        ...,
        description='A UN Product Classification Code (CPC) that the given product belongs to.',
    )
    productNameCompany: str = Field(
        ..., description='The non-empty trade name of the product.'
    )
    comment: str = Field(
        ...,
        description='The additional information related to the product footprint. Whereas the property ProductFootprint/productDescription contains product-level information, ProductFootprint/comment SHOULD be used for information and instructions related to the calculation of the footprint, or other information which informs the ability to interpret, to audit or to verify the Product Footprint.',
    )
    pcf: CarbonFootprint = Field(
        ...,
        description='The carbon footprint of the given product with value conforming to the data type CarbonFootprint.',
    )
    extensions: Optional[List[Dict[str, Any]]] = Field(
        None,
        description='If defined, 1 or more data model extensions associated with the ProductFootprint. ProductFootprint/extensions MUST be encoded as a non-empty JSON Array of DataModelExtension JSON objects.',
        min_length=1,
    )
