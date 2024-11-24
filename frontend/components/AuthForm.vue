<script setup lang="ts">
import { useAuth } from '../composables/useAuth'
import { useRouter } from 'vue-router'

const { state, validate, onSubmit } = useAuth()
const router = useRouter()

async function handleSubmit(event: Event) {
  event.preventDefault()
  const success = await onSubmit(event)
  if (success) {
    router.push('/dashboard')
  }
}
</script>

<template>
  <div class="bg-white p-6 rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-4 text-gray-800">Login</h2>
    <UForm :validate="validate" :state="state" class="space-y-4" @submit="handleSubmit">
      <UFormGroup label="Email" name="email" class="text-gray-700">
        <UInput v-model="state.email" class="border-gray-300" />
      </UFormGroup>

      <UFormGroup label="Password" name="password" class="text-gray-700">
        <UInput v-model="state.password" type="password" class="border-gray-300" />
      </UFormGroup>

      <UButton type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white">
        Submit
      </UButton>
    </UForm>
  </div>
</template>
