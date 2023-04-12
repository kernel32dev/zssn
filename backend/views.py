import json
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, Http404
from schema import Schema, And, Use, Optional, SchemaError
from .models import Sobrevivente, ItemComercial, Relato, Inventario

"""
GET: retorna todas as informações deste sobrevivente
{
    "id": Number,
    "nome": String,
    "sexo": String, ('M' ou 'F')
    "latitude": Number,
    "longitude": Number,
    "infectado": String, (data)
    "relatores": [{
        "id": Number, (id de quem relatou)
        "nome": String, (nome de quem relatou)
    }],
    "relatados": [{
        "id": Number, (id de quem foi relatado)
        "nome": String, (nome de quem foi relatado)
    }],
    "inventario": [{
        "id": Number, (id do item)
        "nome": String, (nome do item)
        "quant": Number,
        "pontos": Number, (valor em pontos de um item)
    }]
}
POST: cadastra um novo sobrevivente
{
    "nome": String,
    "sexo": String, ('M' ou 'F')
    "latitude": Number,
    "longitude": Number,
    "inventario": [{
        "id": Number, (id do item)
        "quant": Number,
    }]
} -> {
    "id": Number,
}
DELETE: marca um sobrevivente como apagado
"""
def sobrevivente(request: HttpRequest, **kwargs):
    def para_dict(sobrevivente: Sobrevivente):
        relatores = []
        relatados = []
        inventario = []
        for relato in Relato.objects.filter(relatado=sobrevivente.id):
            relatores.append({
                "id": relato.relator.id,
                "nome": relato.relator.nome,
            })
        for relato in Relato.objects.filter(relator=sobrevivente.id):
            relatados.append({
                "id": relato.relatado.id,
                "nome": relato.relatado.nome,
            })
        for inventario_item in inventario.objects.filter(dono=sobrevivente.id):
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
            "latitude": sobrevivente.latitude,
            "longitude": sobrevivente.longitude,
            "infectado": sobrevivente.infectado,
            "relatores": relatores,
            "relatados": relatados,
            "inventario": inventario,
        }
    try:
        id = kwargs.get("id")
        if request.method == "GET" and id != None:
            result = para_dict(Sobrevivente.objects.get(id=id))
        elif request.method == "GET":
            sobreviventes = []
            for sobrevivente in Sobrevivente.objects.get(id=id):
                sobreviventes.append(para_dict(sobrevivente))
            result = {
                "sobreviventes": sobreviventes
            }
        elif request.method == "POST":        
            sobrevivente_schema = Schema({
                "nome": And(Use(str)),
                "sexo": And(Use(str), lambda s: s == "M" or s == "F"),
                "latitude": And(Use(float)),
                "longitude": And(Use(float)),
                "inventario": [{
                    "id": And(Use(int)),
                    "quant": And(Use(int)),
                }]
            })
            body = sobrevivente_schema.validate(json.loads(request.body))
            sobrevivente = Sobrevivente(
                nome = body.nome,
                sexo = body.sexo,
                latitude = body.latitude,
                longitude = body.longitude,
            )
            sobrevivente.save()
            for inventario_item in body.inventario:
                Inventario(
                    dono = sobrevivente.id,
                    item = inventario_item.id,
                    quant = inventario_item.quant,
                ).save()
            result = {
                "id": sobrevivente.id
            }
        elif request.method == "DELETE" and id != None:
            (rows_deleted, _) = Sobrevivente.objects.get(id=id).delete()
            if rows_deleted != 1:
                return Http404()
            result = {}
        else:
            return Http404()
        return HttpResponse(json.dumps(result, indent=4))
    except Exception as error:
        print(repr(error))
        return Http404()

"""
POST: cria um relato
{
    "relator": Number,
    "relatado": Number,
}
DELETE: marca um sobrevivente como apagado
{
    "relator": Number,
    "relatado": Number,
}
"""
def relato(request: HttpRequest):
    try:
        if request.method == "POST" or request.method == "DELETE":
            relato_schema = Schema({
                "relator": And(Use(int), lambda x: x >= 0),
                "relatado": And(Use(int), lambda x: x >= 0),
            })
            body = relato_schema.validate(json.loads(request.body))
            if request.method == "POST":
                Relato(relator = body.relator, relatado = body.relatado).save()
            elif request.method == "DELETE":
                Relato.objects.filter(relator = body.relator, relatado = body.relatado).delete()
    except Exception as error:
        print(repr(error))
        return Http404()

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
def item(request: HttpRequest):
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
            return HttpResponse(json.dumps(result, indent=4))
        else:
            return Http404()
    except Exception as error:
        print(repr(error))
        return Http404()
