<template>
<div>

    <NuxtChild :person="person" />
</div>
</template>

<script lang="ts">
import Vue from "vue";
import { Person } from "~/models/person";

export default Vue.extend({
    name: 'PersonPage',
    layout: 'person',
    data () {   
      return { 
        personId: "",
        person: {} as Person,
        dataLoaded: false
      }
    },
    asyncData({ params }) { 
        const personId  = params.id
        return {
          personId
        }
    },
    async mounted() {
      const response = await this.$axios.get<Person>(`/persons/${this.personId}`)
      this.person = response.data
      this.dataLoaded = true

      this.$store.commit('setCurrentPerson', this.person.name)
      this.$store.commit('setCurrentPersonId', this.person.id)
    }
})
</script>