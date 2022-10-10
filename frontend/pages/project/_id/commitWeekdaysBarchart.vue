<template>
  <div class="mt-4">
    <h1 class="has-text-weight-bold">{{$t('commitWeekdaysBarchartTitle')}}</h1>
    <apexchart type="bar" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'FileChangesDevBoxPlotPage',
  layout: 'project',
  data() {
    return {
      projectId: "",
      dataLoaded: false,
      chartOptions: {
        chart: {
        },
        xaxis:{
          categories: [
            this.$i18n.t("monday"), 
            this.$i18n.t("tuesday"), 
            this.$i18n.t("wednesday"), 
            this.$i18n.t("thursday"), 
            this.$i18n.t("friday"), 
            this.$i18n.t("saturday"), 
            this.$i18n.t("sunday")
          ]
        }
      },
      series: [],
    }
  },
  asyncData({ params }) {
    const projectId = params.id
    return {
      projectId
    }
  },
  async mounted() {
    const response = await this.$axios.get(`/commitWeekdayBarcharts/${this.projectId}`)
    const boxplot = response.data
    this.series = boxplot.series
    
    window.dispatchEvent(new Event('resize'))
    this.dataLoaded = true
  }
})
</script>
