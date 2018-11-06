from rest_framework import serializers
from home.models import Publicacion, Carrera, Materia, Usuario

class NoticiaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Publicacion
        fields = ('url', 'titulo', 'cuerpo', 'fecha_alta', 'aprovacion', 'tipo_publicacion')

class CarrerasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Carrera
        fields = ('descripcion','cant_años')

class MateriasSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
	    model = Materia
	    fields = ('descripcion','carrera', 'año')

class UsuariosSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
	    model = Usuario
	    fields = ('nombre', 'eMail', 'tipo', 'estado')

