<template>
  <div class="column">
    <div class="projectcard p-2">
        <div class="level m-0">
          <div class="level-item has-text-centered">
            <div>
              <p class="title">{{person.name}}</p>
            </div>
          </div>
          <div class="level-item has-text-centered">
            <div>
              <p class="heading">{{ $t('commits')}}</p>
              <p class="title is-4">{{person.commitCount}}</p>
            </div>
          </div>
          <div class="level-item has-text-centered">
            <div>
              <p class="heading">{{ $t('issues')}}</p>
              <p class="title is-4">{{person.issueCount}}</p>
            </div>
          </div>
          <div class="level-item has-text-centered">
            <div>
              <p class="heading">{{ $t('prs')}}</p>
              <p class="title is-4">{{person.prCount}}</p>
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
         </div>
      <div>
    </div>

    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { Person } from '~/models/person'

export default Vue.extend({
  name: 'PersonCard',
  data() {
    return {
      showDay: true
    }
  },
  props: {
    person: {
      type: Object as () => Person,
      required: true,
    },
  },
  computed: {
    daysSinceLastScan () {
      const dateNow = new Date()
      const lastScanDate = new Date(this.person.lastScanDate)

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
