<template>
    <div class="container mt-5">
        <div class="card">
            <header class="card-header">
                <p class="card-header-title title">
                    Journeys
                </p>

                <p class="control has-icons-left">
                    <input class="input" type="text" placeholder="Search">
                    <span class="icon is-left">
                        <i class="fas fa-search" aria-hidden="true"></i>
                    </span>
                </p>
            </header>
            <div class="card-content">
                <div class="content">
                    <JourneyTable :rows="data.results" />
                </div>
            </div>
            <footer class="footer">
                <div class="content has-text-centered">
                    <PaginationPanel :links="data.links" />
                </div>
            </footer>
        </div>
    </div>
</template>

<script lang="ts">
import JourneyTable from '../components/journeys/JourneyTable.vue'
import { defineComponent } from 'vue';
import PaginationPanel from '@/components/journeys/PaginationPanel.vue';
import { CsvData } from '@/utils/types';
import csvModule from '@/store/csv';

export default defineComponent({
    name: 'JourneyHistoryView',
    components: {
        JourneyTable,
        PaginationPanel
    },
    data() {
        return {
            isLoading: false
        }
    },
    mounted() {
        this.isLoading = true
        csvModule.fetchCsv();
    },
    computed: {
        data(): CsvData {
            return csvModule.data
        }
    },
    watch: {
        rows: {
            handler(oldVal, newVal) {
                if (oldVal != newVal) {
                    this.isLoading = false;
                }
            },
            deep: true
        },
    }
});
</script>