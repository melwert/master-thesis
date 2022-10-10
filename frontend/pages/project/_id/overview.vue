<template>
  <div>
    <!-- Overview-Component: {{ project.id }} -->

    <template>
      <b-table :data="data" :columns="columns"></b-table>
    </template>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { GeneralStatistic } from '~/models/generalStatistic'
import { Project } from '~/models/project'

export default Vue.extend({
  name: 'ProjectOverviewPage',
  props: {
    project: {
      type: Object as () => Project,
      required: true,
    },
  },
  data() {
    return {
      projectId: "",
      dataLoaded: false,
      data: [
        { 'property': '', 'value': '', },
      ],
      columns: [
        {
          field: 'property',
          label: this.$t('property').toString(),
          width: '400'
        },
        {
          field: 'value',
          label: this.$t('value').toString(),
        },
      ]
    }
  },
  asyncData({ params }) {
    const projectId = params.id
    return {
      projectId
    }
  },
  async mounted() {
      const response = await this.$axios.get<GeneralStatistic>(`/generalStatistics/${this.projectId}`)
      const generalStatistic = response.data
      this.data = [
        { 'property': this.$t('commitCount').toString(), 'value': generalStatistic.commitCount.toString(), },
        { 'property': this.$t('developerCount').toString(), 'value': generalStatistic.developerCount.toString(), },
        { 'property': this.$t('fileCount').toString(), 'value': generalStatistic.fileCount.toString(), },
        { 'property': this.$t('repoLink').toString(), 'value': generalStatistic.repositoryLink, },
        { 'property': this.$t('bibuCommentCount').toString(), 'value': generalStatistic.bitbucketCommentCount.toString(), },
        { 'property': this.$t('bibuPrCount').toString(), 'value': generalStatistic.bitbucketPrCount.toString(), },
        { 'property': this.$t('branchCount').toString(), 'value': generalStatistic.branchCount.toString(),  },
        { 'property': this.$t('jiraIssueCount').toString(), 'value': generalStatistic.jiraIssueCount.toString(),  },
        { 'property': this.$t('usedLanguages').toString(), 'value': generalStatistic.fileEndings.toString(),  },
      ]

      this.dataLoaded = true
    }
})
</script>
