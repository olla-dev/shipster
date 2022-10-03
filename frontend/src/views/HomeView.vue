<template>
  <div class="content">
    <div class="map" id="map"></div>
  </div>
</template>

<script lang="ts">
  import mapboxgl from 'mapbox-gl'
  import { defineComponent } from 'vue';

  export default defineComponent({
    name: 'HomeView',
    components: {
    },
    data() {
      return {
        accessToken: process.env.VUE_APP_MAP_ACCESS_TOKEN,
        mapStyle: process.env.VUE_APP_MAP_ACCESS_STYLE,
        center: [11.030, 37.915],
        zoom: 3,
        map: {},
      }
    },
    mounted() {
      this.createMap()
    },
    methods: {
      async createMap() {
        try {
          mapboxgl.accessToken = this.accessToken;
          this.map = new mapboxgl.Map({
            container: "map",
            style: this.mapStyle,
            center: [11.030, 37.915],
            zoom: this.zoom,
          });

        } catch (err) {
          console.log("map error", err);
        }
      },
    },
  })
</script>
<style>
    #map {
      width: 100%;
      height: calc(100vh - 80px);
    }
</style>
