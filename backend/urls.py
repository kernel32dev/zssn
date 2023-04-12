from django.urls import path

from . import views

urlpatterns = [
    path('sobrevivente/<int:id>', views.sobrevivente, name='sobrevivente'),
    path('sobrevivente', views.sobrevivente, name='sobrevivente'),
    path('relato', views.relato, name='relato'),
    path('item', views.item, name='item'),
]