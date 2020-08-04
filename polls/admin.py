from django.contrib import admin
from .models import Pregunta, Eleccion

# Register your models here.
class EleccionInline(admin.TabularInline):
    model = Eleccion
    extra = 3

class PreguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['texto_pregunta']}),
        ('Infomación de fecha', {'fields': ['fecha_publicacion'], 'classes': ['collapse']}),
    ]
    inlines = [EleccionInline]
    list_display = ('texto_pregunta', 'fecha_publicacion', 'fue_publicado_recientemente')
    list_filter = ['fecha_publicacion']
    search_fields = ['texto_pregunta']

admin.site.register(Pregunta, PreguntaAdmin)