from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logoff/', views.logoff, name='logoff'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),

    path('sobrevivente/', views.sobrevivente, name='sobrevivente'),
    path('posicao/', views.posicao, name='posicao'),
    path('relato/<int:relatado>/', views.relato, name='relato'),

    path('sobreviventes/', views.sobreviventes, name='sobreviventes'),
    path('itens/', views.itens, name='itens'),
    path('relatos/', views.relatos, name='relatos'),
]