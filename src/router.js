import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home.vue'
import Sobreviventes from '@/components/Sobreviventes.vue'
import Inventario from '@/components/Inventario.vue'
import Escambo from '@/components/Escambo.vue'
import Relatos from '@/components/Relatos.vue'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/sobreviventes',
            name: 'sobreviventes',
            component: Sobreviventes
        },
        {
            path: '/inventario',
            name: 'inventario',
            component: Inventario
        },
        {
            path: '/escambo',
            name: 'escambo',
            component: Escambo
        },
        {
            path: '/relatos',
            name: 'relatos',
            component: Relatos
        }
    ]
})
