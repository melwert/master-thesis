<template>
  <div class="sidebar-page">
    <navbar></navbar>

    <section class="sidebar-layout">
      <project-sidemenu :currentProject="currentProject" :currentProjectId="currentProjectId"></project-sidemenu>
      <div class="p-3 mx-4" style="width: 100%">
        <Nuxt />
      </div>
    </section>
  </div>


</template>

<script lang="ts">
import Vue from 'vue'
import Navbar from '~/components/Navbar.vue'
import ProjectSidemenu from '~/components/ProjectSidemenu.vue'

export default Vue.extend({
  name: 'DefaultLayout',
  data() {
    return {
    }
  },
  components: {
    Navbar,
    ProjectSidemenu,
  },
  computed: {
    currentProject() {
      const currentProject = this.$store.state.currentProject as string
      return currentProject
    },
    currentProjectId() {
      const currentProjectId = this.$store.state.currentProjectId as string
      return currentProjectId
    }
  },
})
</script>