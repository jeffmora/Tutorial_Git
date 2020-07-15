from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('<int:pregunta_id>/', views.detalle, name='detalle'),
    path('<int:pregunta_id>/resultados/', views.resultados, name='resultados'),
    path('<int:pregunta_id>/voto/', views.voto, name='voto'),
]