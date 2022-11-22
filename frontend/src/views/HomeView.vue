<template>
  <div class="content">
    <div class="map" id="map"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import vesselModule from '@/store/vessels';
import { Vessel } from '@/utils/types';
import mapboxgl, { AnyLayer, FullscreenControl, Layer, Map, Marker, Popup } from 'mapbox-gl';
import { Feature, Point } from 'geojson';
import { numberLiteralTypeAnnotation } from '@babel/types';


export default defineComponent({
  name: "HomeView",
  data() {
    return {
      accessToken: process.env.VUE_APP_MAP_ACCESS_TOKEN,
      mapStyle: process.env.VUE_APP_MAP_STYLE,
      center: [11.03, 37.915],
      zoom: 3,
      map: {} as Map,
      isLoading: false,
      markers: [{}] as [{ id: number, marker: mapboxgl.Marker }],
      websocketConnection: new WebSocket(process.env.VUE_APP_WEBSOCKET_URL)
    }
  },
  mounted() {
    this.isLoading = true
    vesselModule.fetchVessels();
    this.createMap();
  },
  created: function () {
    const markers = this.markers;
    const map = this.map;
    console.log("Starting connection to WebSocket Server")
    this.websocketConnection.onmessage = function (event: MessageEvent) {
      console.log('Update vessel location.');
      const eventJson = JSON.parse(event.data);
      const marker = markers.find(m => m.id === eventJson.properties.vessel_id)
      if (marker !== undefined) {
        marker.marker.setLngLat(eventJson.geometry.coordinates)
      }
    }

    this.websocketConnection.onopen = function (event: Event) {
      console.log(event)
      console.log("Successfully connected to the vessel websocket server...")
    }
  },
  computed: {
    // need annotation
    vessels(): Vessel[] {
      return vesselModule.vessels
    },
    selectedVessel(): Vessel | undefined {
      return vesselModule.getSelectedVessel
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
      el.id = location.properties!['vessel_id'];
      el.className = "marker";

      // important : attach click listener on marker
      el.addEventListener('click', () => {
        const id = `${this.selectedVessel?.vessel_id}`;

        if (id !== `${location.properties!['vessel_id']}`) {
          // clear selected vessel display from map
          if (this.map.getLayer(id)) {
            this.map.removeLayer(id);
          }
          if (this.map.getSource(id)) {
            this.map.removeSource(id);
          }
        }

        vesselModule.setSelectedVessel(location.properties!['vessel_id']);
      });

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
      this.markers.push({ id: location.properties!['vessel_id'], marker: m });
    },
    loadJourney() {
      console.log('selected vessel:', this.selectedVessel?.vessel_id);

      const id = `${this.selectedVessel?.vessel_id}`;
      // display vessel journey on the map
      this.map.addLayer({
        'id': id,
        'type': 'line',
        'source': {
          'type': 'geojson',
          'data': this.selectedVessel?.journey
        },
        'layout': {
          'line-join': 'round',
          'line-cap': 'round'
        },
        'paint': {
          'line-color': '#ff0000',
          'line-width': 3
        }
      });
    }
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
    },
    selectedVessel: {
      handler(oldVal, newVal) {
        if (oldVal != newVal) {
          this.isLoading = false;
          this.loadJourney();
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
  max-width: 300px;
}
</style>