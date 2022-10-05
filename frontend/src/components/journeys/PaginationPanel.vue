<template>
    <nav class="pagination" role="navigation" aria-label="pagination">
        <p>Page: {{currentPage}}</p>
        <a class="pagination-previous" @click="onClickPreviousPage">Previous</a>
        <a class="pagination-next" @click="onClickNextPage">Next page</a>
    </nav>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
    name: 'PaginationPanel',
    props: {
        links: {
            type: Object
        },
        currentPage: {
            type: Number
        }
    },
    methods: {
        onClickPreviousPage() {
            if (this.$props.currentPage! >= 2) {
                this.$emit('onClickPreviousPage');
            } else {
                alert('You are on the first page.');
            }
        },
        onClickNextPage() {
            this.$emit('onClickNextPage');
        },
    }
})
</script>