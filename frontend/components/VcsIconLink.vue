<template>
  <section>
    <p class="heading">{{ vcsName }}</p>
    <p class="control projectcard-vcs-link">
      <a :href="vcsUri" target="_blank" @click="onWrapperClick" class="button is-light is-flex" style="height: 27px">
        <b-icon :icon="vcsLinkIcon" size="is-small p-0"></b-icon>
      </a>
    </p>

  </section>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'IndexPage',
  props: {
    vcsUri: {
      type: String,
      required: true,
    },
  },
  computed: {
    vcsLinkIcon () {
      if (this.vcsUri.includes("github.com")) {
        return "github"
      } else if (this.vcsUri.includes("gitlab.com")) {
        return "gitlab"
      }
      else if (this.vcsUri.includes("git.int.melwert.de")) {
        return "tea"
      }
      else if (this.vcsUri.includes("bitbucket")) {
        return "bitbucket"
      }
    },
    vcsName () {
      if (this.vcsUri.includes("github.com")) {
        return "Github"
      } else if (this.vcsUri.includes("gitlab.com")) {
        return "Gitlab"
      }
      else if (this.vcsUri.includes("git.int.melwert.de")) {
        return "Gitea"
      }
      else if (this.vcsUri.includes("bitbucket")) {
        return "Bitbucket"
      }
    }
  },
  methods: {
    onWrapperClick(e: any) {
      console.log(e)

      if (e.target.tagName === 'I') {
        e.stopPropagation()
      }
    }
  }
})
</script>