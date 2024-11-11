<script setup lang="ts">
import { ref } from 'vue'
import type { ProductFootprint } from '../types'

const props = defineProps<{
  footprint: ProductFootprint
}>()

const isOpen = ref(false)
</script>

<template>
  <div>
    <div @click="isOpen = !isOpen" class="cursor-pointer flex justify-between items-center">
      <p><strong>ID:</strong> {{ footprint.id }}</p>
      <p><strong>Status:</strong> {{ footprint.status }}</p>
      <UIcon name="i-heroicons-chevron-down" :class="{ 'transform rotate-180': isOpen }" />
    </div>
    <div v-if="isOpen" class="mt-4 space-y-2">
      <p><strong>Spec Version:</strong> {{ footprint.specVersion }}</p>
      <p><strong>Preceding PF IDs:</strong> {{ footprint.precedingPfIds?.join(', ') || 'None' }}</p>
      <p><strong>Version:</strong> {{ footprint.version }}</p>
      <p><strong>Created:</strong> {{ new Date(footprint.created).toLocaleString() }}</p>
      <p><strong>Updated:</strong> {{ footprint.updated ? new Date(footprint.updated).toLocaleString() : 'N/A' }}</p>
      <p><strong>Status Comment:</strong> {{ footprint.statusComment || 'N/A' }}</p>
      <p><strong>Validity Period Start:</strong> {{ footprint.validityPeriodStart ? new Date(footprint.validityPeriodStart).toLocaleString() : 'N/A' }}</p>
      <p><strong>Validity Period End:</strong> {{ footprint.validityPeriodEnd ? new Date(footprint.validityPeriodEnd).toLocaleString() : 'N/A' }}</p>
      <p><strong>Company Name:</strong> {{ footprint.companyName }}</p>
      <p><strong>Company IDs:</strong> {{ footprint.companyIds.join(', ') }}</p>
      <p><strong>Product Description:</strong> {{ footprint.productDescription }}</p>
      <p><strong>Product IDs:</strong> {{ footprint.productIds.join(', ') }}</p>
      <p><strong>Product Category CPC:</strong> {{ footprint.productCategoryCpc }}</p>
      <p><strong>Product Name Company:</strong> {{ footprint.productNameCompany }}</p>
      <p><strong>Comment:</strong> {{ footprint.comment }}</p>
      <div class="mt-4">
        <h3 class="font-bold">PCF Details:</h3>
        <p><strong>Declared Unit:</strong> {{ footprint.pcf.declaredUnit }}</p>
        <p><strong>Unitary Product Amount:</strong> {{ footprint.pcf.unitaryProductAmount }}</p>
        <p><strong>PCF Excluding Biogenic:</strong> {{ footprint.pcf.pCfExcludingBiogenic }}</p>
        <p><strong>PCF Including Biogenic:</strong> {{ footprint.pcf.pCfIncludingBiogenic || 'N/A' }}</p>
        <p><strong>Fossil GHG Emissions:</strong> {{ footprint.pcf.fossilGhgEmissions }}</p>
        <p><strong>Fossil Carbon Content:</strong> {{ footprint.pcf.fossilCarbonContent }}</p>
        <p><strong>Biogenic Carbon Content:</strong> {{ footprint.pcf.biogenicCarbonContent }}</p>
        <p><strong>DLUC GHG Emissions:</strong> {{ footprint.pcf.dLucGhgEmissions || 'N/A' }}</p>
        <p><strong>Land Management GHG Emissions:</strong> {{ footprint.pcf.landManagementGhgEmissions || 'N/A' }}</p>
        <p><strong>Other Biogenic GHG Emissions:</strong> {{ footprint.pcf.otherBiogenicGhgEmissions || 'N/A' }}</p>
        <p><strong>ILUC GHG Emissions:</strong> {{ footprint.pcf.iLucGhgEmissions || 'N/A' }}</p>
        <p><strong>Biogenic Carbon Withdrawal:</strong> {{ footprint.pcf.biogenicCarbonWithdrawal || 'N/A' }}</p>
        <p><strong>Aircraft GHG Emissions:</strong> {{ footprint.pcf.aircraftGhgEmissions || 'N/A' }}</p>
        <p><strong>Characterization Factors:</strong> {{ footprint.pcf.characterizationFactors }}</p>
        <p><strong>Cross Sectoral Standards Used:</strong> {{ footprint.pcf.crossSectoralStandardsUsed.join(', ') }}</p>
        <div v-if="footprint.pcf.productOrSectorSpecificRules">
          <h4 class="font-semibold">Product or Sector Specific Rules:</h4>
          <ul>
            <li v-for="(rule, index) in footprint.pcf.productOrSectorSpecificRules" :key="index">
              {{ rule.operator }} - {{ rule.ruleNames.join(', ') }}
              <span v-if="rule.otherOperatorName">({{ rule.otherOperatorName }})</span>
            </li>
          </ul>
        </div>
        <p><strong>Biogenic Accounting Methodology:</strong> {{ footprint.pcf.biogenicAccountingMethodology || 'N/A' }}</p>
        <p><strong>Boundary Processes Description:</strong> {{ footprint.pcf.boundaryProcessesDescription }}</p>
        <p><strong>Reference Period Start:</strong> {{ footprint.pcf.referencePeriodStart }}</p>
        <p><strong>Reference Period End:</strong> {{ footprint.pcf.referencePeriodEnd }}</p>
        <p><strong>Geography Country Subdivision:</strong> {{ footprint.pcf.geographyCountrySubdivision || 'N/A' }}</p>
        <p><strong>Geography Country:</strong> {{ footprint.pcf.geographyCountry }}</p>
        <p><strong>Geography Region or Subregion:</strong> {{ footprint.pcf.geographyRegionOrSubregion || 'N/A' }}</p>
        <div v-if="footprint.pcf.secondaryEmissionFactorSources">
          <h4 class="font-semibold">Secondary Emission Factor Sources:</h4>
          <ul>
            <li v-for="(source, index) in footprint.pcf.secondaryEmissionFactorSources" :key="index">
              {{ source.name }} (Version: {{ source.version }})
            </li>
          </ul>
        </div>
        <p><strong>Exempted Emissions Percent:</strong> {{ footprint.pcf.exemptedEmissionsPercent }}%</p>
        <p><strong>Exempted Emissions Description:</strong> {{ footprint.pcf.exemptedEmissionsDescription }}</p>
        <p><strong>Packaging Emissions Included:</strong> {{ footprint.pcf.packagingEmissionsIncluded ? 'Yes' : 'No' }}</p>
        <p><strong>Packaging GHG Emissions:</strong> {{ footprint.pcf.packagingGhgEmissions || 'N/A' }}</p>
        <p><strong>Allocation Rules Description:</strong> {{ footprint.pcf.allocationRulesDescription || 'N/A' }}</p>
        <p><strong>Uncertainty Assessment Description:</strong> {{ footprint.pcf.uncertaintyAssessmentDescription || 'N/A' }}</p>
        <p><strong>Primary Data Share:</strong> {{ footprint.pcf.primaryDataShare || 'N/A' }}%</p>
      </div>
      <div v-if="footprint.extensions && footprint.extensions.length > 0" class="mt-4">
        <h3 class="font-bold">Extensions:</h3>
        <pre>{{ JSON.stringify(footprint.extensions, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>
