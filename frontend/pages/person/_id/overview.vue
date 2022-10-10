<template>
  <div>
    <template>
      <b-table :data="data" :columns="columns"></b-table>
    </template>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { Person } from '~/models/person'

export default Vue.extend({
  name: 'PersonOverviewPage',
  props: {
    person: {
      type: Object as () => Person,
      required: true,
    },
  },
  data() {
    return {
      personId: "",
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
    const personId = params.id
    return {
      personId
    }
  },
  async mounted() {
      const response = await this.$axios.get<Person>(`/persons/${this.personId}`)
      const p = response.data

      this.data = [
        { 'property': this.$t('commitCount').toString(), 'value': p.commitCount.toString(), },
      ]

      this.dataLoaded = true
    }
})
</script>
