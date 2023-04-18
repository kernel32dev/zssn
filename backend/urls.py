from django.urls import path

from . import views
from . import rel

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logoff/', views.logoff, name='logoff'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),

    path('sobrevivente/', views.sobrevivente, name='sobrevivente'),
    path('posicao/', views.posicao, name='posicao'),
    path('relato/<int:relatado>/', views.relato, name='relato'),
    path('compra/<int:oferta>/', views.compra, name='compra'),

    path('rel/infeccoes/', rel.infeccoes, name='infeccoes'),
    path('rel/recursos/', rel.recursos, name='recursos'),
    path('rel/recursos-perdidos/', rel.recursos_perdidos, name='recursos_perdidos'),
    path('rel/sob-relatores/', rel.sob_relatores, name='sob_relatores'),
    path('rel/sob-distancia/', rel.sob_distancia, name='sob_sistancia'),
    path('rel/sob-pontos/', rel.sob_pontos, name='sob_pontos'),

    path('sobreviventes/', views.sobreviventes, name='sobreviventes'),
    path('itens/', views.itens, name='itens'),
    path('relatos/', views.relatos, name='relatos'),
    path('ofertas/', views.ofertas, name='ofertas'),
]