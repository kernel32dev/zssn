import api from '@/services/api.js'

export default {
    // autenticação
    login(payload) {
        return api.post(`login/`, payload)
    },
    logoff() {
        return api.post(`logoff/`)
    },
    signup(payload) {
        return api.post(`signup/`, payload)
    },
    signout() {
        return api.post(`signout/`)
    },

    // api privadas
    fetchSobrevivente() {
        return api.get(`sobrevivente/`)
    },
    postPosicao(latitude, longitude) {
        return api.post(`posicao/`, `{"latitude":${latitude},"longitude":${longitude}}`)
    },
    postRelato(relatado) {
        return api.post(`relato/${relatado}/`)
    },
    deleteRelato(relatado) {
        return api.post(`relato/${relatado}/`)
    },

    // api publicas
    fetchSobreviventes() {
        return api.get(`sobreviventes/`)
    },
    fetchItens() {
        return api.get(`itens/`)
    },
    fetchRelatos() {
        return api.get(`relatos/`)
    },
}