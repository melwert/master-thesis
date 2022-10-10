<template>
  <div class="mt-4">
    <h1 class="has-text-weight-bold">{{$t('commitHoursBarchartTitle')}}</h1>
    <apexchart type="bar" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'CommitHoursPersonBarchart',
  layout: 'person',
  data() {
    return {
      personId: "",
      dataLoaded: false,
      chartOptions: {
        chart: {
        },
      },
      series: []
    }
  },
  asyncData({ params }) {
    const personId = params.id
    return {
      personId
    }
  },
  async mounted() {
    const response = await this.$axios.get(`/commitHourPersonBarcharts/${this.personId}`)
    const boxplot = response.data
    this.series = boxplot.series
    
    window.dispatchEvent(new Event('resize'))
    this.dataLoaded = true
  }
})
</script>
