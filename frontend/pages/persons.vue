<template>
  <section v-if="dataLoaded"  class="section">
    <div v-for="(person, index) in persons" :key="index" class="columns is-mobile">
      <nuxt-link :to="localePath({ name: 'person-id-overview', params: { id: person.id }})" style="width: 100%;" append>
        <person-card :person="person"></person-card>
      </nuxt-link>
    </div>
  </section>
</template>

<script lang="ts">
import PersonCard from '~/components/PersonCard.vue'
import Vue from 'vue';
import { Person } from '~/models/person';

export default Vue.extend({
  name: 'PersonsPage',
  components: {
    PersonCard,
  },
  data() {
    const persons: Person[] = [];
    return {
      persons,
      dataLoaded: false
    }
  },
  async mounted() {
    const response = await this.$axios.get<Person[]>("persons")
     
    this.persons = response.data
    this.dataLoaded = true
  }
})
</script>
