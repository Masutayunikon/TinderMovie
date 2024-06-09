// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    "@nuxtjs/tailwindcss",
    "@pinia/nuxt",
    "@pinia-plugin-persistedstate/nuxt",
    "@nuxtjs/color-mode",
    "nuxt-icon",
    "@nuxtjs/i18n"
  ],
  app: {
    head: {
      link: [{ rel: 'stylesheet', href: 'https://rsms.me/inter/inter.css' }]
    },
  },
  css: ['~/assets/css/reset.css'],
  runtimeConfig: {
    // The private keys which are only available within server-side
    accessToken: process.env.ACCESS_TOKEN,
    // Keys within public, will be also exposed to the client-side
    public: {
      fusekiEndpoint: 'http://localhost:3030/movies/sparql',
    }
  }
})
