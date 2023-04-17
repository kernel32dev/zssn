import json
import decimal
import hashlib
import datetime
import string
import random
import uuid
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, Http404
from django.conf import settings
from django.core.exceptions import PermissionDenied, BadRequest
from schema import Schema, And, Or, Use, SchemaError
from .models import Sobrevivente, ItemComercial, Relato, Inventario, Sessao

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

SESSION_COOKIE_NAME = "sessionid"
DEBUG = settings.DEBUG

ident = 4 if DEBUG else None

################
# AUTENTICAÇÃO #
################

"""
POST: {
    "name": String,
    "senha": String,
} -> {
    "id": Number,
    "nome": String,
    "sexo": String, ('M' ou 'F')
    "posicao": {
        "latitude": Number,
        "longitude": Number,
    } | null,
    "infectado": String, (data)
    "inventario": [{
        "id": Number, (id do item)
        "nome": String, (nome do item)
        "quant": Number,
        "pontos": Number, (valor em pontos de um item)
    }]
} & cria a sessão
"""
def login(request: HttpRequest):
    try:
        login_schema = Schema({
            "nome": And(Use(str), lambda x: 4 < len(x) < 100),
            "senha": Use(str),
        })
        body = login_schema.validate(json.loads(request.body))
        if request.method == "POST":
            sobrevivente = Sobrevivente.objects.get(nome=body["nome"], infectado=None)
            hasher = hashlib.sha256()
            hasher.update(body["senha"].encode())
            hasher.update(sobrevivente.sal.encode())
            hash_calculado = hasher.hexdigest()
            if hash_calculado == sobrevivente.senha:
                velha_sessao = None
                try:
                    velha_sessao = autenticar_sessao(request)
                except Exception:
                    pass
                if velha_sessao != None:
                    velha_sessao.delete()
                sessao = Sessao(usuario = sobrevivente, validade = datetime.datetime.now() + datetime.timedelta(days=1))
                sessao.save()
                result = sobrevivente_para_dict(sobrevivente, True)
                response = HttpResponse(json.dumps(result, indent=ident, cls=DecimalEncoder))
                set_cookie(response, SESSION_COOKIE_NAME, str(sessao.id), 1)
                return response
            else:
                raise PermissionDenied
        else:
            raise Http404()
    except json.JSONDecodeError as error:
        if DEBUG: raise
        print(repr(error))
        raise BadRequest()
    except SchemaError as error:
        if DEBUG: raise
        print(repr(error))
        raise BadRequest()
    except Exception as error:
        if DEBUG: raise
        print(repr(error))
        raise Http404()

"""
POST: deleta a sessão e limpa o cookie do navegador
"""
def logoff(request: HttpRequest):
    try:
        if request.method == "POST":
            autenticar_sessao(request).delete()
            response = HttpResponse("")
            unset_cookie(response, SESSION_COOKIE_NAME)
            return response
        else:
            raise Http404()
    except Exception as error:
        if DEBUG: raise
        print(repr(error))
        raise Http404()

"""
POST: cadastra um novo sobrevivente e cria sua sessão
{
    "nome": String,
    "senha": String,
    "sexo": String, ('M' ou 'F')
    "posicao": {
        "latitude": Number,
        "longitude": Number,
    } | null,
    "inventario": [{
        "id": Number, (id do item)
        "quant": Number,
    }]
} -> {
    "id": Number,
    "nome": String,
    "sexo": String, ('M' ou 'F')
    "posicao": {
        "latitude": Number,
        "longitude": Number,
    } | null,
    "infectado": String, (data)
    "inventario": [{
        "id": Number, (id do item)
        "nome": String, (nome do item)
        "quant": Number,
        "pontos": Number, (valor em pontos de um item)
    }]
}
"""
def signup(request: HttpRequest):
    try:
        if request.method == "POST":
            sobrevivente_schema = Schema({
                "nome": Use(str),
                "senha": Use(str),
                "sexo": And(Use(str), lambda s: s == "M" or s == "F"),
                "posicao": Or({
                    "latitude": Use(float),
                    "longitude": Use(float),
                }, None),
                "inventario": [{
                    "id": Use(int),
                    "quant": Use(int),
                }]
            })
            body = sobrevivente_schema.validate(json.loads(request.body))
            sal = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
            hasher = hashlib.sha256()
            hasher.update(body["senha"].encode())
            hasher.update(sal.encode())
            senha = hasher.hexdigest()
            sobrevivente = Sobrevivente(
                nome = body["nome"],
                sexo = body["sexo"],
                latitude = body["posicao"]["latitude"] if body["posicao"] != None else None,
                longitude = body["posicao"]["longitude"] if body["posicao"] != None else None,
                senha = senha,
                sal = sal,
            )
            sobrevivente.save()
            try:
                for inventario_item in body["inventario"]:
                    Inventario(
                        dono = sobrevivente,
                        item = ItemComercial.objects.get(id=inventario_item["id"]),
                        quant = inventario_item["quant"],
                    ).save()
                sessao = Sessao(usuario = sobrevivente, validade = datetime.datetime.now() + datetime.timedelta(days=1))
                sessao.save()
            except:
                sobrevivente.delete()
                raise
            result = sobrevivente_para_dict(sobrevivente, True)
            response = HttpResponse(json.dumps(result, indent=ident, cls=DecimalEncoder))
            set_cookie(response, SESSION_COOKIE_NAME, str(sessao.id), 1)
            return response
        elif request.method == "DELETE" and id != None:
            (rows_deleted, _) = Sobrevivente.objects.get(id=id).delete()
            if rows_deleted != 1:
                raise Http404()
            return HttpResponse("{}")
        else:
            raise Http404()
    except json.JSONDecodeError as error:
        if DEBUG: raise
        print(repr(error))
        raise BadRequest()
    except SchemaError as error:
        if DEBUG: raise
        print(repr(error))
        raise BadRequest()
    except Exception as error:
        if DEBUG: raise
        print(repr(error))
        raise Http404()

"""
POST: deleta o usuário
"""
def signout(request: HttpRequest):
    try:
        if request.method == "POST":
            autenticar_usuario(request).delete()
        else:
            raise Http404()
        return HttpResponse("")
    except Exception as error:
        if DEBUG: raise
        print(repr(error))
        raise Http404()

#################
# APIS PRIVADAS #
#################

"""
GET: retorna todas as informações deste sobrevivente
{
    "id": Number,
    "nome": String,
    "sexo": String, ('M' ou 'F')
    "posicao": {
        "latitude": Number,
        "longitude": Number,
    } | null,
    "infectado": String, (data)
    "inventario": [{
        "id": Number, (id do item)
        "nome": String, (nome do item)
        "quant": Number,
        "pontos": Number, (valor em pontos de um item)
    }]
}
"""
def sobrevivente(request: HttpRequest):
    try:
        sobrevivente = autenticar_usuario(request)
        if request.method == "GET":
            result = sobrevivente_para_dict(sobrevivente, True)
        else:
            raise Http404()
        return HttpResponse(json.dumps(result, indent=ident, cls=DecimalEncoder))
    except Exception as error:
        if DEBUG: raise
        print(repr(error))
        raise Http404()

"""
POST: atualiza a posição do sobrevivente
{
    "latitude": Number,
    "longitude": Number,
}
"""
def posicao(request: HttpRequest):
    try:
        posicao_schema = Schema({
            "latitude": And(Use(float), lambda x: -90 < x < 90),
            "longitude": And(Use(float), lambda x: -180 < x < 180),
        })
        sobrevivente = autenticar_usuario(request)
        if request.method == "POST":
            sobrevivente.latitude = posicao_schema["latitude"]
            sobrevivente.longitude = posicao_schema["longitude"]
            sobrevivente.save()
        else:
            raise Http404()
        return HttpResponse("")
    except SchemaError:
        raise BadRequest()
    except Exception as error:
        if DEBUG: raise
        print(repr(error))
        raise Http404()

"""
POST: cria um relato
DELETE: apaga um relato
"""
def relato(request: HttpRequest, **kwargs):
    try:
        relator = autenticar_usuario(request).id
        relatado = kwargs.get('relatado')
        if relatado == None:
            raise BadRequest()
        if request.method == "POST":
            if Relato.objects.filter(relator = relator, relatado = relatado).count() == 0:
                Relato(relator = relator, relatado = relatado).save()
        elif request.method == "DELETE":
            Relato.objects.filter(relator = relator, relatado = relatado).delete()
        else:
            raise Http404()
    except Exception as error:
        if DEBUG: raise
        print(repr(error))
        raise Http404()

#################
# APIS PÚBLICAS #
#################

"""
GET: retorna todos os sobreviventes
{
    "sobreviventes": [{
        "id": Number,
        "nome": String,
        "sexo": String, ('M' ou 'F')
        "posicao": {
            "latitude": Number,
            "longitude": Number,
        } | null,
        "infectado": String, (data) | null
    }]
}
"""
def sobreviventes(request: HttpRequest):
    try:
        if request.method == "GET":
            sobreviventes = []
            for sobrevivente in Sobrevivente.objects.all():
                sobreviventes.append(sobrevivente_para_dict(sobrevivente, False))
            result = {
                "sobreviventes": sobreviventes
            }
        else:
            raise Http404()
        return HttpResponse(json.dumps(result, indent=ident, cls=DecimalEncoder))
    except Exception as error:
        if DEBUG: raise
        print(repr(error))
        raise Http404()

"""
GET: retorna todos os itens
{
    "itens": [{
        "id": Number, (id do item)
        "nome": String, (nome do item)
        "pontos": Number, (valor em pontos de um item)
    }]
}
"""
def itens(request: HttpRequest):
    try:
        if request.method == "GET":
            itens = []
            for item in ItemComercial.objects.all():
                itens.append({
                    "id": item.id,
                    "item": item.nome,
                    "pontos": item.pontos,
                })
            result = {
                "itens": itens
            }
        else:
            raise Http404()
        return HttpResponse(json.dumps(result, indent=ident, cls=DecimalEncoder))
    except Exception as error:
        if DEBUG: raise
        print(repr(error))
        raise Http404()

"""
GET: retorna todos os relatos
{
    "relatos": [
        [
            relator:Number, relatado:Number
        ]
    ]
}
"""
def relatos(request: HttpRequest):
    try:
        if request.method == "GET":
            itens = []
            for relato in Relato.objects.all().order_by('relator', 'relatado'):
                itens.append([relato.relator.id, relato.relatado.id])
            result = {
                "itens": itens
            }
        else:
            raise Http404()
        return HttpResponse(json.dumps(result, indent=ident, cls=DecimalEncoder))
    except Exception as error:
        if DEBUG: raise
        print(repr(error))
        raise Http404()

############
# NÃO APIS #
############

def sobrevivente_para_dict(sobrevivente: Sobrevivente, inclui_inventario: bool):
        if sobrevivente.latitude != None and sobrevivente.longitude != None:
            posicao = {
                "latitude": sobrevivente.latitude,
                "longitude": sobrevivente.longitude,
            }
        else:
            posicao = None
        if inclui_inventario:
            inventario = []
            for inventario_item in Inventario.objects.filter(dono=sobrevivente.id):
                inventario.append({
                    "id": inventario_item.item.id,
                    "nome": inventario_item.item.nome,
                    "quant": inventario_item.quant,
                    "pontos": inventario_item.item.pontos,
                })
            return {
                "id": sobrevivente.id,
                "nome": sobrevivente.nome,
                "sexo": sobrevivente.sexo,
                "posicao": posicao,
                "infectado": sobrevivente.infectado,
                "inventario": inventario,
            }
        else:
            return {
                "id": sobrevivente.id,
                "nome": sobrevivente.nome,
                "sexo": sobrevivente.sexo,
                "posicao": posicao,
                "infectado": sobrevivente.infectado,
            }

"""
função que pega o cookie, procura a sessão e retorna o sobrevivente logado
se não for possível autenticar esse request, raise PermissionDenied
"""
def autenticar_usuario(request: HttpRequest):
    return autenticar_sessao(request).usuario

"""
função que pega o cookie, procura a sessão e retorna a sessão
se não for possível autenticar esse request, raise PermissionDenied
"""
def autenticar_sessao(request: HttpRequest):
    sessao = request.COOKIES.get(SESSION_COOKIE_NAME)
    if sessao == None:
        raise PermissionDenied()
    try:
        id = uuid.UUID(sessao)
    except Exception:
        raise BadRequest()
    try:
        return Sessao.objects.get(id=id)
    except Exception:
        raise PermissionDenied()

def set_cookie(response: HttpResponse, key: str, value: str, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        httponly=True,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None,
    )

def unset_cookie(response: HttpResponse, key: str):
    response.set_cookie(key, "", max_age=0, expires=-1)
