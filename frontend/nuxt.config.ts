// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  modules: ["@nuxt/ui"],
  ui: {
    global: true,
    colors: {
      primary: 'blue',
      gray: 'cool'  // or 'neutral', 'slate', 'zinc', etc.
    }
  },
  runtimeConfig: {
    // Server-side environment variables
    apiSecret: '',
    // Client-side environment variables (public)
    public: {
      apiBase: 'http://localhost:8000'
    }
  }
})