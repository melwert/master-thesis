<template>
  <section v-if="dataLoaded"  class="section">
    <div v-for="(project, index) in projects" :key="index" class="columns is-mobile">
      <nuxt-link :to="localePath({ name: 'project-id-overview', params: { id: project.id }})" style="width: 100%;" append>
        <project-card :project="project"></project-card>
      </nuxt-link>
    </div>
  </section>
</template>

<script lang="ts">
import ProjectCard from '~/components/ProjectCard.vue'
import { Project } from '~/models/project'
import Vue from 'vue';

export default Vue.extend({
  name: 'IndexPage',
  components: {
    ProjectCard,
  },
  data() {
    const projects: Project[] = [];
    return {
      projects,
      dataLoaded: false
    }
  },
  async mounted() {
    const response = await this.$axios.get<Project[]>("projects")
     
    this.projects = response.data
    this.dataLoaded = true
  }
})
</script>
