<template>
    <div id="login">
        <div id="card">
            <div id="header">
                <h3>ZSSN</h3>
                <h4>Rede Social de Sobrevivência Zumbi</h4>
            </div>
            <div id="input">
                <div class="input-space"></div>
                <p>Nome do usuário</p>
                <input type="text" id="username" v-model="username" @keydown="handleEnter($event)">
                <div class="input-space"></div>
                <div id="password-label">
                    <p>Senha</p>
                    <div class="space"></div>
                    <div id="view-password" @click="showPassword = !showPassword">
                        <span v-if="!showPassword">&#xf070;</span>
                        <span v-if="showPassword">&#xf06e;</span>
                    </div>
                </div>
                <input v-if="showPassword" type="text" id="password" class="input" v-model="password" @keydown="handleEnter($event)"/>
                <input v-else          type="password" id="password" class="input" v-model="password" @keydown="handleEnter($event)"/>
                <div class="input-space"></div>
                <div v-if="register">
                    <p>Genêro:</p>
                    <select id="select-genero">
                        <option value="">-------</option>
                        <option value="M">Masculino</option>
                        <option value="F">Feminino</option>
                    </select>
                    <div class="input-space"></div>
                    <p>Inventário:</p>
                    <table>
                        <thead>
                            <tr>
                                <th>Item</th>
                                <th>Pontos</th>
                                <th>Quant.</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item in itens">
                                <td>{{ item.item }}</td>
                                <td class="pontos-td">{{ item.pontos }}</td>
                                <td class="quant-td">
                                    <button class="quant-button" @click="mutateQuant(item.id, -1)" :class="{disabled: !quants[item.id]}">-</button>
                                    <div class="quant-label">{{ quants[item.id] || 0 }}</div>
                                    <button class="quant-button" @click="mutateQuant(item.id, 1)">+</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <p>&nbsp;</p>
                    <div id="items-total" v-if="pontos_total !== 1">Você tem {{ pontos_total }} pontos no seu inventário</div>
                    <div id="items-total" v-if="pontos_total === 1">Você tem 1 ponto no seu inventário</div>
                </div>
                <p>&nbsp;</p>
            </div>
            <div class="buttons">
                <div class="button" v-if="!register" :class="{disabled: loading}" @click="register = true">Registrar...</div>
                <div class="button" v-if="register" :class="{disabled: loading}" @click="register = false">Entrar...</div>
                <div class="space"></div>
                <button type="submit" class="button highlight" v-if="!register && !loading" @click="submit()">Entrar</button>
                <button type="submit" class="button highlight" v-if="register && !loading" @click="submit()">Registrar</button>
                <button type="submit" class="button highlight button-loading" v-if="loading"><span>&#xf110;</span></button>
            </div>
        </div>
    </div>
</template>

<script>
import Vue from 'vue'
import { mapState, mapActions } from 'vuex'
export default {
    name: 'Login',
    data() {
        return {
            username: "",
            password: "",
            showPassword: false,
            register: false,
            loading: false,
            quants: {},
            pontos_total: 0,
        };
    },
    computed: mapState({
        login: state => state.backend.login,
        itens: state => state.backend.itens,
    }),
    methods: {
        handleEnter(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                if (event.target.id === "password") {
                    this.submit();
                } else {
                    document.getElementById("password").focus();
                }
            }
        },
        mutateQuant(id, delta) {
            console.log(`mutateQuant(${id},${delta})`)
            if (this.quants[id] === undefined) {
                if (delta === -1) return;
                Vue.set(this.quants, id, delta);
            } else {
                this.quants[id] += delta;
            }
            if (this.quants[id] <= 0) {
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
        submit() {
            let error = false;
            if (this.username === "") {
                attention("username");
                error = true;
            }
            if (this.password === "") {
                attention("password");
                error = true;
            }
            if (!this.register) {
                if (error) return;
                this.$store.dispatch('backend/login', {
                    "nome": this.username,
                    "senha": this.password,
                });
            } else {
                let sexo = document.getElementById("select-genero").value;
                if (sexo !== "M" && sexo !== "F") {
                    attention("select-genero");
                    error = true;
                }
                if (error) return;
                let inventario = []
                for (let id in this.quants) {
                    inventario.push({
                        "id": Number(id),
                        "quant": this.quants[id],
                    });
                }
                this.$store.dispatch('backend/signup', {
                    "nome": this.username,
                    "senha": this.password,
                    "sexo": sexo,
                    "posicao": null,
                    "inventario": inventario,
                });
            }
        },
        ...mapActions('backend', [])
    }
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
#login {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}
#card {
    border: 3px solid var(--theme-color);
    display: flex;
    flex-direction: column;
    width: 400px;
    box-shadow: black 0px 0px 10px 0px;
    border-radius: 30px;
    overflow: hidden;
}
#header {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 100%;
    height: 80px;
    background-color: var(--theme-color);
}
#header h3 {
    margin-left: 20px;
    font-style: italic;
}
#header h4 {
    margin-left: 30px;
    font-style: italic;
}
#input {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    padding: 0 30px;
}
#input input {
    width: calc(100% - 1em - 3px);
    height: 2em;
    padding: 0 0.5em;
    border: 1px solid gray;
}
#input p {
    vertical-align: bottom;
}
#password-label {
    display: flex;
    flex-direction: row;
    position: relative;
}
#view-password {
    border-radius: 50%;
    position: absolute;
    bottom: 3px;
    right: 0;
    width: 2em;
    line-height: 2em;
    text-align: center;
    font-family: 'Font Awesome 6 Free';
    user-select: none;
}
#view-password:hover {
    background-color: #DDD;
}
#view-password:active {
    background-color: #BBB;
}
#view-password:active #view-password-blur, #view-password-focus {
    display: none;
}
#view-password:active #view-password-focus, #view-password-blur {
    display: block;
}
.pontos-td {
    text-align: center;
}
.quant-td {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
.buttons {
    height: 60px;
    background-color: lightgray;
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 0 30px;
}
.quant-label {
    width: 3em;
    text-align: center;
}
table {
    width: 100%;
}
tr {
    height: 30px;
}
.button {
    font-size: 1em;
    border: 1px solid gray;
    user-select: none;
    cursor: pointer;
    background-color: lightgray;
    border-radius: 10px;
    padding: 8px 15px;
}
.quant-button {
    font-size: 1.5em;
    width: 23px;
    height: 23px;
    border: 1px solid gray;
    user-select: none;
    cursor: pointer;
    background-color: lightgray;
    border-radius: 3px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.button.disabled, .quant-button.disabled {
    pointer-events: none;
    background-color: rgb(129, 129, 129);
}
.button:hover, .quant-button:hover {
    background-color: rgb(180, 180, 180);
}
.button:active, .quant-button:active {
    background-color: rgb(164, 164, 164);
}
.button.highlight {
    background-color: var(--theme-color-button);
}
.button.highlight:hover {
    background-color: var(--theme-color-button-hover);
}
.button.highlight:active {
    background-color: var(--theme-color-button-active);
}
.button-loading span {
    font-family: 'Font Awesome 6 Free';
    animation: pulse-rotate 1s linear 0s infinite;
    display: block;
}
@keyframes pulse-rotate {
    0% { transform: rotate(0deg); }
    12.5% { transform: rotate(0deg); }
    12.50001% { transform: rotate(45deg); }
    25% { transform: rotate(45deg); }
    25.00001% { transform: rotate(90deg); }
    37.5% { transform: rotate(90deg); }
    37.50001% { transform: rotate(135deg); }
    50% { transform: rotate(135deg); }
    50.00001% { transform: rotate(180deg); }
    62.5% { transform: rotate(180deg); }
    62.50001% { transform: rotate(225deg); }
    75% { transform: rotate(225deg); }
    75.00001% { transform: rotate(270deg); }
    87.5% { transform: rotate(270deg); }
    87.50001% { transform: rotate(315deg); }
    99.99999% { transform: rotate(315deg); }
    100% { transform: rotate(360deg); }
}
.space {
    flex-grow: 1;
}
.input-space {
    height: 32px;
}
#items-total {
    width: 100%;
    text-align: center;
}
#select-genero {
    width: 100%;
    height: 30px;
}
@keyframes attention {
    0%   { box-shadow: 0 0 0px 0px red; }
    50%  { box-shadow: 0 0 13px 4px red; }
    100% { box-shadow: 0 0 0px 0px red; }
}
.attention {
    animation: attention 1s ease;
}
</style>
