<template>
    <article class="panel is-success mt-5">
        <p class="panel-tabs">
            <a 
                @click="setVisibleTab(0)"
                :class="visibleTab === 0 ? 'is-active' : ''">
                Backend
            </a>
            <a 
                @click="setVisibleTab(1)"
                :class="visibleTab === 1 ? 'is-active' : ''">
                Frontend
            </a>
            <a 
                @click="setVisibleTab(2)"
                :class="visibleTab === 2 ? 'is-active' : ''">
                DevOps
            </a>
            <a 
                @click="setVisibleTab(3)"
                :class="visibleTab === 3 ? 'is-active' : ''">
                Other
            </a>
        </p>
        <div 
            v-if="visibleTab === 0"
            class="panel-block has-text-left"
            :class="visibleTab === 0 ? 'is-active' : ''">
            <ul>
                <li>Database: PostGreSQL using PostGIS</li>
                <li>Caching: Redis with django-redis (view caching) and django-cachalot (queryset caching)</li>
                <li>Django</li>
                <li>Django Rest Framework</li>
                <li>Django Channels</li>
            </ul>
        </div>
        <div 
            v-if="visibleTab === 1"
            @click="setVisibleTab(1)"
            class="panel-block has-text-left"
            :class="visibleTab === 1 ? 'is-active' : ''">
            <ul>
                <li>Vue 3 using typescript</li>
                <li>Bulma</li>
                <li>MapboxGL</li>
                <li>Vue Router</li>
                <li>Vuex</li>
                <li>Axios</li>
            </ul>
        </div>
        <div
            v-if="visibleTab === 2"
            @click="setVisibleTab(2)"
            class="panel-block has-text-left"
            :class="visibleTab === 2 ? 'is-active' : ''">
            <ul>
                <li>Docker</li>
            </ul>
        </div>
        <div
            v-if="visibleTab === 3"
            @click="setVisibleTab(3)"
            class="panel-block has-text-left"
            :class="visibleTab === 3 ? 'is-active' : ''">
            <ul>
                <li>A lot of 🍕 and energy drinks</li>
            </ul>
        </div>
    </article>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
    name: 'TechStack',
    data() {
        return {
           visibleTab: 0
        }
    },
    methods: {
        setVisibleTab(tabIndex=0) {
            this.visibleTab = tabIndex
        }
    }
})
</script>