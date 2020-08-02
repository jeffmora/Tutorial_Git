from django.test import TestCase

# Create your tests here.
import datetime
from django.utils import timezone
from django.urls import reverse
from .models import Pregunta

class ModeloPreguntaTest(TestCase):

    def test_fue_publicado_recientemente_con_pregunta_futura(self):
        """
        fue_publicada_recientemente() devuleve False para preguntas cuya fecha_publicacion es en el futuro.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Pregunta(fecha_publicacion=time)
        self.assertIs(future_question.fue_publicado_recientemente(), False)

    def test_fue_publicado_recientemente_con_pregunta_antigua(self):
        """
        fue_publicada_recientemente() devuleve False para preguntas cuya fecha_publicacion es pasada a 1 día.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Pregunta(fecha_publicacion=time)
        self.assertIs(old_question.fue_publicado_recientemente(), False)

    def test_fue_publicado_recientemente_con_pregunta_actual(self):
        """
        fue_publicada_recientemente() devuelve True para preguntas cuya fecha_publicacion se encuentra dentro del último día.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Pregunta(fecha_publicacion=time)
        self.assertIs(recent_question.fue_publicado_recientemente(), True)

def create_question(texto_pregunta_test, dias):
    """
    Cree una pregunta con el 'texto_pregunta_test' dado y publique el número dado de 'dias' offset hasta ahora (negativo para preguntas publicadas en el pasado,
    positivo para preguntas que aún no se han publicado).
    """
    time = timezone.now() + datetime.timedelta(days=dias)
    return Pregunta.objects.create(texto_pregunta=texto_pregunta_test, fecha_publicacion=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        Si no existen preguntas, se muestra un mensaje apropiado.
        """
        response = self.client.get(reverse('polls:inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay encuestas disponibles.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Las preguntas con fecha_publicación en el pasado se muestran en la página de índice.
        """
        create_question(texto_pregunta_test="Pregunta pasada.", dias=-30)
        response = self.client.get(reverse('polls:inicio'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Pregunta: Pregunta pasada.>']
        )

    def test_future_question(self):
        """
        Las preguntas con una fecha de publicación en el futuro no se muestran en la página de índice.
        """
        create_question(texto_pregunta_test="Pregunta futura.", dias=30)
        response = self.client.get(reverse('polls:inicio'))
        self.assertContains(response, "No hay encuestas disponibles.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Incluso si existen preguntas pasadas y futuras, solo se muestran las preguntas pasadas.
        """
        create_question(texto_pregunta_test="Pregunta pasada.", dias=-30)
        create_question(texto_pregunta_test="Pregunta futura.", dias=30)
        response = self.client.get(reverse('polls:inicio'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Pregunta: Pregunta pasada.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(texto_pregunta_test="Pregunta pasada 1.", dias=-30)
        create_question(texto_pregunta_test="Pregunta pasada 2.", dias=-5)
        response = self.client.get(reverse('polls:inicio'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Pregunta: Pregunta pasada 2.>', '<Pregunta: Pregunta pasada 1.>']
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        La vista detallada de una pregunta con fecha_publicacion en el futuro devuelve un 404 no encontrado.
        """
        future_question = create_question(texto_pregunta_test="Pregunta futura.", dias=5)
        url = reverse('polls:detalle', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        La vista detallada de una pregunta con fecha_publicacion en el pasado muestra el texto de la pregunta.
        """
        past_question = create_question(texto_pregunta_test="Pregunta pasada.", dias=-5)
        url = reverse('polls:detalle', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.texto_pregunta)