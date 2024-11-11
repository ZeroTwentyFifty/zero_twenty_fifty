import { ref, reactive } from 'vue'
import { type ProductFootprint, type FormError, DeclaredUnit } from '../types'

export function useFootprints() {
    const footprints = ref<ProductFootprint[]>([])
    const validationErrors = ref<FormError[]>([])

    const newFootprint: ProductFootprint = reactive({
        id: '', // This should be generated on the server side
        specVersion: '',
        version: 1,
        created: new Date(),
        status: ProductFootprintStatus.ACTIVE,
        companyName: '',
        companyIds: [],
        productDescription: '',
        productIds: [],
        productCategoryCpc: '',
        productNameCompany: '',
        comment: '',
        pcf: {
            declaredUnit: DeclaredUnit.kilogram,
            unitaryProductAmount: 0,
            pCfExcludingBiogenic: 0,
            fossilGhgEmissions: 0,
            fossilCarbonContent: 0,
            biogenicCarbonContent: 0,
            characterizationFactors: CharacterizationFactors.AR5,
            crossSectoralStandardsUsed: [],
            boundaryProcessesDescription: '',
            referencePeriodStart: '',
            referencePeriodEnd: '',
            geographyCountry: '',
            exemptedEmissionsPercent: 0,
            exemptedEmissionsDescription: '',
            packagingEmissionsIncluded: false
        }
    })

    const validateFootprint = (footprint: ProductFootprint): FormError[] => {
        const errors: FormError[] = [];
        if (!footprint.specVersion) errors.push({ path: 'specVersion', message: 'Spec Version is required' });
        if (!footprint.companyName) errors.push({ path: 'companyName', message: 'Company Name is required' });
        if (footprint.companyIds.length === 0) errors.push({ path: 'companyIds', message: 'At least one Company ID is required' });
        if (!footprint.productDescription) errors.push({ path: 'productDescription', message: 'Product Description is required' });
        if (footprint.productIds.length === 0) errors.push({ path: 'productIds', message: 'At least one Product ID is required' });
        if (!footprint.productCategoryCpc) errors.push({ path: 'productCategoryCpc', message: 'Product Category CPC is required' });
        if (!footprint.productNameCompany) errors.push({ path: 'productNameCompany', message: 'Product Name Company is required' });

        // Validate PCF fields
        if (!footprint.pcf.declaredUnit) errors.push({ path: 'pcf.declaredUnit', message: 'Declared Unit is required' });
        if (footprint.pcf.unitaryProductAmount <= 0) errors.push({ path: 'pcf.unitaryProductAmount', message: 'Unitary Product Amount must be greater than 0' });
        if (footprint.pcf.pCfExcludingBiogenic < 0) errors.push({ path: 'pcf.pCfExcludingBiogenic', message: 'PCF Excluding Biogenic cannot be negative' });
        if (footprint.pcf.pCfIncludingBiogenic < 0) errors.push({ path: 'pcf.pCfIncludingBiogenic', message: 'PCF Including Biogenic cannot be negative' });
        if (!footprint.pcf.characterizationFactors) errors.push({ path: 'pcf.characterizationFactors', message: 'Characterization Factors is required' });
        if (footprint.pcf.crossSectoralStandardsUsed.length === 0) errors.push({ path: 'pcf.crossSectoralStandardsUsed', message: 'At least one Cross Sectoral Standard is required' });
        if (!footprint.pcf.biogenicAccountingMethodology) errors.push({ path: 'pcf.biogenicAccountingMethodology', message: 'Biogenic Accounting Methodology is required' });
        if (!footprint.pcf.boundaryProcessesDescription) errors.push({ path: 'pcf.boundaryProcessesDescription', message: 'Boundary Processes Description is required' });
        if (!footprint.pcf.referencePeriodStart) errors.push({ path: 'pcf.referencePeriodStart', message: 'Reference Period Start is required' });
        if (!footprint.pcf.referencePeriodEnd) errors.push({ path: 'pcf.referencePeriodEnd', message: 'Reference Period End is required' });
        if (!footprint.pcf.geographyCountry) errors.push({ path: 'pcf.geographyCountry', message: 'Geography Country is required' });
        if (footprint.pcf.exemptedEmissionsPercent < 0 || footprint.pcf.exemptedEmissionsPercent > 100) errors.push({ path: 'pcf.exemptedEmissionsPercent', message: 'Exempted Emissions Percent must be between 0 and 100' });
        if (footprint.pcf.primaryDataShare < 0 || footprint.pcf.primaryDataShare > 100) errors.push({ path: 'pcf.primaryDataShare', message: 'Primary Data Share must be between 0 and 100' });

        return errors;
    }

    async function fetchFootprints() {
        try {
            const bearerToken = localStorage.getItem('bearerToken');
            if (!bearerToken) {
                throw new Error('No bearer token found');
            }

            const response = await fetch('https://localhost:8000/2/footprints', {
                headers: {
                    'Authorization': `Bearer ${bearerToken}`,
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch footprints');
            }

            const data = await response.json();
            footprints.value = data.data;
            console.log('Footprints fetched:', footprints.value);
        } catch (error) {
            console.error('Error fetching footprints:', error);
        }
    }

    async function createFootprint() {
        validationErrors.value = validateFootprint(newFootprint);
        if (validationErrors.value.length > 0) {
            console.error('Validation errors:', validationErrors.value);
            return;
        }

        try {
            const bearerToken = localStorage.getItem('bearerToken');
            if (!bearerToken) {
                throw new Error('No bearer token found');
            }

            const response = await fetch('https://localhost:8000/2/footprints/create-product-footprint/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${bearerToken}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newFootprint)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`Failed to create footprint: ${errorData.message || response.statusText}`);
            }

            const data = await response.json();
            console.log('Footprint created:', data);
            // Optionally, refresh the footprints list
            await fetchFootprints();
            // Clear the form
            Object.assign(newFootprint, {
                id: '',
                specVersion: '',
                precedingPfIds: [],
                version: 0,
                created: '',
                updated: '',
                status: '',
                statusComment: '',
                validityPeriodStart: '',
                validityPeriodEnd: '',
                companyName: '',
                companyIds: [],
                productDescription: '',
                productIds: [],
                productCategoryCpc: '',
                productNameCompany: '',
                comment: '',
                pcf: {
                    declaredUnit: DeclaredUnit['cubic meter'],
                    unitaryProductAmount: 0,
                    pCfExcludingBiogenic: 0,
                    pCfIncludingBiogenic: 0,
                    fossilGhgEmissions: 0,
                    fossilCarbonContent: 0,
                    biogenicCarbonContent: 0,
                    dLucGhgEmissions: 0,
                    landManagementGhgEmissions: 0,
                    otherBiogenicGhgEmissions: 0,
                    iLucGhgEmissions: 0,
                    biogenicCarbonWithdrawal: 0,
                    aircraftGhgEmissions: 0,
                    characterizationFactors: '',
                    crossSectoralStandardsUsed: [],
                    productOrSectorSpecificRules: [],
                    biogenicAccountingMethodology: '',
                    boundaryProcessesDescription: '',
                    referencePeriodStart: '',
                    referencePeriodEnd: '',
                    geographyCountrySubdivision: '',
                    geographyCountry: '',
                    geographyRegionOrSubregion: '',
                    secondaryEmissionFactorSources: [],
                    exemptedEmissionsPercent: 0,
                    exemptedEmissionsDescription: '',
                    packagingEmissionsIncluded: false,
                    packagingGhgEmissions: 0,
                    allocationRulesDescription: '',
                    uncertaintyAssessmentDescription: '',
                    primaryDataShare: 0,
                    dqi: {},
                    assurance: {}
                },
                extensions: []
            });
        } catch (error) {
            console.error('Error creating footprint:', error);
            validationErrors.value.push({ path: 'api', message: error.message });
        }
    }

    return {
        footprints,
        validationErrors,
        newFootprint,
        validateFootprint,
        fetchFootprints,
        createFootprint
    }
}
