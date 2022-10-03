<template>
  <div class="content">
    <div class="map" id="map"></div>
  </div>
</template>

<script lang="ts">
  import mapboxgl from 'mapbox-gl';
  import { defineComponent } from 'vue';
  import vesselModule from '@/store/vessels';

  export default defineComponent({
    name: 'HomeView',
    data() {
      return {
        accessToken: process.env.VUE_APP_MAP_ACCESS_TOKEN,
        mapStyle: process.env.VUE_APP_MAP_STYLE,
        center: [11.030, 37.915],
        zoom: 3,
        map: {} as mapboxgl.Map,
      }
    },
    mounted() {
      vesselModule.fetchVessels()
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
          this.map.addControl(new mapboxgl.FullscreenControl());

          // create a HTML element for each feature
          const el = document.createElement('div');
          el.className = 'marker';

          // make a marker for each feature and add to the map
          new mapboxgl
            .Marker(el)
            .setLngLat([11.030, 37.915])
            .addTo(this.map);
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
    .marker {
      background-image: url('../assets/ship.png');
      background-size: cover;
      cursor: pointer;
    }

</style>
