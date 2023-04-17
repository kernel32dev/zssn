<template>
    <div id="app">
        <Login v-if="login === null"/>
        <Router v-if="login !== null"/>
    </div>
</template>

<script>
import { mapState } from 'vuex'
import Login from './components/Login.vue'
import Router from './components/Router.vue'
export default {
    name: 'App',
    created() {
        this.$store.dispatch('backend/initialize')
        this.$store.dispatch('backend/fetchLogin')
    },
    computed: mapState({
        login: state => state.backend.login
    }),
    components: {
        Router, Login
    }
}
</script>
