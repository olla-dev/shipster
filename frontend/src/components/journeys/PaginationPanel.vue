<template>
    <nav class="pagination" role="navigation" aria-label="pagination">
        <a class="pagination-previous" :disabled="currentPage === 1">Previous</a>
        <a class="pagination-next">Next page</a>
        <ul class="pagination-list">
            <li v-for="page in slidingWindow " :key="page">
                <a class="pagination-link" @click="onClickPage(page)">{{page}}</a>
            </li>
        </ul>
    </nav>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
    name: 'JourneyTable',
    data() {
        return {
            page: 1,
            slidingWindow: [...Array(10).keys()]
        }
    },
    props: {
        links: {
            type: Object
        },
        currentPage: {
            type: Number,
            default: 1
        }
    },
    methods: {
        onClickPage(p: number) {
            this.$emit('load-page', p);
            this.recalculateSlidingWindow(p)
        },
        onClickFirstPage() {
            this.$emit('load-page', 1);
            this.slidingWindow = [...Array(10)]
            this.page = this.slidingWindow[0];
        },
        onClickPreviousPage() {
            this.$emit('load-page', this.$props.currentPage - 1);
        },
        onClickNextPage() {
            this.$emit('load-page', this.$props.currentPage + 1);
        },
        recalculateSlidingWindow(p: number) {
            console.log(this.slidingWindow[9], p)
            if (this.slidingWindow[9] - p <= 3) {
                this.slidingWindow = [...Array.from({ length: (this.slidingWindow[9] + p, p - 3) }, (v, k) => k + (p - 3)).keys()]
                this.page = p;
            }
        },
    }
})
</script>