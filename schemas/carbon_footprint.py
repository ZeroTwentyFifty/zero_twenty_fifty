from datetime import datetime
from typing import List

from pydantic import BaseModel, validator


class CarbonFootprint(BaseModel):
    declaredUnit: str
    unitaryProductAmount: int
    pCfExcludingBiogenic: int
    pCfIncludingBiogenic: int
    fossilGhgEmissions: int
    fossilCarbonContent: int
    biogenicCarbonContent: int
    characterizationFactors: str
    crossSectoralStandardsUsed: List[str]
    productOrSectorSpecificRules: List[str]
    boundaryProcessesDescription: str
    referencePeriodStart: datetime
    referencePeriodEnd: datetime
    exemptedEmissionsPercent: float
    exemptedEmissionsDescription: str
    packagingEmissionsIncluded: bool

    @validator('exemptedEmissionsPercent')
    def check_percent(cls, v):
        assert 0 <= v <= 5, "Value must be a decimal number between 0.0 and 5."
        return v
    