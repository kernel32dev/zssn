import io
import datetime
import math
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, portrait
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from django.http import HttpResponse, HttpRequest, Http404
from django.conf import settings
from django.core.exceptions import PermissionDenied, BadRequest, ObjectDoesNotExist
from schema import Schema, And, Or, Use, SchemaError
from .models import Sobrevivente, ItemComercial, Relato, Inventario, Sessao, Oferta, OfertaItem
from django.middleware import csrf

def infeccoes(request: HttpRequest):
    num_infectados = 0
    num_sobreviventes = 0
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=portrait(letter))
    w, h = portrait(letter)

    x = 30
    y = h - 40
    p.setFontSize(20)
    p.drawString(x, y, "Resumo das infecções")
    y = h - 80
    p.setFontSize(12)
    p.drawString(x, y, "Sobreviventes:")
    p.setFontSize(10)
    for sobrevivente in Sobrevivente.objects.filter(infectado=None):
        num_sobreviventes += 1
        y -= 18
        p.drawString(x, y, sobrevivente.nome)
    y -= 32
    p.setFontSize(12)
    p.drawString(x, y, "Infectados:")
    p.setFontSize(10)
    for sobrevivente in Sobrevivente.objects.exclude(infectado=None):
        num_infectados += 1
        y -= 18
        p.drawString(x, y, sobrevivente.nome)
    perc_infectados = int(100 * num_infectados / (num_infectados + num_sobreviventes))
    perc_sobreviventes = int(100 * num_sobreviventes / (num_infectados + num_sobreviventes))
    p.setFontSize(10)
    p.drawString(30, 30, datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
    x = 300
    y = h - 100
    p.setFontSize(14)
    p.drawString(x, y, f"Infectados: {num_infectados}")
    y -= 24
    p.drawString(x, y, f"Sobreviventes: {num_sobreviventes}")
    y -= 24
    p.drawString(x, y, f"Porcentagem Infectados: {perc_infectados}%")
    y -= 24
    p.drawString(x, y, f"Porcentagem Sobreviventes: {perc_sobreviventes}%")
    p.showPage()

    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='infeccoes.pdf')

def recursos(request: HttpRequest):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=portrait(letter))
    w, h = portrait(letter)

    x = 30
    y = h - 40
    p.setFontSize(20)
    p.drawString(x, y, "Recursos por sobreviventes")
    y = h - 80
    p.setFontSize(12)
    p.drawString(x, y, "Recursos:")
    p.setFontSize(10)
    total = Sobrevivente.objects.filter(infectado=None).count()
    for item in ItemComercial.objects.all():
        quant = 0
        for item_inventario in Inventario.objects.filter(item=item):
            if item_inventario.dono.infectado == None:
                quant += item_inventario.quant
        y -= 18
        p.drawString(x, y, f"{item.nome}: {quant/total} em média por sobrevivente ({quant} itens no total, entre {total} sobreviventes)")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='recursos.pdf')

def recursos_perdidos(request: HttpRequest):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=portrait(letter))
    w, h = portrait(letter)
    num_infectados = 0
    num_sobreviventes = 0

    x = 30
    y = h - 40
    p.setFontSize(20)
    p.drawString(x, y, "Recursos perdidos por sobreviventes infectados")
    y = h - 80
    p.setFontSize(12)
    p.drawString(x, y, "Infectados:")
    p.setFontSize(10)
    totais = {}
    for infectado in Sobrevivente.objects.exclude(infectado=None):
        x = 30
        p.drawString(x, y, f"{infectado.nome}:")
        x += 30
        for item in Inventario.objects.filter(dono=infectado):
            p.drawString(x, y, f" {item.item.nome} x {item.quant},")
            totais[item.item.nome] += item.quant
            x += 20
        y -= 18
    y -= 32
    x = 30
    p.drawString(x, y, "Total: ")
    x += 30
    for key, value in totais:
        p.drawString(x, y, f" {key} x {value},")
        x += 20
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='recursos-perdidos.pdf')

def sob_relatores(request: HttpRequest):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=portrait(letter))
    w, h = portrait(letter)
    p.drawString(10,h - 30, "TODO!")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='sob-relatores.pdf')

def sob_distancia(request: HttpRequest):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=portrait(letter))
    w, h = portrait(letter)
    p.drawString(10,h - 30, "TODO!")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='sob-distancia.pdf')

def sob_pontos(request: HttpRequest):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=portrait(letter))
    w, h = portrait(letter)
    p.drawString(10,h - 30, "TODO!")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='sob-pontos.pdf')
