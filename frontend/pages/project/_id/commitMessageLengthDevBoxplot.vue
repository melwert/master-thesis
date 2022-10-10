<template>
  <div class="mt-4">
    <h1 class="has-text-weight-bold">{{$t('commitMessageLengthDevBoxplotTitle')}}</h1>
    <apexchart type="boxPlot" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'CommitMessageLengthDevBoxPlotPage',
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
    const response = await this.$axios.get(`/commitMessageLengthDeveloperBoxplots/${this.projectId}`)
    const boxplot = response.data
    this.series = boxplot.series

    window.dispatchEvent(new Event('resize'))
    this.dataLoaded = true
  }
})
</script>
