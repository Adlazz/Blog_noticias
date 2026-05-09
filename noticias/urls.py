from django.urls import path
from . import views
from .feeds import UltimasNoticiasFeed

urlpatterns = [
    path('', views.home, name='home'),
    path('noticias/', views.lista_noticias, name='lista_noticias'),
    path('noticias/<slug:slug>/', views.detalle_noticia, name='detalle_noticia'),
    path('categoria/<slug:slug>/', views.categoria, name='categoria'),
    path('archivo/<int:anio>/<int:mes>/', views.noticias_por_fecha, name='noticias_por_fecha'),
    path('buscar/', views.buscar, name='buscar'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
    path('feed/', UltimasNoticiasFeed(), name='feed'),
]
