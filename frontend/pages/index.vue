<template>
  <div class="landing-page">
    <h1 class="text-3xl font-bold mb-6">Welcome to Our App</h1>
    <AuthForm />
  </div>
</template>

<script setup lang="ts">
import AuthForm from '@/components/AuthForm.vue'
</script>

<style scoped>
.landing-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}
</style>