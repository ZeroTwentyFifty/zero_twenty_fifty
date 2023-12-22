from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import field_validator, ConfigDict, BaseModel, Field

from schemas.carbon_footprint import CarbonFootprint


class ProductFootprint(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    specVersion: str
    version: int
    created: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str
    companyName: str
    companyIds: list[str]
    productDescription: str
    productIds: list[str]
    productCategoryCpc: str 
    productNameCompany: str
    comment: str
    pcf: CarbonFootprint

    @field_validator('version')
    @classmethod
    def check_version(cls, v):
        assert 0 <= v <= 2**31-1, "Version value must be an integer in the inclusive range of 0 to 2^31-1."
        return v

    @field_validator('status')
    @classmethod
    def check_status(cls, v):
        valid_statuses = ['Active', 'Deprecated']
        assert v in valid_statuses, f"Status must be one of the following: {', '.join(valid_statuses)}"
        return v
    model_config = ConfigDict(from_attributes=True)
