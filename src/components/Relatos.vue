<template>
    <div id="relatos">
        <table>
            <thead>
                <tr>
                    <th>Relatado</th>
                    <th>Relator #1</th>
                    <th>Relator #2</th>
                    <th>Relator #3</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="linha in resumo">
                    <td v-if="linha.relatado.id !== login.id">{{ linha.relatado.nome }}</td>
                    <td v-if="linha.relatado.id === login.id">Você</td>
                    <td v-for="index in [0,1,2]">
                        <div class="owned-report" v-if="index < linha.relatores.length && linha.relatores[index].id === login.id">Você<button v-if="linha.relatado.infectado === null" class="button icon" @click="anulaRelato(linha.relatado.id)">&#xf2ed;</button></div>
                        <span v-if="index < linha.relatores.length && linha.relatores[index].id !== login.id" class="button">{{ linha.relatores[index].nome }}</span>
                        <button v-if="index === linha.relatores.length && join(linha.relatores, login.id) === null" class="button" @click="criaRelato(linha.relatado.id)">Relatar</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
    name: 'Relatos',
    data() {
        return {}
    },
    methods: {
        join,
        criaRelato(relatado) {
            this.$store.dispatch('backend/postRelato', relatado);
        },
        anulaRelato(relatado) {
            this.$store.dispatch('backend/deleteRelato', relatado);
        },
    },
    computed: mapState({
        login: state => state.backend.login,
        itens: state => state.backend.itens,
        relatos: state => state.backend.relatos,
        resumo: state => {
            let resumo = [];
            let me = null;
            let sobreviventes = state.backend.sobreviventes;
            let login = state.backend.login;
            let relatos = state.backend.relatos;
            resumo.length = sobreviventes.length;
            for (let i = 0; i < resumo.length; i++) {
                if (sobreviventes[i].id === login.id) {
                    me = i;
                }
                resumo[i] = {
                    id: sobreviventes[i].id,
                    relatado: sobreviventes[i],
                    relatores: [],
                }
            }
            if (me !== null) {
                resumo.splice(me, 1);
            }
            for (let relato of relatos) {
                let linha = join(resumo, relato[1]);
                if (linha === null) continue;
                let relator = join(sobreviventes, relato[0]);
                if (relator === null) continue;
                linha.relatores.push(relator);
            }
            resumo.sort((a, b) => a.id - b.id)
            return resumo;
        }
    }),
}
function join(src, id) {
    for (let i = 0; i < src.length; i++) {
        if (src[i].id === id) {
            return src[i];
        }
    }
    return null;
}
</script>

<style scoped>
#relatos {
    padding: 30px;
}
table {
    width: 100%;
    max-width: 700px;
    margin: 0 auto;
    border-collapse: collapse;
}
thead th {
    background-color: #f0f0f0;
    font-weight: bold;
    padding: 10px;
    text-align: left;
    border: 1px solid #ccc;
}
tbody tr {
    background-color: #ffffff;
}
tbody td {
    padding: 10px;
    border: 1px solid #ccc;
    text-align: center;
}
tbody td:first-child {
    font-weight: bold;
    text-align: left;
}
tbody td:nth-child(even) {
    background-color: #f9f9f9;
}
tbody td:nth-child(odd) {
    background-color: #ffffff;
}
.owned-report {
    display: flex;
    flex-direction: row;
    justify-content: space-evenly;
    align-items: center;
}
button {
    background-color: white;
}
button:hover {
    background-color: rgb(229, 229, 229);
}
button:active {
    background-color: rgb(206, 206, 206);
}
</style>
