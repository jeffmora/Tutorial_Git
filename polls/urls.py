from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.iniciovista.as_view(), name='inicio'),
    path('<int:pk>/', views.detallevista.as_view(), name='detalle'),
    path('<int:pk>/resultados/', views.resultadosvista.as_view(), name='resultados'),
    path('<int:pregunta_id>/voto/', views.voto, name='voto'),
]