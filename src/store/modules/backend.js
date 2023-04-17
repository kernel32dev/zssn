import backend from '../../services/backend'

const state = {
    login: null,
    sobreviventes: [],
    relatos: [],
    itens: [],
}

const getters = {
    login: state => {
        return state.login
    },
    sobreviventes: state => {
        return state.sobreviventes
    },
    relatos: state => {
        return state.relatos
    },
    itens: state => {
        return state.itens
    },
}

const actions = {
    initialize({ commit }) {
        backend.fetchSobreviventes().then(result => {
            if (result.ok) commit('setSobreviventes', result.ok.sobreviventes)
        })
        backend.fetchRelatos().then(result => {
            if (result.ok) commit('setRelatos', result.ok.relatos)
        })
        backend.fetchItens().then(result => {
            if (result.ok) commit('setItens', result.ok.itens)
        })
    },
    login({ commit }, payload) {
        backend.login(payload).then(result => {
            if (result.ok) commit('setLogin', result.ok)
        })
    },
    logoff({ commit }) {
        backend.logoff().then(result => {
            if (result.ok) commit('setLogin', null)
        })
    },
    signup({ commit }, payload) {
        backend.signup(payload).then(result => {
            if (result.ok) commit('setLogin', result.ok)
        })
    },
    signout({ commit }) {
        backend.signout().then(result => {
            if (result.ok) commit('setLogin', null)
        })
    },
    fetchLogin({ commit }) {
        backend.fetchSobrevivente()
            .then(result => {
                if (result.ok) commit('setLogin', result.ok)
            })
    },
    postPosition({ commit }, latitude, longitude) {
        backend.postPosition(latitude, longitude)
            .then(result => {
                if (result.ok) commit('setPosition', latitude, longitude)
            })
    },
    postRelato({ commit }, relatado) {
        backend.postRelato(relatado)
            .then(result => {
                if (result.ok) commit('addRelato', relatado)
            })
    },
    deleteRelato({ commit }, relatado) {
        backend.deleteRelato(relatado)
            .then(result => {
                if (result.ok) commit('rmRelato', relatado)
            })
    },
}

const mutations = {
    setLogin(state, login) {
        state.login = login;
    },
    setSobreviventes(state, sobreviventes) {
        state.sobreviventes = sobreviventes;
    },
    setRelatos(state, relatos) {
        state.relatos = relatos;
    },
    setItens(state, itens) {
        state.itens = itens;
    },
    setPosition(state, position) {
        if (state.sobrevivente !== null) {
            state.sobrevivente.position = position;
        }
    },
    addRelato(state, relatado) {
        if (state.sobrevivente !== null) {
            let relator = state.sobrevivente.id;
            let index = state.relatos.findIndex(x => x[0] === relator && x[1] === relatado);
            if (index === -1) {
                state.relatos.push([relator, relatado]);
            }
        }
    },
    rmRelato(state, relatado) {
        if (state.sobrevivente !== null) {
            let relator = state.sobrevivente.id;
            let index = state.relatos.findIndex(x => x[0] === relator && x[1] === relatado);
            if (index !== -1) {
                state.relatos.splice(index, 1);
            }
        }
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}