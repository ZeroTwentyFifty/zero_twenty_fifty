<script setup lang="ts">
import AuthForm from './components/AuthForm.vue'
import FootprintForm from './components/FootprintForm.vue'
import FootprintList from './components/FootprintList.vue'
</script>

<template>
  <div class="flex flex-col items-center min-h-screen bg-gray-100 pt-10">
    <AuthForm class="w-full max-w-md p-6 bg-white rounded-lg shadow-md mb-6" />

    <div class="flex flex-col lg:flex-row w-full max-w-7xl space-y-6 lg:space-y-0 lg:space-x-6">
      <FootprintForm class="w-full lg:w-1/2 p-6 bg-white rounded-lg shadow-md" />
      <FootprintList class="w-full lg:w-1/2 p-6 bg-white rounded-lg shadow-md" />
    </div>
  </div>
</template>
