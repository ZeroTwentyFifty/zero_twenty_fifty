<script setup lang="ts">
import { ref } from 'vue'
import type { ProductFootprint } from '../types'

const props = defineProps<{
  footprint: ProductFootprint
}>()

const isOpen = ref(false)
</script>

<template>
  <div class="text-gray-800">
    <div @click="isOpen = !isOpen" class="cursor-pointer flex justify-between items-center p-2 hover:bg-gray-100 rounded">
      <p><strong class="text-gray-900">ID:</strong> {{ footprint.id }}</p>
      <p><strong class="text-gray-900">Status:</strong> <span :class="footprint.status === 'Active' ? 'text-green-600' : 'text-red-600'">{{ footprint.status }}</span></p>
      <UIcon name="i-heroicons-chevron-down" :class="{ 'transform rotate-180': isOpen }" class="text-gray-600" />
    </div>
    <div v-if="isOpen" class="mt-4 space-y-2 p-4 bg-white rounded border border-gray-200">
      <p class="text-gray-700"><strong class="text-gray-900">Spec Version:</strong> {{ footprint.specVersion }}</p>
      <p class="text-gray-700"><strong class="text-gray-900">Preceding PF IDs:</strong> {{ footprint.precedingPfIds?.join(', ') || 'None' }}</p>
      <p class="text-gray-700"><strong class="text-gray-900">Version:</strong> {{ footprint.version }}</p>
      <p class="text-gray-700"><strong class="text-gray-900">Created:</strong> {{ new Date(footprint.created).toLocaleString() }}</p>
      <p class="text-gray-700"><strong class="text-gray-900">Updated:</strong> {{ footprint.updated ? new Date(footprint.updated).toLocaleString() : 'N/A' }}</p>
      <p class="text-gray-700"><strong class="text-gray-900">Status Comment:</strong> {{ footprint.statusComment || 'N/A' }}</p>
      <p class="text-gray-700"><strong class="text-gray-900">Validity Period Start:</strong> {{ footprint.validityPeriodStart ? new Date(footprint.validityPeriodStart).toLocaleString() : 'N/A' }}</p>
      <p class="text-gray-700"><strong class="text-gray-900">Validity Period End:</strong> {{ footprint.validityPeriodEnd ? new Date(footprint.validityPeriodEnd).toLocaleString() : 'N/A' }}</p>
      <p class="text-gray-700"><strong class="text-gray-900">Company Name:</strong> {{ footprint.companyName }}</p>
      <p class="text-gray-700"><strong class="text-gray-900">Company IDs:</strong> {{ footprint.companyIds.join(', ') }}</p>
      <p class="text-gray-700"><strong class="text-gray-900">Product Description:</strong> {{ footprint.productDescription }}</p>
      <p class="text-gray-700"><strong class="text-gray-900">Product IDs:</strong> {{ footprint.productIds.join(', ') }}</p>
      <p class="text-gray-700"><strong class="text-gray-900">Product Category CPC:</strong> {{ footprint.productCategoryCpc }}</p>
      <p class="text-gray-700"><strong class="text-gray-900">Product Name Company:</strong> {{ footprint.productNameCompany }}</p>
      <p class="text-gray-700"><strong class="text-gray-900">Comment:</strong> {{ footprint.comment }}</p>
      <div class="mt-4">
        <h3 class="font-bold">PCF Details:</h3>
        <p class="text-gray-700"><strong class="text-gray-900">Declared Unit:</strong> {{ footprint.pcf.declaredUnit }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Unitary Product Amount:</strong> {{ footprint.pcf.unitaryProductAmount }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">PCF Excluding Biogenic:</strong> {{ footprint.pcf.pCfExcludingBiogenic }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">PCF Including Biogenic:</strong> {{ footprint.pcf.pCfIncludingBiogenic || 'N/A' }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Fossil GHG Emissions:</strong> {{ footprint.pcf.fossilGhgEmissions }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Fossil Carbon Content:</strong> {{ footprint.pcf.fossilCarbonContent }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Biogenic Carbon Content:</strong> {{ footprint.pcf.biogenicCarbonContent }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">DLUC GHG Emissions:</strong> {{ footprint.pcf.dLucGhgEmissions || 'N/A' }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Land Management GHG Emissions:</strong> {{ footprint.pcf.landManagementGhgEmissions || 'N/A' }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Other Biogenic GHG Emissions:</strong> {{ footprint.pcf.otherBiogenicGhgEmissions || 'N/A' }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">ILUC GHG Emissions:</strong> {{ footprint.pcf.iLucGhgEmissions || 'N/A' }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Biogenic Carbon Withdrawal:</strong> {{ footprint.pcf.biogenicCarbonWithdrawal || 'N/A' }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Aircraft GHG Emissions:</strong> {{ footprint.pcf.aircraftGhgEmissions || 'N/A' }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Characterization Factors:</strong> {{ footprint.pcf.characterizationFactors }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Cross Sectoral Standards Used:</strong> {{ footprint.pcf.crossSectoralStandardsUsed.join(', ') }}</p>
        <div v-if="footprint.pcf.productOrSectorSpecificRules">
          <h4 class="font-semibold">Product or Sector Specific Rules:</h4>
          <ul>
            <li v-for="(rule, index) in footprint.pcf.productOrSectorSpecificRules" :key="index">
              {{ rule.operator }} - {{ rule.ruleNames.join(', ') }}
              <span v-if="rule.otherOperatorName">({{ rule.otherOperatorName }})</span>
            </li>
          </ul>
        </div>
        <p class="text-gray-700"><strong class="text-gray-900">Biogenic Accounting Methodology:</strong> {{ footprint.pcf.biogenicAccountingMethodology || 'N/A' }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Boundary Processes Description:</strong> {{ footprint.pcf.boundaryProcessesDescription }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Reference Period Start:</strong> {{ footprint.pcf.referencePeriodStart }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Reference Period End:</strong> {{ footprint.pcf.referencePeriodEnd }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Geography Country Subdivision:</strong> {{ footprint.pcf.geographyCountrySubdivision || 'N/A' }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Geography Country:</strong> {{ footprint.pcf.geographyCountry }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Geography Region or Subregion:</strong> {{ footprint.pcf.geographyRegionOrSubregion || 'N/A' }}</p>
        <div v-if="footprint.pcf.secondaryEmissionFactorSources">
          <h4 class="font-semibold">Secondary Emission Factor Sources:</h4>
          <ul>
            <li v-for="(source, index) in footprint.pcf.secondaryEmissionFactorSources" :key="index">
              {{ source.name }} (Version: {{ source.version }})
            </li>
          </ul>
        </div>
        <p class="text-gray-700"><strong class="text-gray-900">Exempted Emissions Percent:</strong> {{ footprint.pcf.exemptedEmissionsPercent }}%</p>
        <p class="text-gray-700"><strong class="text-gray-900">Exempted Emissions Description:</strong> {{ footprint.pcf.exemptedEmissionsDescription }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Packaging Emissions Included:</strong> {{ footprint.pcf.packagingEmissionsIncluded ? 'Yes' : 'No' }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Packaging GHG Emissions:</strong> {{ footprint.pcf.packagingGhgEmissions || 'N/A' }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Allocation Rules Description:</strong> {{ footprint.pcf.allocationRulesDescription || 'N/A' }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Uncertainty Assessment Description:</strong> {{ footprint.pcf.uncertaintyAssessmentDescription || 'N/A' }}</p>
        <p class="text-gray-700"><strong class="text-gray-900">Primary Data Share:</strong> {{ footprint.pcf.primaryDataShare || 'N/A' }}%</p>
      </div>
      <div v-if="footprint.extensions && footprint.extensions.length > 0" class="mt-4">
        <h3 class="font-bold">Extensions:</h3>
        <pre>{{ JSON.stringify(footprint.extensions, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>
