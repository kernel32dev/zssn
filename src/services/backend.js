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
    postPosicao(payload) {
        return api.post(`posicao/`, payload)
    },
    postRelato(relatado) {
        return api.post(`relato/${relatado}/`)
    },
    deleteRelato(relatado) {
        return api.delete(`relato/${relatado}/`)
    },
    postOferta(oferta) {
        return api.post(`relato/`, oferta)
    },
    deleteOferta(oferta) {
        return api.delete(`relato/${oferta}/`)
    },
    postCompra(oferta) {
        return api.post(`compra/${oferta}/`)
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
    fetchOfertas() {
        return api.get(`ofertas/`)
    },
}