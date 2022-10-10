<template>
  <div class="mt-4">
    <h1 class="has-text-weight-bold">{{$t('fileCountAreaPiechartTitle')}}</h1>
    <apexchart type="pie" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'FileCountAreaPiechartPage',
  layout: 'project',
  data() {
    return {
      projectId: "",
      dataLoaded: false,
      chartOptions: {
        labels: {}
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
    const response = await this.$axios.get(`/fileCountAreaPiecharts/${this.projectId}`)
    const piechartDataSet = response.data
    this.series = piechartDataSet.series

    this.chartOptions = {
      labels: piechartDataSet.labels
    }
    
    window.dispatchEvent(new Event('resize'))
    this.dataLoaded = true
  }
})
</script>
