import { createApp } from 'vue'
import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'
import 'bulma/css/bulma.css'
import App from './App.vue'
import router from './router'
import store from './store'

import Notifications from '@kyvg/vue3-notification'

createApp(App)
    .use(store)
    .use(router)
    .use(Notifications)
    .mount('#app')
