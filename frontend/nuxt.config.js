const development = process.env.NODE_ENV !== 'production'

export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,

  // Target: https://go.nuxtjs.dev/config-target
  target: 'static',

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'Project Insight',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: ['@/assets/scss/main.scss'],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  // TODO: This causes a 'Uncaught (in promise) DOMException: The operation is insecure.' error in Firefox
  plugins: ['@/plugins/apexcharts.js', '@/plugins/country-flags.js'],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/buefy
    ['nuxt-buefy', { css: false }],
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    // https://go.nuxtjs.dev/pwa
    '@nuxtjs/pwa',
    // https://i18n.nuxtjs.org
    ['@nuxtjs/i18n', {
      locales: [
        {
          code: 'en',
          name: 'English',
          file: 'en.js',
          flagkey: 'gb',
        },
        {
          code: 'de',
          name: 'Deutsch',
          file: 'de.js',
          flagkey: 'de',
        },
      ],
      lazy: true,
      langDir: 'lang/',
      defaultLocale: 'en',
    }],
  ],  

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
    // instead of baseUrl these individual values can be used
    // https: development ? false : (process.env.USE_HTTPS === 'true'),
    // host: development ? 'localhost' : process.env.BACKEND_HOST,
    // port: development ? '8080' : process.env.BACKEND_PORT,
    // prefix: '/api',

    baseURL: development ? 'http://localhost:8080/api' : 'BASE_URL_STRING_TO_REPLACE',
  },

  // PWA module configuration: https://go.nuxtjs.dev/pwa
  pwa: {
    manifest: {
      lang: 'en',
    },
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},

  publicRuntimeConfig: {
    apiURL: development ? 'http://localhost:8080/swagger/index.html' : 'SWAGGER_URL_STRING_TO_REPLACE',
  }
}
