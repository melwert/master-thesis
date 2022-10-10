<template>
  <b-navbar class="mb-3">
    <template #brand>
      <b-navbar-item tag="router-link" :to="{ path: '/' }">
        <img
          src="https://raw.githubusercontent.com/buefy/buefy/dev/static/img/buefy-logo.png"
          alt="Lightweight UI components for Vue.js based on Bulma"
        >
      </b-navbar-item>
    </template>
    <template #start>
      <b-navbar-item v-for="(item, key) of items" :key="key" class="px-4">
        <nuxt-link :to="localePath({name: item.to})" exact-active-class="is-active" class="is-flex">
          <b-icon :icon="item.icon" class="m-0 pr-3"/> {{ item.title }}
        </nuxt-link>
      </b-navbar-item>
      <!-- TODO make configurable -->
      <b-navbar-item href="http://localhost:8080/swagger/index.html" target="_blank" class="is-flex">
        <b-icon icon="api" class="m-0 pr-3"/> {{ $t('apiExplorer')}}
      </b-navbar-item>
    </template>

    <template #end>
      <b-navbar-item tag="div">
        <b-field>
          <p v-for="locale in availableLocales" class="control">
            <a href="#" @click.prevent.stop="$i18n.setLocale(locale.code)" class="button is-light px-0">
              <country-flag :country="locale.flagkey" size="normal" shadow class="m-0"/>
            </a>
          </p>
        </b-field>
      </b-navbar-item>
    </template>
  </b-navbar>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {
      items: [
        {
          title: 'Projects',
          icon: 'home',
          to: 'index',
        },
        {
          title: 'Persons',
          icon: 'information',
          to: 'persons',
        },
      ],
    }
  },
  computed: {
    availableLocales () {
      return this.$i18n.locales.filter(i => i.code !== this.$i18n.locale)
  },
}
}
</script>