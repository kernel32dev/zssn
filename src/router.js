import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home.vue'
import Comprar from '@/components/Comprar.vue'
import Vender from '@/components/Vender.vue'
import Relatos from '@/components/Relatos.vue'
import Relatorios from '@/components/Relatorios.vue'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            meta: { alias: 'Meu Perfil' },
            component: Home
        },
        {
            path: '/comprar',
            name: 'comprar',
            meta: { alias: 'Comprar' },
            component: Comprar
        },
        {
            path: '/vender',
            name: 'vender',
            meta: { alias: 'Vender' },
            component: Vender
        },
        {
            path: '/relatos',
            name: 'relatos',
            meta: { alias: 'Relatos' },
            component: Relatos
        },
        {
            path: '/relatorios',
            name: 'relatorios',
            meta: { alias: 'Relatórios' },
            component: Relatorios
        }
    ]
})
