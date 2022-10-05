<template>
  <table class="table">
    <thead>
      <tr>
        <th>Vessel</th>
        <th>Received Time</th>
        <th>Latitude</th>
        <th>Longitude</th>
      </tr>
    </thead>
    <tfoot>
      <tr>
        <th>Vessel</th>
        <th>Received Time</th>
        <th>Latitude</th>
        <th>Longitude</th>
      </tr>
    </tfoot>
    <tbody v-if="rows">
      <tr v-for="row in rows" v-bind:key="row.vessel_id">
        <th>{{ row.vessel_id }}</th>
        <td>{{ row.received_time_utc }}</td>
        <td>{{ row.latitude }}</td>
        <td>{{ row.longitude }}</td>
      </tr>
    </tbody>
  </table>
</template>
<script lang="ts">
import { defineComponent, PropType } from 'vue'
import { CsvRow } from '@/utils/types'
export default defineComponent({
  name: 'JourneyTable',
  props: {
    rows: {
      type: Array as PropType<Array<CsvRow>>
    }
  }
})
</script>