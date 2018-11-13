from django.contrib import admin
from .models import Publicacion, Comentario, Carrera, Materia, Denuncia, MeGusta, Evento, Usuario, GroupInvitation, Estado_Grupo
from rest_framework.authtoken.admin import TokenAdmin
# Register your models here.
admin.site.register(Carrera)
admin.site.register(Materia)
admin.site.register(Publicacion)
admin.site.register(Comentario)
admin.site.register(Denuncia)
admin.site.register(MeGusta)
admin.site.register(Usuario)
admin.site.register(GroupInvitation)
admin.site.register(Estado_Grupo)
admin.site.register(Evento)
TokenAdmin.raw_id_fields = ('user',)


