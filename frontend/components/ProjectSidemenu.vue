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
              <p class="heading">{{$t('project')}}</p>
              <p class="title">{{currentProject}}</p>
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
        <b-menu-list label="Heatmaps">
          <b-menu-item 
            tag="nuxt-link" 
            :to="localePath({ name: 'project-id-commitHeatmap', params: { id: currentProjectId, commitHeatmap: 'commitHeatmap'}})" 
            icon="source-commit" 
            :label="$t('commitChanges')"
            exact-active-class="is-active">
          </b-menu-item>
          <b-menu-item 
            tag="nuxt-link"
            :to="localePath({ name: 'project-id-commitMessageLengthHeatmap', params: { id: currentProjectId, commitMessageLengthHeatmap: 'commitMessageLengthHeatmap'}})"
            icon="arrow-split-vertical" 
            :label="$t('commitMessageLengths')"
            exact-active-class="is-active">
          </b-menu-item>
        </b-menu-list>
        <b-menu-list label="Boxplots">
          <b-menu-item 
            tag="nuxt-link" 
            :to="localePath({ name: 'project-id-commitMessageLengthAreaBoxplot', params: { id: currentProjectId, commitMessageLengthAreaBoxplot: 'commitMessageLengthAreaBoxplot'}})" 
            icon="source-commit" 
            :label="$t('commitMessageArea')"
            exact-active-class="is-active">
          </b-menu-item>
          <b-menu-item 
            tag="nuxt-link" 
            :to="localePath({ name: 'project-id-commitMessageLengthDevBoxplot', params: { id: currentProjectId, commitMessageLengthDevBoxplot: 'commitMessageLengthDevBoxplot'}})" 
            icon="source-commit" 
            :label="$t('commitMessageDev')"
            exact-active-class="is-active">
          </b-menu-item>
        </b-menu-list>
        <b-menu-list label="Barcharts">
          <b-menu-item 
            tag="nuxt-link" 
            :to="localePath({ name: 'project-id-fileChangesAreaBarchart', params: { id: currentProjectId, fileChangesAreaBoxplot: 'fileChangesAreaBoxplot'}})" 
            icon="file-edit-outline" 
            :label="$t('fileChangesArea')"
            exact-active-class="is-active">
          </b-menu-item>
          <b-menu-item 
            tag="nuxt-link" 
            :to="localePath({ name: 'project-id-fileChangesDevBarchart', params: { id: currentProjectId, fileChangesDevBoxplot: 'fileChangesDevBoxplot'}})" 
            icon="file-edit-outline" 
            :label="$t('fileChangesDev')"
            exact-active-class="is-active">
          </b-menu-item>
          <b-menu-item 
            tag="nuxt-link" 
            :to="localePath({ name: 'project-id-commitHoursBarchart', params: { id: currentProjectId, commitHoursBarchart: 'commitHoursBarchart'}})" 
            icon="source-commit" 
            :label="$t('commitHoursBarchart')"
            exact-active-class="is-active">
          </b-menu-item>
          <b-menu-item 
            tag="nuxt-link" 
            :to="localePath({ name: 'project-id-commitWeekdaysBarchart', params: { id: currentProjectId, commitWeekdaysBarchart: 'commitWeekdaysBarchart'}})" 
            icon="source-commit" 
            :label="$t('commitWeekdaysBarchart')"
            exact-active-class="is-active">
          </b-menu-item>
        </b-menu-list>
        <b-menu-list label="Piecharts">
          <b-menu-item 
            tag="nuxt-link" 
            :to="localePath({ name: 'project-id-fileCountAreaPiechart', params: { id: currentProjectId, fileCountAreaPiechart: 'fileCountAreaPiechart'}})" 
            icon="file-multiple" 
            :label="$t('fileCountAreaPiechart')"
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
    currentProject: {
      type: String,
      required: true,
    },
    currentProjectId: {
      type: String,
      required: true,
    },
  },
  computed: {
    overviewLink() {
      return `/project/${this.currentProjectId}/overview`
    },
    commitHeatmapLink() {
      return `/project/${this.currentProjectId}/commitHeatmap`
    }
  }
};
</script>
