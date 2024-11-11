<script setup lang="ts">
import { useFootprints } from '../composables/useFootprints'
import { ref } from 'vue'
import {
  ProductFootprintStatus,
  CharacterizationFactors,
  BiogenicAccountingMethodology,
  DeclaredUnit,
  RegionOrSubregion,
  CrossSectoralStandard,
  ProductOrSectorSpecificRuleOperator
} from '../types'

const { newFootprint, validationErrors, createFootprint } = useFootprints()

const productOrSectorSpecificRule = ref({
  operator: '' as ProductOrSectorSpecificRuleOperator,
  ruleNames: [''],
  otherOperatorName: ''
})

const addRuleName = () => {
  productOrSectorSpecificRule.value.ruleNames.push('')
}

const removeRuleName = (index: number) => {
  productOrSectorSpecificRule.value.ruleNames.splice(index, 1)
}

const submitForm = () => {
  if (productOrSectorSpecificRule.value.operator) {
    newFootprint.pcf.productOrSectorSpecificRules = [productOrSectorSpecificRule.value]
  }
  createFootprint()
}
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Create New Footprint</h2>
    <form @submit.prevent="submitForm" class="space-y-4">
      <div>
        <label for="specVersion" class="block mb-1">Spec Version</label>
        <UInput id="specVersion" v-model="newFootprint.specVersion" required />
      </div>

      <div>
        <label for="status" class="block mb-1">Status</label>
        <USelect id="status" v-model="newFootprint.status" :options="Object.values(ProductFootprintStatus)" required />
      </div>

      <div>
        <label for="companyName" class="block mb-1">Company Name</label>
        <UInput id="companyName" v-model="newFootprint.companyName" required />
      </div>

      <div>
        <label for="companyIds" class="block mb-1">Company IDs (comma-separated)</label>
        <UInput id="companyIds" v-model="newFootprint.companyIds" @input="newFootprint.companyIds = ($event.target as HTMLInputElement).value.split(',')" required />
      </div>

      <div>
        <label for="productDescription" class="block mb-1">Product Description</label>
        <UTextarea id="productDescription" v-model="newFootprint.productDescription" required />
      </div>

      <div>
        <label for="productIds" class="block mb-1">Product IDs (comma-separated)</label>
        <UInput id="productIds" v-model="newFootprint.productIds" @input="newFootprint.productIds = ($event.target as HTMLInputElement).value.split(',')" required />
      </div>

      <div>
        <label for="productCategoryCpc" class="block mb-1">Product Category CPC</label>
        <UInput id="productCategoryCpc" v-model="newFootprint.productCategoryCpc" required />
      </div>

      <div>
        <label for="productNameCompany" class="block mb-1">Product Name Company</label>
        <UInput id="productNameCompany" v-model="newFootprint.productNameCompany" required />
      </div>

      <div>
        <label for="comment" class="block mb-1">Comment</label>
        <UTextarea id="comment" v-model="newFootprint.comment" />
      </div>

      <h3 class="text-xl font-bold mt-6 mb-2">Carbon Footprint Details</h3>

      <div>
        <label for="declaredUnit" class="block mb-1">Declared Unit</label>
        <USelect id="declaredUnit" v-model="newFootprint.pcf.declaredUnit" :options="Object.values(DeclaredUnit)" required />
      </div>

      <div>
        <label for="unitaryProductAmount" class="block mb-1">Unitary Product Amount</label>
        <UInput id="unitaryProductAmount" v-model.number="newFootprint.pcf.unitaryProductAmount" type="number" required />
      </div>

      <div>
        <label for="pCfExcludingBiogenic" class="block mb-1">PCF Excluding Biogenic</label>
        <UInput id="pCfExcludingBiogenic" v-model.number="newFootprint.pcf.pCfExcludingBiogenic" type="number" required />
      </div>

      <div>
        <label for="characterizationFactors" class="block mb-1">Characterization Factors</label>
        <USelect id="characterizationFactors" v-model="newFootprint.pcf.characterizationFactors" :options="Object.values(CharacterizationFactors)" required />
      </div>

      <div>
        <label for="crossSectoralStandardsUsed" class="block mb-1">Cross Sectoral Standards Used</label>
        <USelect id="crossSectoralStandardsUsed" v-model="newFootprint.pcf.crossSectoralStandardsUsed" :options="Object.values(CrossSectoralStandard)" multiple required />
      </div>

      <div>
        <label for="biogenicAccountingMethodology" class="block mb-1">Biogenic Accounting Methodology</label>
        <USelect id="biogenicAccountingMethodology" v-model="newFootprint.pcf.biogenicAccountingMethodology" :options="Object.values(BiogenicAccountingMethodology)" />
      </div>

      <div>
        <label for="boundaryProcessesDescription" class="block mb-1">Boundary Processes Description</label>
        <UTextarea id="boundaryProcessesDescription" v-model="newFootprint.pcf.boundaryProcessesDescription" required />
      </div>

      <div>
        <label for="referencePeriodStart" class="block mb-1">Reference Period Start</label>
        <UInput id="referencePeriodStart" v-model="newFootprint.pcf.referencePeriodStart" type="date" required />
      </div>

      <div>
        <label for="referencePeriodEnd" class="block mb-1">Reference Period End</label>
        <UInput id="referencePeriodEnd" v-model="newFootprint.pcf.referencePeriodEnd" type="date" required />
      </div>

      <div>
        <label for="geographyCountry" class="block mb-1">Geography Country</label>
        <UInput id="geographyCountry" v-model="newFootprint.pcf.geographyCountry" required />
      </div>

      <div>
        <label for="geographyRegionOrSubregion" class="block mb-1">Geography Region or Subregion</label>
        <USelect id="geographyRegionOrSubregion" v-model="newFootprint.pcf.geographyRegionOrSubregion" :options="Object.values(RegionOrSubregion)" />
      </div>

      <div>
        <h4 class="font-bold mb-2">Product or Sector Specific Rules</h4>
        <div>
          <label for="ruleOperator" class="block mb-1">Operator</label>
          <USelect id="ruleOperator" v-model="productOrSectorSpecificRule.operator" :options="Object.values(ProductOrSectorSpecificRuleOperator)" />
        </div>
        <div v-if="productOrSectorSpecificRule.operator === 'Other'">
          <label for="otherOperatorName" class="block mb-1">Other Operator Name</label>
          <UInput id="otherOperatorName" v-model="productOrSectorSpecificRule.otherOperatorName" />
        </div>
        <div v-for="(ruleName, index) in productOrSectorSpecificRule.ruleNames" :key="index">
          <label :for="'ruleName' + index" class="block mb-1">Rule Name {{ index + 1 }}</label>
          <div class="flex">
            <UInput :id="'ruleName' + index" v-model="productOrSectorSpecificRule.ruleNames[index]" class="flex-grow" />
            <UButton @click="removeRuleName(index)" class="ml-2" v-if="productOrSectorSpecificRule.ruleNames.length > 1">Remove</UButton>
          </div>
        </div>
        <UButton @click="addRuleName" class="mt-2">Add Rule Name</UButton>
      </div>

      <UButton type="submit" class="w-full">
        Create Footprint
      </UButton>
    </form>

    <div v-if="validationErrors.length > 0" class="mt-4 p-4 bg-red-100 text-red-700 rounded">
      <h3 class="font-bold mb-2">Validation Errors:</h3>
      <ul class="list-disc list-inside">
        <li v-for="error in validationErrors" :key="error.path">
          {{ error.path }}: {{ error.message }}
        </li>
      </ul>
    </div>
  </div>
</template>
