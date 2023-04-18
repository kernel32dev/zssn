<template>
    <div id="comprar">
        <div id="header">
            <h3>Ofertas:</h3>
        </div>
        <div v-for="oferta in ofertas" class="card">
            <div class="ofertas">
                <div class="side">
                    <h4>Steve oferece:</h4>
                    <div class="item" v-for="item in oferta.itens" v-if="item.quant > 0">{{ item.quant }} x {{ item.item }}</div>
                </div>
                <div class="slit"></div>
                <div class="side">
                    <h4>Em troca de:</h4>
                    <div class="item" v-for="item in oferta.itens" v-if="item.quant < 0">{{ -item.quant }} x {{ item.item }}</div>
                </div>
            </div>
            <button class="comprar-oferta" @click="comprarOferta(oferta.id)">Aceitar oferta</button>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
    name: 'Comprar',
    computed: mapState({
        ofertas: state => {
            let ofertas = [];
            for (let i = 0; i < state.backend.ofertas.length; i++) {
                let oferta = state.backend.ofertas[i];
                if (oferta.vendedor !== state.backend.login.id) {
                    let itens = [];
                    for (let j = 0; j < oferta.itens.length; j++) {
                        let item_oferta = oferta.itens[j];
                        for (let k = 0; k < state.backend.itens.length; k++) {
                            let item = state.backend.itens[k];
                            if (item.id === item_oferta.id) {
                                itens.push({
                                    id: item_oferta.id,
                                    item: item.item,
                                    quant: item_oferta.quant,
                                });
                                break;
                            }
                        }
                    }
                    for (let j = 0; j < state.backend.sobreviventes.length; j++) {
                        let sobrevivente = state.backend.sobreviventes[j];
                        if (sobrevivente.id === oferta.vendedor) {
                            ofertas.push({
                                id: oferta.id,
                                vendedor: sobrevivente.nome,
                                itens: itens,
                            });
                            break;
                        }
                    }
                }
            }
            return ofertas;
        }
    }),
    methods: {
        comprarOferta(oferta) {
            this.$store.dispatch('backend/postCompra', oferta);
        }
    }
}
</script>

<style scoped>
#comprar {
    padding: 30px;
}
.apaga-oferta { background-color: rgb(255, 110, 110); }
.apaga-oferta:hover { background-color: rgb(255, 149, 149); }
.apaga-oferta:active { background-color: rgb(255, 169, 169); }
.card {
    color: black;
    width: calc(100% - 40px);
    padding: 20px;
    border-radius: 30px;
    margin-top: 20px;
    border: 1px gray solid;
    background-color: lightgray;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: end;
}
.card .ofertas {
    display: flex;
    flex-direction: row;
    width: 100%;
    margin-bottom: 20px;
}
.card .side {
    width: 50%;
    height: 100%;
}
.card .side:first-child {
    border-right: 1px gray solid;
}
</style>
