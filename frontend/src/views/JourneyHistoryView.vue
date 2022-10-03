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
                    <JourneyTable />
                </div>
            </div>
            <footer class="footer">
                <div class="content has-text-centered">
                    <nav class="pagination" role="navigation" aria-label="pagination">
                    <a class="pagination-previous">Previous</a>
                    <a class="pagination-next">Next page</a>
                    <ul class="pagination-list">
                        <li>
                        <a class="pagination-link" aria-label="Goto page 1">1</a>
                        </li>
                        <li>
                        <span class="pagination-ellipsis">&hellip;</span>
                        </li>
                        <li>
                        <a class="pagination-link" aria-label="Goto page 45">45</a>
                        </li>
                        <li>
                        <a class="pagination-link is-current" aria-label="Page 46" aria-current="page">46</a>
                        </li>
                        <li>
                        <a class="pagination-link" aria-label="Goto page 47">47</a>
                        </li>
                        <li>
                        <span class="pagination-ellipsis">&hellip;</span>
                        </li>
                        <li>
                        <a class="pagination-link" aria-label="Goto page 86">86</a>
                        </li>
                    </ul>
                    </nav>
                </div>
            </footer>
        </div>
    </div>
</template>

<script lang="ts">
    import JourneyTable from '../components/journeys/JourneyTable.vue'
    import { defineComponent } from 'vue';
    export default defineComponent({
        name: 'JourneyHistoryView',
        components: {
            JourneyTable
        },
    });
</script>