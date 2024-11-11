<script setup lang="ts">
import { useFootprints } from '../composables/useFootprints'
import FootprintDetails from './FootprintDetails.vue'

const { footprints, fetchFootprints } = useFootprints()
</script>

<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Footprints Dashboard</h2>
    <UButton @click="fetchFootprints" class="mb-4">
      Fetch Footprints
    </UButton>
    <ul v-if="footprints.length > 0" class="space-y-4 max-h-[calc(100vh-200px)] overflow-y-auto">
      <li v-for="footprint in footprints" :key="footprint.id" class="border p-4 rounded">
        <FootprintDetails :footprint="footprint" />
      </li>
    </ul>
    <p v-else>No footprints data available. Click the button to fetch data.</p>
  </div>
</template>
