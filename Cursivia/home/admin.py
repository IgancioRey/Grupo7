from django.contrib import admin
from .models import Publicacion, Comentario, Carrera, Materia

# Register your models here.
admin.site.register(Carrera)
admin.site.register(Materia)
admin.site.register(Publicacion)
admin.site.register(Comentario)