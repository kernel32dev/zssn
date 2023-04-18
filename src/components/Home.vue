<template>
    <div id="home">
        <div id="home-content">
            <h2>{{ login.nome }}</h2>
            <h6 v-if="login.sexo === 'M'">Sobrevivente, Homem</h6>
            <h6 v-if="login.sexo === 'F'">Sobrevivente, Mulher</h6>
            <div id="posicao">
                <h4>Posição:</h4>
                <div id="posicao-inputs">
                    <div class="posicao-input">
                        <span>Latitude:</span>
                        <input v-model="latitude" id="latitude" type="text">
                    </div>
                    <div class="posicao-input-space"></div>
                    <div class="posicao-input">
                        <span>Longitude:</span>
                        <input v-model="longitude" id="longitude" type="text">
                    </div>
                </div>
                <button id="posicao-submit" class="button green" @click="savePosition()" tabindex="0"><span class="icon">&#xf0c7;</span> Salvar</button>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Pontos</th>
                        <th>Quant</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in login.inventario">
                        <td>{{ item.nome }}</td>
                        <td>{{ item.pontos }}</td>
                        <td>{{ item.quant }}</td>
                    </tr>
                </tbody>
            </table>
            <p>&nbsp;</p>
            <p>Total de pontos: {{ login.inventario.map(x => x.pontos * x.quant).reduce((a,b) => a+b) }}</p>
            <p>&nbsp;</p>
            <div id="button-row">
                <button id="signout" class="button red" @click="signout()" tabindex="0"><span class="icon">&#xf2ed;</span> Apagar Conta</button>
                <div class="button-row-space"></div>
                <button id="logoff" class="button orange" @click="logoff()" tabindex="0"><span class="icon">&#xf08b;</span> Sair</button>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
export default {
    name: 'Home',
    data() {
        let posicao = this.$store.state.backend.login.posicao || {
            latitude: "", 
            longitude: "",
        };
        return {
            latitude: String(posicao.latitude).replace('.', ','),
            longitude: String(posicao.longitude).replace('.', ','),
        };
    },
    computed: mapState({
        login: state => state.backend.login,
        itens: state => state.backend.itens,
    }),
    methods: {
        savePosition() {
            let error = false;
            let latitude = validate_number(this.latitude, -90, 90);
            let longitude = validate_number(this.longitude, -180, 180);
            if (latitude === null) {
                attention("latitude")
                if (!error) {
                    document.getElementById("latitude").focus();
                    error = true;
                }
            }
            if (longitude === null) {
                attention("longitude")
                if (!error) {
                    document.getElementById("longitude").focus();
                    error = true;
                }
            }
            if (error) return;
            this.postPosicao({
                "latitude": latitude,
                "longitude": longitude,
            });
        },
        ...mapActions('backend', ['logoff', 'signout', 'postPosicao'])
    }
}
function validate_number(text, min, max) {
    text = text.trim();
    let is_integer = /^\d+$/.test(text);
    let is_fraction = /^\d+,\d+$/.test(text);
    if (!is_integer && !is_fraction) {
        return null;
    }
    if (is_fraction) {
        text = text.replace(',', '.');
    }
    let number = Number(text);
    if (number < min || number > max) {
        return null;
    }
    return number;
}
function attention(elem) {
    if (typeof elem === "string") {
        elem = document.getElementById(elem);
    }
    elem.classList.remove('attention');
    setTimeout(() => elem.classList.add('attention'), 1);
}
</script>

<style scoped>
#home {
    padding-top: 50px;
    text-align: center;
}
#home-content {
    width: min(100% - 100px, 400px);
    margin: 0 auto;
}
h6 {
    color: gray;
}
#posicao {
    margin: 50px 0;
    border: 1px gray solid;
    padding: 15px 20px 20px;
    width: calc(100% - 40px);
    display: flex;
    align-items: end;
    flex-direction: column;
}
#posicao input {
    flex-shrink: 1;
}
#posicao h4 {
    text-align: left;
    margin-bottom: 10px;
    width: 100%;
}
#button-row {
    display: flex;
    flex-direction: row;
}
#signout, #logoff {
    min-width: 150px;
}
.button-row-space {
    flex-grow: 1;
}
#posicao-inputs {
    display: flex;
    flex-direction: row;
    margin-bottom: 20px;
    width: 100%;
}
#posicao-inputs input {
    max-width: 150px;
}
.posicao-input-space {
    flex-grow: 1;
    min-width: 1em;
}
.posicao-input {
    display: flex;
    flex-direction: column;
}
#posicao-input span {
    text-align: left;
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
</style>
