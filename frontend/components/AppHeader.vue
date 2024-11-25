<template>
    <UHorizontalNavigation :links="links" class="border-b border-gray-200 dark:border-gray-800" />
  </template>
  
<script setup lang="ts">
const links = [{
  label: 'Profile',
  avatar: {
    src: 'https://avatars.githubusercontent.com/u/739984?v=4'
  },
  badge: 100
}, {
  label: 'Home',
  icon: 'i-heroicons-home',
  to: '/'
}, {
  label: 'Dashboard',
  icon: 'i-heroicons-chart-bar',
  to: '/dashboard'
}, {
  label: 'About',
  icon: 'i-heroicons-information-circle',
  to: '/about'
}]
</script>
  