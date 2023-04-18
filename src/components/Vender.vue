<template>
    <div id="vender">
        <div v-if="!prompt_venda" id="header">
            <h3>Suas ofertas:</h3>
            <button class="nova-oferta green" @click="novaOferta()">Nova oferta</button>
        </div>
        <div v-if="!prompt_venda" v-for="oferta in ofertas" class="card">
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
            <button class="apaga-oferta" @click="apagaOferta(oferta.id)">Apagar oferta</button>
        </div>
        <div v-if="prompt_venda">
            <table>
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Pontos</th>
                        <th>Quant.</th>
                        <th style="min-width: 100px;">Ação</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in itens">
                        <td>{{ item.item }}</td>
                        <td class="pontos-td">{{ item.pontos }}</td>
                        <td class="quant-td">
                            <button class="quant-button" @click="mutateQuant(item.id, -1)" :class="{disabled: !quants[item.id]}">-</button>
                            <div class="quant-label">{{ Math.abs(quants[item.id] || 0) }}</div>
                            <button class="quant-button" @click="mutateQuant(item.id, 1)">+</button>
                        </td>
                        <td>
                            <button class="direcao-button" v-if="quants[item.id] > 0" @click="flipQuant(item.id)">Vender</button>
                            <button class="direcao-button" v-if="quants[item.id] < 0" @click="flipQuant(item.id)">Comprar</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <p>&nbsp;</p>
            <div class="card">
                <div class="ofertas">
                    <div class="side">
                        <h4>Steve oferece:</h4>
                        <div class="item" v-for="item in itens" v-if="quants[item.id] > 0">{{ quants[item.id] }} x {{ item.item }}</div>
                    </div>
                    <div class="slit"></div>
                    <div class="side">
                        <h4>Em troca de:</h4>
                        <div class="item" v-for="item in itens" v-if="quants[item.id] < 0">{{ -quants[item.id] }} x {{ item.item }}</div>
                    </div>
                </div>
                <div class="button-row">
                    <button class="apaga-oferta red" @click="cancelaOferta()">Cancelar oferta</button>
                    <div class="button-row-space"></div>
                    <button class="salva-oferta green" @click="salvaOferta()">Publicar oferta</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Vue, { del } from 'vue'
import { mapState } from 'vuex'
export default {
    name: 'Vender',
    data() {
        return {
            prompt_venda: false,
            quants: {},
        }
    },
    methods: {
        novaOferta() {
            this.prompt_venda = true;
        },
        cancelaOferta() {
            this.prompt_venda = false;
            this.oferta_itens = [];
        },
        salvaOferta() {
            alert("TODO!");
        },
        apagaOferta(oferta) {
            alert(`apaga: ${oferta}`)
        },
        mutateQuant(id, delta) {
            if (delta === -1 && this.quants[id] === undefined) {
                // não é possivel diminuir abaixo de zero
                return;
            }
            if (this.quants[id] !== undefined && this.quants[id] < 0) {
                delta = -delta;
            }
            console.log(`mutateQuant(${id},${delta})`)
            if (this.quants[id] === undefined) {
                Vue.set(this.quants, id, delta);
            } else {
                this.quants[id] += delta;
            }
            if (this.quants[id] === 0) {
                delete this.quants[id];
            }
            let total = 0;
            for (let id in this.quants) {
                id = Number(id);
                for (let index = 0; index < this.itens.length; index++) {
                    if (this.itens[index].id === id) {
                        total += this.quants[id] * this.itens[index].pontos;
                        break;
                    }
                }
            }
            this.pontos_total = total;
        },
        flipQuant(id) {
            console.log(`flipQuant(${id})`)
            if (this.quants[id] !== undefined) {
                this.quants[id] = -this.quants[id];
            }
        }
    },
    computed: mapState({
        itens: state => state.backend.itens,
        ofertas: state => {
            let ofertas = [];
            for (let i = 0; i < state.backend.ofertas.length; i++) {
                let oferta = state.backend.ofertas[i];
                if (oferta.vendedor === state.backend.login.id) {
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
                    ofertas.push({
                        id: oferta.id,
                        itens: itens,
                    });
                }
            }
            return ofertas;
        }
    })
}
</script>

<style scoped>
#vender {
    padding: 30px;
}
#header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
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
    padding-bottom: 10px;
    border-bottom: gray 1px solid;
}
.card .side {
    width: 50%;
    height: 100%;
}
.card .side:first-child {
    border-right: 1px gray solid;
}
table {
    width: 100%;
    max-width: 700px;
    margin: 20px auto 0;
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
.quant-td {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
.quant-label {
    width: 3em;
    text-align: center;
}
.button-row {
    display: flex;
    flex-direction: row;
}
.button-row-space {
    width: 30px;
}
</style>
