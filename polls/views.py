from django.shortcuts import render
from django.http import HttpResponse


def inicio(request):
    return HttpResponse("Hola mundo, Está es la aplicación inicial de encuestas.")
# Create your views here.
