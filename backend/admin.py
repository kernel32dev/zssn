from django.contrib import admin

from .models import Sobrevivente, Relato, ItemComercial, Inventario

admin.site.register(Sobrevivente)
admin.site.register(Relato)
admin.site.register(ItemComercial)
admin.site.register(Inventario)
