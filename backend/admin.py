from django.contrib import admin

from .models import Sobrevivente, Relato, ItemComercial, Inventario, Sessao, Oferta, OfertaItem

admin.site.register(Sobrevivente)
admin.site.register(Relato)
admin.site.register(ItemComercial)
admin.site.register(Inventario)
admin.site.register(Sessao)
admin.site.register(Oferta)
admin.site.register(OfertaItem)
