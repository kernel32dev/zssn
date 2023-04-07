from django.shortcuts import render
from django.http import HttpResponse
from .models import Ticket

def index(request):
    body = "Tickets no sistema:<br>"
    count = 0
    for ticket in Ticket.objects.all():
        count += 1
        body += ticket.name + "<br>"
    if count == 1:
        body += "1 item"
    else:
        body += f"{count} itens"
    return HttpResponse(body)
