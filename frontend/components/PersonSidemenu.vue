<template>
  <b-sidebar
    position="static"
    :mobile="mobile"
    :expand-on-hover="expandOnHover"
    :reduce="reduce"
    :delay="expandWithDelay ? 500 : null"
    type="is-light"
    open
    class="sidemenu-shadow m-4 mt-5"
  >
    <div class="p-3">
      <div class="block mb-5">
         <div class="level-item has-text-centered pt-2">
            <div>
              <p class="heading">{{$t('person')}}</p>
              <p class="title">{{currentPerson}}</p>
            </div>
          </div>
      </div>
      <hr class="sidemenu-ruler my-1">
      <b-menu class="is-custom-mobile">
        <b-menu-list>
          <b-menu-item 
            tag="nuxt-link" 
            :to="localePath(overviewLink)" 
            icon="information-outline" 
            :label="$t('overview')"
            exact-active-class="is-active">
          </b-menu-item>
        </b-menu-list>
        <b-menu-list label="Barcharts">
          <b-menu-item 
            tag="nuxt-link" 
            :to="localePath({ name: 'person-id-commitHoursBarchart', params: { id: currentPersonId, commitHoursBarchart: 'commitHoursBarchart'}})" 
            icon="file-edit-outline" 
            :label="$t('commitHoursBarchart')"
            exact-active-class="is-active">
          </b-menu-item>
          <b-menu-item 
            tag="nuxt-link" 
            :to="localePath({ name: 'person-id-commitWeekdaysBarchart', params: { id: currentPersonId, commitWeekdaysBarchart: 'commitWeekdaysBarchart'}})" 
            icon="file-edit-outline" 
            :label="$t('commitWeekdaysBarchart')"
            exact-active-class="is-active">
          </b-menu-item>
        </b-menu-list>
      </b-menu>
    </div>
  </b-sidebar>
</template>

<script>
export default {
  data() {
    return {
      expandOnHover: false,
      expandWithDelay: false,
      mobile: "reduce",
      reduce: false
    };
  },
  props: {
    currentPerson: {
      type: String,
      required: true,
    },
    currentPersonId: {
      type: String,
      required: true,
    },
  },
  computed: {
    overviewLink() {
      return `/person/${this.currentPersonId}/overview`
    },
  }
};
</script>
