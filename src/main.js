import Vue from 'vue'

import App from '@/App.vue'

import store from '@/store'
import router from '@/router'

Vue.config.productionTip = false

// Vue.use(VueRouter)

import '@/assets/style.css'
import '@/assets/fontawesome/fontawesome.css'
import '@/assets/fontawesome/solid.css'

const vue = new Vue({
    router,
    store,
    render: h => h(App)
})

if (/(android|webos|iphone|ipad|ipod|blackberry|windows phone|tablet|ipad)/.test(navigator.userAgent.toLowerCase())) {
    document.body.classList.add('mobile')
} else {
    document.body.classList.add('desktop')
}

vue.$mount('#app')
