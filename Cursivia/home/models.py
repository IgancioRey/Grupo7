from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime, string
from django.http import HttpResponseRedirect
from django.urls import reverse 

# Create your models here.
class Carrera (models.Model):
    descripcion = models.CharField(max_length=50, null=False, blank=False, default='') 
    cant_años = models.IntegerField(null=True, blank=True, default=0)
    def __str__(self):
        return self.descripcion

    def id(self):
        """
        Devuelve el URL a una instancia particular de la publicacion
        """
        return self.id

    def get_absolute_url(self): 
        return reverse('foro-carrera', args=[str(self.id)])

class Materia (models.Model):
    descripcion = models.CharField(max_length=50, null=False, blank=False, default='')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, null=False, blank=False,default='')
    año = models.IntegerField(default=0)
    def __str__(self):
        return self.descripcion  


class Usuario(models.Model):
    """
    Modelo que representa datos del usuario
    """
    estadoUsuario = (
        ('p', 'Pendiente de activación'),
        ('a', 'Activo'),
        ('s', 'Suspendido'),
        ('e', 'Eliminado'),
    )
    tipoUsuario = (
        ('a', 'Administrador'),
        ('e', 'Estudiante'),
    ) 

    nombre = models.CharField(max_length=50, null=False, blank=False, default='')
    apellido = models.CharField(max_length=50, null=False, blank=False, default='')
    eMail = models.EmailField()
    usuario = models.OneToOneField(User,on_delete = models.CASCADE, null=True, blank=True)
    fechaNacimiento = models.DateField(null=True, blank=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, null=True, blank=True)
    localidad = models.CharField(max_length=50, null=True, blank=True)
    fechaAlta = models.DateField(null=False, blank=False, auto_now_add=True)
    fechaBaja = models.DateField(null=True, blank=True)
    tipo = models.CharField(max_length=1, choices=tipoUsuario, blank=True, default='e',
                              help_text='tipo de usuario')
    estado = models.CharField(max_length=1, choices=estadoUsuario, blank=True, default='p',
                              help_text='estado actual del usuario')
    tokenActivacion = models.CharField(max_length = 40, blank = True, null = True)

    def __str__(self):
        return self.usuario.username

class Publicacion(models.Model):
    """
    Modelo que representa una publicacion, tanto noticia como documento.
    """
    estadosCargados = (
        ('p', 'Publicado'),
        ('b', 'Borrador'),
        ('d', 'Denunciado'),
        ('e', 'Eliminado'),
    )
    alcances = (
        ('g', 'Global'),
        ('e', 'Expecifico'),
    )
    tipoPublicacion = (
        ('n', 'Noticia'),
        ('d', 'Documentacion'),
        ('f', 'Foro'),
    )
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, null=True, blank=True, default='')
    titulo = models.CharField(max_length=100)
    cuerpo = models.TextField(max_length=5000)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    fecha_alta = models.DateTimeField(default=timezone.now, null=True)
    fecha_baja = models.DateTimeField(null=True, blank=True)
    tipo_publicacion =  models.CharField(max_length=1, choices=tipoPublicacion, blank=True, default='d',
                              help_text='tipo de publicacion')
    estado_publicacion = models.CharField(max_length=1, choices=estadosCargados, blank=True, default='b',
                              help_text='situacion actual de la publicacion')
    alcance = models.CharField(max_length=1, choices=alcances, blank=True, default='g',
                              help_text='alcance de la publicacion')
    aprovacion = models.IntegerField(null=True, blank=True, default=0)
    denuncias = models.IntegerField(null=True, blank=True, default=0)
    image = models.ImageField(upload_to='images/', null=True, blank=True, default='#')

    def __str__(self):
        return self.titulo

    def display_materia(self):
        """
        Esto se requiere para ser mostrada la carrera en el admin
        """
        return ', '.join([materia.descripcion for materia in self.materia.all()[:3]])

        display_materia.short_description = 'Materia'

    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de la publicacion
        """
        return reverse('publicacion-detail', args=[str(self.id)])
    
    def get_aboslute_url_modificar(self): 
        return reverse ('noticia_update', args=[str(self.id)])

    def cambiar_estado_eliminado(self): 
        return reverse ('noticia_delete', args=[str(self.id)])

    def __unicode__(self,):
        return str(self.image)


class Comentario(models.Model):
    """
    Modelo que representa una publicacion, tanto noticia como documento.
    """
    estadosCargados = (
        ('p', 'Publicado'),
        ('b', 'Borrador'),
        ('d', 'Denunciado'),
        ('e', 'Eliminado'),
    )

    comentario = models.CharField(max_length=1000)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, null=True, blank=True)
    fecha_alta = models.DateTimeField(default=timezone.now, null=True)
    fecha_baja = models.DateTimeField(null=True)
    motivo_baja = models.CharField(max_length=200)
    estado_comentario = models.CharField(max_length=1, choices=estadosCargados, blank=True, default='b',
                              help_text='situacion actual del comentario')

    def __str__(self):
        return self.comentario