<script setup lang="ts">
import { useAuth } from '../composables/useAuth'
import { useRouter } from 'vue-router'

const { state, validate, onSubmit } = useAuth()
const router = useRouter()

async function handleSubmit(event: FormSubmitEvent<any>) {
  const success = await onSubmit(event)
  if (success) {
    router.push('/dashboard')
  }
}
</script>

<template>
  <UCard class="max-w-md mx-auto">
    <UCardTitle class="text-2xl font-bold mb-4">Login</UCardTitle>
    <UForm 
      :validate="validate"
      :state="state"
      class="space-y-4"
      @submit="handleSubmit"
    >
      <UFormGroup label="Email" name="email">
        <UInput
          v-model="state.email"
          color="primary"
          variant="outline"
          placeholder="Enter your email"
        />
      </UFormGroup>

      <UFormGroup label="Password" name="password">
        <UInput 
          v-model="state.password"
          type="password"
          color="primary"
          variant="outline"
          placeholder="Enter your password"
        />
      </UFormGroup>

      <UButton
        type="submit"
        color="primary"
        variant="solid"
        block
      >
        Login
      </UButton>
    </UForm>
  </UCard>
</template>
