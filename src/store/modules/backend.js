import backend from '../../services/backend'

const state = {
    login: 'loading',
    sobreviventes: [],
    relatos: [],
    itens: [],
    ofertas: [],
}

const getters = {
    login: state => {
        return state.login;
    },
    sobreviventes: state => {
        return state.sobreviventes;
    },
    relatos: state => {
        return state.relatos;
    },
    itens: state => {
        return state.itens;
    },
    ofertas: state => {
        return state.ofertas;
    },
}

const actions = {
    initialize({ commit }) {
        backend.fetchSobreviventes().then(result => {
            if (!result.err) commit('setSobreviventes', result.ok.sobreviventes);
        });
        backend.fetchRelatos().then(result => {
            if (!result.err) commit('setRelatos', result.ok.relatos);
        });
        backend.fetchItens().then(result => {
            if (!result.err) commit('setItens', result.ok.itens);
        });
        backend.fetchOfertas().then(result => {
            if (!result.err) commit('setOfertas', result.ok.ofertas);
        });
    },
    login({ commit }, payload) {
        backend.login(payload).then(result => {
            commit('setLogin', result.ok || null);
        });
    },
    logoff({ commit }) {
        backend.logoff().then(result => {
            if (!result.err) commit('setLogin', null);
        });
    },
    signup({ commit }, payload) {
        backend.signup(payload).then(result => {
            commit('setLogin', result.ok || null);
        });
    },
    signout({ commit }) {
        backend.signout().then(result => {
            if (!result.err) commit('setLogin', null);
        });
    },
    fetchLogin({ commit }) {
        commit('setLogin', 'loading');
        backend.fetchSobrevivente()
            .then(result => {
                commit('setLogin', result.ok || null);
            });
    },
    postPosicao({ commit }, payload) {
        backend.postPosicao(payload)
            .then(result => {
                if (!result.err) commit('setPosicao', payload);
            })
    },
    postRelato({ commit }, relatado) {
        backend.postRelato(relatado)
            .then(result => {
                if (!result.err) {
                    commit('addRelato', relatado);
                    commit('setInfectado', { relatado, infectado: result.ok.infectado });
                }
            })
    },
    deleteRelato({ commit }, relatado) {
        backend.deleteRelato(relatado)
            .then(result => {
                if (!result.err) commit('rmRelato', relatado)
            })
    },
    postOferta({ commit, state }, payload) {
        let vendedor = state.login.id;
        backend.postOferta(payload)
            .then(result => {
                if (!result.err) {
                    commit('addOferta', {
                        id: result.ok.id,
                        vendedor,
                        itens: payload.itens
                    });
                }
            })
    },
    deleteOferta({ commit }, oferta) {
        backend.deleteOferta(oferta)
            .then(result => {
                if (!result.err) commit('rmOferta', oferta)
            })
    },
    postCompra({ commit }, oferta) {
        backend.postCompra(oferta)
            .then(result => {
                if (!result.err) commit('postCompra', oferta)
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
    setOfertas(state, ofertas) {
        state.ofertas = ofertas;
    },
    setPosicao(state, position) {
        if (state.login !== null && state.login !== 'loading') {
            state.login.position = position;
        }
    },
    addRelato(state, relatado) {
        if (state.login !== null) {
            let relator = state.login.id;
            let index = state.relatos.findIndex(x => x[0] === relator && x[1] === relatado);
            if (index === -1) {
                state.relatos.push([relator, relatado]);
            }
        }
    },
    rmRelato(state, relatado) {
        if (state.login !== null) {
            let relator = state.login.id;
            let index = state.relatos.findIndex(x => x[0] === relator && x[1] === relatado);
            if (index !== -1) {
                state.relatos.splice(index, 1);
            }
        }
    },
    setInfectado(state, { relatado, infectado }) {
        for (let i = 0; i < state.sobreviventes.length; i++) {
            if (state.sobreviventes[i].id === relatado) {
                state.sobreviventes[i].infectado = infectado;
            }
            break;
        }
    },
    addOferta(state, oferta) {
        state.ofertas.push(oferta);
    },
    rmOferta(state, oferta) {
        let index = state.ofertas.findIndex(x => x.id === oferta);
        if (index !== -1) {
            state.ofertas.splice(index, 1);
        }
    },
    postCompra(state, oferta) {
        let index = state.ofertas.findIndex(x => x.id === oferta);
        if (index !== -1) {
            oferta = state.ofertas[index];
            state.ofertas.splice(index, 1);
            let comprador_1 = state.login;
            let comprador_2 = null;
            for (let i = 0; i < state.sobreviventes.length; i++) {
                if (state.sobreviventes[i].id === state.login.id) { 
                    comprador_2 = state.sobreviventes[i];
                    break;
                }
            }
            let vendedor = null;
            for (let i = 0; i < state.sobreviventes.length; i++) {
                if (state.sobreviventes[i].id === oferta.vendedor) { 
                    vendedor = state.sobreviventes[i];
                    break;
                }
            }
            console.log({comprador_1, comprador_2, vendedor});
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