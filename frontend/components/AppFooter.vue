<template>
  <UFooter class="bg-blue-500 text-white p-4 fixed bottom-0 w-full">
    <div class="container mx-auto flex justify-between items-center">
      <h1 class="text-xl font-bold">ZeroTwentyFifty</h1>
      <nav>
        <ul class="flex space-x-4">
          <li><NuxtLink to="/">Home</NuxtLink></li>
          <li><NuxtLink to="/dashboard">Dashboard</NuxtLink></li>
          <li><NuxtLink to="/about">About</NuxtLink></li>
        </ul>
      </nav>
    </div>
  </UFooter>
</template>

<script setup lang="ts">
</script>

<style scoped>
/* No additional styles needed for sticky footer */
</style>