<template>
    <div class="is-small ml-2">
        <progress class="progress is-small is-primary" max="100">15%</progress>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'LoadingView'
});
</script>