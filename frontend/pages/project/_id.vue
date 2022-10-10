<template>
<div>
    <!-- projectId aus der URL ausgelesen (_id.vue): {{projectId}} -->
    <!-- <hr> -->

    <NuxtChild :project="project" />
</div>
</template>

<script lang="ts">
import Vue from "vue";
import { Project } from "~/models/project";

export default Vue.extend({
    name: 'ProjectPage',
    layout: 'project',
    data () {
      return { 
        projectId: "",
        project: {} as Project,
        dataLoaded: false
      }
    },
    asyncData({ params }) { 
        const projectId  = params.id
        return {
          projectId
        }
    },
    async mounted() {
      const response = await this.$axios.get<Project>(`/projects/${this.projectId}`)
      this.project = response.data
      this.dataLoaded = true

      this.$store.commit('setCurrentProject', this.project.name)
      this.$store.commit('setCurrentProjectId', this.project.id)
    }
})
</script>