<template>
  <div class="content">
    <div class="map" id="map"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import vesselModule from '@/store/vessels';
import { Vessel } from '@/utils/types';
import mapboxgl, { FullscreenControl, Map, Marker, Popup } from 'mapbox-gl';
import { Feature, Point } from 'geojson';


export default defineComponent({
  name: "HomeView",
  data() {
    return {
      accessToken: process.env.VUE_APP_MAP_ACCESS_TOKEN,
      mapStyle: process.env.VUE_APP_MAP_STYLE,
      center: [11.03, 37.915],
      zoom: 3,
      map: {} as Map,
      isLoading: false
    }
  },
  mounted() {
    this.isLoading = true
    vesselModule.fetchVessels();
    this.createMap();
  },
  computed: {
    // need annotation
    vessels(): Vessel[] {
      return vesselModule.vessels
    }
  },
  methods: {
    async createMap() {
      try {
        mapboxgl.accessToken = this.accessToken;
        this.map = new Map({
          container: "map",
          style: this.mapStyle,
          center: [11.03, 37.915],
          zoom: this.zoom,
        });
        this.map.addControl(new FullscreenControl());
      }
      catch (err) {
        console.log("map error", err);
      }
    },
    fillMap() {
      for (var v of this.vessels!) {
        this.addMarker(v.latest_location)
      }
    },
    addMarker(location: Feature<Point>) {
      // create a HTML element for the marker
      const el = document.createElement("div");
      el.className = "marker";

      // add a popup to the marker
      const popup = new Popup({ offset: 25 })
        .setText(
          `Vessel: ${location.properties!['vessel_id']}\n (Last update: ${location.properties!['received_time_utc']})`
        );

      const m = new Marker(el)
        .setLngLat([
          location.geometry.coordinates[0],
          location.geometry.coordinates[1]
        ])
        .setPopup(popup)
        .addTo(this.map);
    },
  },

  watch: {
    vessels: {
      handler(oldVal, newVal) {
        if (oldVal != newVal) {
          this.isLoading = false;
          this.fillMap();
        }
      },
      deep: true
    }
  },
})
</script>


<style>
#map {
  width: 100%;
  height: calc(100vh - 80px);
}

.marker {
  background-image: url('@/assets/ship.png');
  background-size: cover;
  height: 48px;
  width: 48px;
  cursor: pointer;
}

.mapboxgl-popup {
  max-width: 200px;
}
</style>