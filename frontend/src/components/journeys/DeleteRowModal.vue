<template>
    <div class="modal">
        <div class="modal-background"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title">Delete</p>
                <button class="delete" @click="close()"></button>
            </header>
            <section class="modal-card-body">
                Are you sure you want to delete this location ?
            </section>
            <footer class="modal-card-foot">
                <button class="button is-danger" @click="deleteLocation()">Delete</button>
                <button class="button" @click="close()">Cancel</button>
            </footer>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
    name: 'DeleteRowModal',
    props: {
        row: {
            type: Object
        }
    },
    methods: {
        close() {
            this.$emit('close');
        },
        deleteLocation() {
            this.$emit('deleteRow');
        },
    },
});
</script>
  
  