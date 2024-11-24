<script setup lang="ts">
import { useFootprints } from '../composables/useFootprints'
import FootprintDetails from './FootprintDetails.vue'

const { footprints, fetchFootprints } = useFootprints()
</script>

<template>
  <div class="bg-white p-6 rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-4 text-gray-800">Footprints Dashboard</h2>
    <UButton 
      @click="fetchFootprints" 
      class="mb-4 bg-blue-600 hover:bg-blue-700 text-white"
    >
      Fetch Footprints
    </UButton>
    <ul v-if="footprints.length > 0" class="space-y-4 max-h-[calc(100vh-200px)] overflow-y-auto">
      <li v-for="footprint in footprints" :key="footprint.id" class="border border-gray-200 p-4 rounded bg-gray-50">
        <FootprintDetails :footprint="footprint" />
      </li>
    </ul>
    <p v-else class="text-gray-700">No footprints data available. Click the button to fetch data.</p>
  </div>
</template>
