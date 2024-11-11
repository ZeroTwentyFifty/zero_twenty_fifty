<script setup lang="ts">
import { useAuth } from '../composables/useAuth'

const { state, validate, onSubmit } = useAuth()
</script>

<template>
  <UForm :validate="validate" :state="state" class="space-y-4" @submit="onSubmit">
    <UFormGroup label="Email" name="email">
      <UInput v-model="state.email" />
    </UFormGroup>

    <UFormGroup label="Password" name="password">
      <UInput v-model="state.password" type="password" />
    </UFormGroup>

    <UButton type="submit" class="w-full">
      Submit
    </UButton>
  </UForm>
</template>
