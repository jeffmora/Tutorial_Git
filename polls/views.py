from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Pregunta, Eleccion

class iniciovista(generic.ListView):
    template_name = 'polls/indice.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Devuelva las últimas cinco preguntas publicadas."""
        return Pregunta.objects.order_by('-fecha_publicacion')[:5]

class detallevista(generic.DetailView):
    model = Pregunta
    template_name = 'polls/detalle.html'

class resultadosvista(generic.DetailView):
    model = Pregunta
    template_name = 'polls/resultados.html'

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
