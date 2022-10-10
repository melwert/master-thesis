<template>
  <div class="sidebar-page">
    <navbar></navbar>

    <section class="sidebar-layout">
      <person-sidemenu :currentPerson="currentPerson" :currentPersonId="currentPersonId"></person-sidemenu>
      <div class="p-3 mx-4" style="width: 100%">
        <Nuxt />
      </div>
    </section>
  </div>


</template>

<script lang="ts">
import Vue from 'vue'
import Navbar from '~/components/Navbar.vue'
import PersonSidemenu from '~/components/PersonSidemenu.vue'

export default Vue.extend({
  name: 'DefaultLayout',
  data() {
    return {
    }
  },
  components: {
    Navbar,
    PersonSidemenu,
  },
  computed: {
    currentPerson() {
      const currentPerson = this.$store.state.currentPerson as string
      return currentPerson
    },
    currentPersonId() {
      const currentPersonId = this.$store.state.currentPersonId as string
      return currentPersonId
    }
  },
})
</script>