import Vue from 'vue'
import Vuex from 'vuex'
import backend from './modules/backend.js'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        backend
    }
})