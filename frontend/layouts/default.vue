<template>
  <div>
    <navbar></navbar>

    <section class="main-content columns">
      <div class="container column is-10">
        <Nuxt />
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import Navbar from '~/components/Navbar.vue'

export default {
  name: 'DefaultLayout',
  components: {
    Navbar,
  },
}
</script>
