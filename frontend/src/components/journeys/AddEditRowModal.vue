<template>
    <div class="modal">
        <div class="modal-background"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title">{{ mode === 'create' ? 'Add Location' : 'Edit Location'}}</p>
                <button class="delete" @click="close()"></button>
            </header>
            <section class="modal-card-body">
                <div class="field">
                    <label class="label is-medium">Vessel ID</label>
                    <div class="control has-icons-left has-icons-right">
                        <input class="input is-medium" :readonly="mode !== 'create'" v-model="local.vessel_id"
                            type="number" placeholder="Vessel ID">
                        <span class="icon is-small is-left">
                            <i class="fa fa-ship fa-xs"></i>
                        </span>
                    </div>
                </div>
                <div class="field">
                    <label class="label is-medium">Latitude</label>
                    <div class="control has-icons-left has-icons-right">
                        <input class="input is-medium" v-model="local.latitude" type="text" placeholder="Latitude">
                        <span class="icon is-small is-left">
                            <i class="fas fa-globe fa-xs"></i>
                        </span>
                    </div>
                </div>
                <div class="field">
                    <label class="label is-medium">Longitude</label>
                    <div class="control has-icons-left has-icons-right">
                        <input class="input is-medium" v-model="local.longitude" type="decimal" placeholder="Longitude">
                        <span class="icon is-small is-left">
                            <i class="fas fa-globe fa-xs"></i>
                        </span>
                    </div>
                </div>
            </section>
            <footer class="modal-card-foot">
                <button class="button is-sucess" @click="saveLocation">Save</button>
                <button class="button" @click="close()">Cancel</button>
            </footer>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { CsvRow, CsvRowGeo } from '@/utils/types';
import csvModule from '@/store/csv';

export default defineComponent({
    name: 'AddEditRowModal',
    props: {
        mode: {
            type: String
        },
        selectedRow: {
            type: Object
        }
    },
    data() {
        return {
            vesselId: -1,
            latitude: 0.0,
            longitude: 0.0
        }
    },
    computed: {
        local: {
            get() { return csvModule.selectedRow; },
            set(newVal: CsvRow) {
                this.vesselId = newVal.vessel_id;
                this.latitude = newVal.latitude;
                this.longitude = newVal.longitude;
            },
        },
    },
    methods: {
        close() {
            this.$emit('close');
        },
        saveLocation() {
            const row: CsvRowGeo = {
                "location_id": this.local.location_id,
                "vessel_id": this.local.vessel_id,
                "received_time_utc": new Date().toISOString().split('.')[0] + "Z",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        this.local.latitude,
                        this.local.longitude
                    ]
                }
            }
            this.$emit('saveRow', row);
        }
    },
});
</script>
  
  