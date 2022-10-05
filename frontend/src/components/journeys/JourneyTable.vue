<template>
  <table class="table">
    <thead>
      <tr>
        <th>Id</th>
        <th>Vessel</th>
        <th>Received Time</th>
        <th>Latitude</th>
        <th>Longitude</th>
        <th style="width: 300px;"></th>
      </tr>
    </thead>
    <tfoot>
      <tr>
        <th>Id</th>
        <th>Vessel</th>
        <th>Received Time</th>
        <th>Latitude</th>
        <th>Longitude</th>
        <th></th>
      </tr>
    </tfoot>
    <tbody v-if="rows">
      <tr v-for="row in rows" v-bind:key="row.location_id">
        <th>{{ row.location_id }}</th>
        <th>{{ row.vessel_id }}</th>
        <td>{{ row.received_time_utc }}</td>
        <td>{{ row.latitude }}</td>
        <td>{{ row.longitude }}</td>
        <td>
          <div class="buttons  are-small">
            <button class="button is-secondary" @click="editRow(row)">
              <span class="icon is-small">
                <i class="fas fa-align-left"></i>
              </span>
              <span>Edit</span>
            </button>
            <button class="button is-danger" @click="deleteRow(row)">
              <span class="icon is-small">
                <i class="fas fa-align-left"></i>
              </span>
              <span>Delete</span>
            </button>
          </div>
        </td>
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
  },
  methods: {
    editRow(row: CsvRow) {
      this.$emit('editRow', row)
    },
    deleteRow(row: CsvRow) {
      this.$emit('deleteRow', row)
    }
  }
})
</script>