from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Pregunta

def inicio(request):
    ultima_lista_preguntas = Pregunta.objects.order_by('-fecha_publicacion')[:5]
    contexto = {'ultima_lista_preguntas': ultima_lista_preguntas}
    return render(request, 'polls/indice.html', contexto)

def detalle(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, 'polls/detalle.html', {'Pregunta': Pregunta})

def resultados(request, pregunta_id):
    response = "Estas viendo los resultados de la pregunta %s."
    return HttpResponse(response % pregunta_id)

def voto(request, pregunta_id):
    return HttpResponse("Estás votando por la pregunta %s." % pregunta_id)
