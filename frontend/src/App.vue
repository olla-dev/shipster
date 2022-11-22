<template>
  <NavHeader />
  <notifications />
  <router-view/>
</template>

<script lang="ts">
  import NavHeader from './components/NavHeader.vue'
  export default {
    name: 'App',
    components: {
      NavHeader
    }
  }
</script>