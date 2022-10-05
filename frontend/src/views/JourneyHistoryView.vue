<template>
    <div class="container mt-5">
        <div class="card">
            <header class="card-header">
                <p class="card-header-title title">
                    Locations
                    <Loading v-show="isLoading" />
                </p>

                <p class="control has-icons-left mt-5 mr-5">
                    <button class="button is-primary" @click="addRow">
                        <span>Add</span>
                    </button>
                </p>

                <p class="control has-icons-left mt-5 mr-5">
                    <input class="input" type="text" v-on:keyup.enter="applyFilter" v-model="searchFilter"
                        placeholder="Search">
                    <span class="icon is-left">
                        <i class="fas fa-search" aria-hidden="true"></i>
                    </span>
                </p>
            </header>
            <div class="card-content">
                <div class="content">
                    <JourneyTable :rows="data.results" @deleteRow="showDeleteRow" @editRow="showEditRow" />
                </div>
            </div>
            <footer class="footer">
                <div class="content has-text-centered">
                    <PaginationPanel :current-page="currentPage" :links="data.links"
                        @onClickPreviousPage="fetchPreviousPage" @onClickNextPage="fetchNextPage" />
                </div>
            </footer>
        </div>

        <DeleteRowModal v-show="deleteModalVisible" :class="{'is-active': deleteModalVisible}" :row="selectedRow"
            @close="closeModal" @deleteRow="deleteRow" />
        <AddEditRowModal v-show="addEditModalVisible" :row="selectedRow" :mode="mode"
            :class="{'is-active': addEditModalVisible}" @close="closeModal" @saveRow="saveRow" />
    </div>
</template>

<script lang="ts">
import JourneyTable from '../components/journeys/JourneyTable.vue'
import { defineComponent } from 'vue';
import PaginationPanel from '@/components/journeys/PaginationPanel.vue';
import { CsvData, CsvRow } from '@/utils/types';
import csvModule from '@/store/csv';
import DeleteRowModal from '../components/journeys/DeleteRowModal.vue';
import AddEditRowModal from '../components/journeys/AddEditRowModal.vue';
import Loading from '@/components/Loading.vue';

export default defineComponent({
    name: 'JourneyHistoryView',
    components: {
        JourneyTable,
        PaginationPanel,
        DeleteRowModal,
        AddEditRowModal,
        Loading
    },
    data() {
        return {
            isLoading: false,
            mode: 'edit', // edit or create mode
            deleteModalVisible: false,
            addEditModalVisible: false,
            selectedRow: {} as CsvRow,
            searchFilter: ''
        }
    },
    mounted() {
        this.isLoading = true
        csvModule.fetchCsv({ page: 1, filter: '' });
    },
    computed: {
        data(): CsvData {
            return csvModule.data
        },
        currentPage(): number {
            return csvModule.currentPage
        }
    },
    methods: {
        addRow() {
            this.mode = 'create'
            this.addEditModalVisible = true
            this.selectedRow = {} as CsvRow;
            csvModule.setSelectedRow(this.selectedRow);
        },
        showEditRow(row: CsvRow) {
            this.mode = 'edit'
            this.addEditModalVisible = true
            this.selectedRow = row;
            csvModule.setSelectedRow(this.selectedRow);
        },
        showDeleteRow(row: CsvRow) {
            this.selectedRow = row
            this.deleteModalVisible = true
            csvModule.setSelectedRow(this.selectedRow);
        },
        deleteRow() {
            this.isLoading = true;
            console.log(`delete location: ${this.selectedRow.location_id}`)
            csvModule.deleteLocation(this.selectedRow);
            this.closeModal();
            csvModule.fetchCsv({ page: this.currentPage, filter: '' });
            this.selectedRow = {} as CsvRow;
            csvModule.setSelectedRow(this.selectedRow);
        },
        saveRow(row: any) {
            this.isLoading = true;
            const update = this.mode === 'edit';

            console.log(`${this.mode} location: ${row.point.coordinates}`)
            if (update === true) {
                csvModule.updateLocation(row);
            } else {
                csvModule.saveLocation(row);
            }
            this.closeModal();
            csvModule.fetchCsv({ page: this.currentPage, filter: '' });
            this.selectedRow = {} as CsvRow;
        },
        closeModal() {
            this.deleteModalVisible = false
            this.addEditModalVisible = false
        },
        fetchNextPage() {
            this.isLoading = true;
            csvModule.fetchCsv({ page: this.currentPage + 1, filter: '' })
        },
        fetchPreviousPage() {
            this.isLoading = true;
            csvModule.fetchCsv({ page: this.currentPage - 1, filter: '' })
        },
        applyFilter() {
            if (this.searchFilter.length > 2) {
                this.isLoading = true;
                csvModule.fetchCsv({ page: 1, filter: this.searchFilter });
            }
            if (this.searchFilter === '') {
                csvModule.fetchCsv({ page: 1, filter: '' });

            }
        }
    },
    watch: {
        data: {
            handler(oldVal, newVal) {
                if (oldVal != newVal) {
                    this.isLoading = false;
                    this.$forceUpdate();
                }
            },
            deep: true
        },
        currentPage: {
            handler(oldVal, newVal) {
                if (oldVal != newVal) {
                    this.isLoading = false;
                    this.$forceUpdate();
                }
            },
            deep: false
        },
    }
});
</script>