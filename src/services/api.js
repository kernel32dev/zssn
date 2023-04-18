import axios from 'axios'
import Cookies from 'js-cookie'

// essa função pega uma promise do axios que falha, e retorna uma promise que sempre retorna um objeto javascript
// esse objecto tem um campo booleano chamado "ok"
// se o request tiver sucesso, o campo ok conterá um objeto com a resposta do servidor e "err" não estara definido
// se o request falhar, o campo err conterá o erro, informações adicionais serão encontradas no própio objeto (como status) e "ok" não estará definido
// portanto você pode verificar se deu certo ou não apenas usando if (!result.err) ou if (result.err)
function handle_errors(promise) {
    return new Promise(resolve => {
        promise.then(response => {
            let json = null
            try {
                json = {ok: response.data}
            } catch (e) {
                json = {err: "bad json"}
            }
            resolve(json)
        }).catch(error => {
            if (error.response && error.response.status != 200) {
                let status = error.response.status;
                if (status === 403) {
                    resolve({err: "forbidden", status})
                } else if (status === 404) {
                    resolve({err: "not found", status})
                } else if (status === 409) {
                    resolve({err: "conflict", status})
                } else {
                    resolve({err: "bad status", status})
                }
            } else if (error.message = "Network Error") {
                resolve({err: "bad connection"})
            } else {
                resolve({err: `axios error: ${error.message}`})
            }
        })
    })
}

export default {
    axios: axios.create({
        baseURL: '/api',
        timeout: 5000,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    }),
    get(url) {
        return handle_errors(this.axios.get(url))
    },
    post(url, data) {
        return handle_errors(this.axios.post(url, data))
    },
    delete(url) {
        return handle_errors(this.axios.delete(url))
    }
}