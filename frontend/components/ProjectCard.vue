<template>
  <div class="column">
    <div class="projectcard p-2">
        <div class="level m-0">
          <div class="level-item has-text-centered">
            <div>
              <p class="title">{{project.name}}</p>
            </div>
          </div>
          <div class="level-item has-text-centered">
            <div>
              <p class="heading">{{ $t('developers')}}</p>
              <p class="title is-4">{{project.developerCount}}</p>
            </div>
          </div>
          <div class="level-item has-text-centered">
            <div>
              <p class="heading">{{ $t('commits')}}</p>
              <p class="title is-4">{{project.commitCount}}</p>
            </div>
          </div>
          <div class="level-item has-text-centered">
            <div>
              <p class="heading">{{ $t('files')}}</p>
              <p class="title is-4">{{project.fileCount}}</p>
            </div>
          </div>
          <div class="level-item has-text-centered">
            <div>
              <p class="heading">{{ $t('lastScan')}}</p>
              <!-- Getting the translation in the days script did not work -->
              <p v-if="showDay" class="title is-4">{{$t('dayAgoPrefix')}} {{daysSinceLastScan}} {{$t('dayAgoSuffix')}}</p>
              <p v-else class="title is-4">{{$t('daysAgoPrefix')}} {{daysSinceLastScan}} {{$t('daysAgoSuffix')}}</p>
            </div>
          </div>
          <div class="level-item has-text-centered">
            <div>
              <vcs-icon-link :vcsUri="project.url"></vcs-icon-link>
            </div>
          </div>
         </div>
      <div>
    </div>

    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { Project } from '~/models/project'

export default Vue.extend({
  name: 'ProjectCard',
  data() {
    return {
      showDay: true
    }
  },
  props: {
    project: {
      type: Object as () => Project,
      required: true,
    },
  },
  computed: {
    daysSinceLastScan () {
      const dateNow = new Date()
      const lastScanDate = new Date(this.project.lastScanDate)

      const timeSinceLastScan = Math.abs(dateNow.getTime() - lastScanDate.getTime());
      const daysSinceLastScan = Math.ceil(timeSinceLastScan / (1000 * 3600 * 24));

      if (daysSinceLastScan == 1) {
        this.showDay = true
      } else {
        this.showDay = false
      }

      return daysSinceLastScan
    },
  },
})
</script>
