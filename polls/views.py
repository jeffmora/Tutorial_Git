from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Pregunta, Eleccion

def inicio(request):
    ultima_lista_preguntas = Pregunta.objects.order_by('-fecha_publicacion')[:5]
    contexto = {'ultima_lista_preguntas': ultima_lista_preguntas}
    return render(request, 'polls/indice.html', contexto)

def detalle(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, 'polls/detalle.html', {'pregunta': pregunta})

def resultados(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, 'polls/resultados.html', {'pregunta': pregunta})

def voto(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    try:
        eleccion_elegida = pregunta.eleccion_set.get(pk=request.POST['eleccion'])
    except (KeyError, Eleccion.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detalle.html', {
            'pregunta': pregunta,
            'mensaje_error': "No seleccionaste una opción.",
        })
    else:
        eleccion_elegida.votos += 1
        eleccion_elegida.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:resultados', args=(pregunta.id,)))
