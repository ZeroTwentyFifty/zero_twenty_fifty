import type { UUID } from 'crypto'

export enum ProductFootprintStatus {
    ACTIVE = "Active",
    DEPRECATED = "Deprecated"
}

export const CharacterizationFactors = {
    AR5: 'AR5',
    AR6: 'AR6'
} as const;
export type CharacterizationFactors = typeof CharacterizationFactors[keyof typeof CharacterizationFactors];

export const BiogenicAccountingMethodology = {
    PEF: 'PEF',
    ISO: 'ISO',
    GHGP: 'GHGP',
    Quantis: 'Quantis'
} as const;
export type BiogenicAccountingMethodology = typeof BiogenicAccountingMethodology[keyof typeof BiogenicAccountingMethodology];

export const DeclaredUnit = {
    liter: 'liter',
    kilogram: 'kilogram',
    'cubic meter': 'cubic meter',
    'kilowatt hour': 'kilowatt hour',
    megajoule: 'megajoule',
    'ton kilometer': 'ton kilometer',
    'square meter': 'square meter'
} as const;
export type DeclaredUnit = typeof DeclaredUnit[keyof typeof DeclaredUnit];

export const RegionOrSubregion = {
    Africa: 'Africa',
    Americas: 'Americas',
    Asia: 'Asia',
    Europe: 'Europe',
    Oceania: 'Oceania',
    'Australia and New Zealand': 'Australia and New Zealand',
    'Central Asia': 'Central Asia',
    'Eastern Asia': 'Eastern Asia',
    'Eastern Europe': 'Eastern Europe',
    'Latin America and the Caribbean': 'Latin America and the Caribbean',
    Melanesia: 'Melanesia',
    Micronesia: 'Micronesia',
    'Northern Africa': 'Northern Africa',
    'Northern America': 'Northern America',
    'Northern Europe': 'Northern Europe',
    Polynesia: 'Polynesia',
    'South-eastern Asia': 'South-eastern Asia',
    'Southern Asia': 'Southern Asia',
    'Southern Europe': 'Southern Europe',
    'Sub-Saharan Africa': 'Sub-Saharan Africa',
    'Western Asia': 'Western Asia',
    'Western Europe': 'Western Europe'
} as const;
export type RegionOrSubregion = typeof RegionOrSubregion[keyof typeof RegionOrSubregion];

export const CrossSectoralStandard = {
    'GHG Protocol Product standard': 'GHG Protocol Product standard',
    'ISO Standard 14067': 'ISO Standard 14067',
    'ISO Standard 14044': 'ISO Standard 14044'
} as const;
export type CrossSectoralStandard = typeof CrossSectoralStandard[keyof typeof CrossSectoralStandard];

export const ProductOrSectorSpecificRuleOperator = {
    PEF: 'PEF',
    'EPD International': 'EPD International',
    Other: 'Other'
} as const;
export type ProductOrSectorSpecificRuleOperator = typeof ProductOrSectorSpecificRuleOperator[keyof typeof ProductOrSectorSpecificRuleOperator];

export interface ProductOrSectorSpecificRule {
    operator: ProductOrSectorSpecificRuleOperator
    ruleNames: string[]
    otherOperatorName?: string
}

export interface EmissionFactorDS {
    name: string
    version: string
}

export interface ProductFootprint {
    id: UUID
    specVersion: string
    precedingPfIds?: string[]
    version: number
    created: Date
    updated?: Date
    status: ProductFootprintStatus
    statusComment?: string
    validityPeriodStart?: Date
    validityPeriodEnd?: Date
    companyName: string
    companyIds: string[]
    productDescription: string
    productIds: string[]
    productCategoryCpc: string
    productNameCompany: string
    comment: string
    pcf: CarbonFootprint
    extensions?: Record<string, any>[]
}

export interface FormError {
    path: string
    message: string
}

export interface CarbonFootprint {
    declaredUnit: DeclaredUnit;
    unitaryProductAmount: number;
    pCfExcludingBiogenic: number;
    pCfIncludingBiogenic?: number;
    fossilGhgEmissions: number;
    fossilCarbonContent: number;
    biogenicCarbonContent: number;
    dLucGhgEmissions?: number;
    landManagementGhgEmissions?: number;
    otherBiogenicGhgEmissions?: number;
    iLucGhgEmissions?: number;
    biogenicCarbonWithdrawal?: number;
    aircraftGhgEmissions?: number;
    characterizationFactors: CharacterizationFactors;
    crossSectoralStandardsUsed: CrossSectoralStandard[];
    productOrSectorSpecificRules?: ProductOrSectorSpecificRule[];
    biogenicAccountingMethodology?: BiogenicAccountingMethodology;
    boundaryProcessesDescription: string;
    referencePeriodStart: string;
    referencePeriodEnd: string;
    geographyCountrySubdivision?: string;
    geographyCountry?: string;
    geographyRegionOrSubregion?: RegionOrSubregion;
    secondaryEmissionFactorSources?: EmissionFactorDS[];
    exemptedEmissionsPercent: number;
    exemptedEmissionsDescription: string;
    packagingEmissionsIncluded: boolean;
    packagingGhgEmissions?: number;
    allocationRulesDescription?: string;
    uncertaintyAssessmentDescription?: string;
    primaryDataShare?: number;
    dqi?: Record<string, any>;
    assurance?: Record<string, any>;
}
