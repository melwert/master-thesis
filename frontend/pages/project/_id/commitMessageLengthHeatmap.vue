<template>
  <div class="mt-4">
    <h1 class="has-text-weight-bold">{{$t('commitMessageLengthHeatmapTitle')}}</h1>
    <apexchart type="heatmap" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'CommitMessageLengthHeatmapPage',
  layout: 'project',
  data() {
    return {
      projectId: "",
      dataLoaded: false,
      chartOptions: {
        chart: {
        },
      },
      series: []
    }
  },
  asyncData({ params }) {
    const projectId = params.id
    return {
      projectId
    }
  },
  async mounted() {
    const response = await this.$axios.get(`/commitMessageLengthHeatmaps/${this.projectId}`)
    const commitMessageLengthHeatmap = response.data
    this.series = commitMessageLengthHeatmap.series

    this.dataLoaded = true
  }
})
</script>
