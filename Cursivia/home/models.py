from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.utils import timezone
import datetime, string
from django.http import HttpResponseRedirect
from django.urls import reverse 
from django.conf import settings
import re

# Create your models here.
class Carrera (models.Model):
    descripcion = models.CharField(max_length=50, null=False, blank=False, default='') 
    cant_años = models.IntegerField(null=True, blank=True, default=0)
    def __str__(self):
        return self.descripcion

    def id(self): 
        return self.id

    def get_absolute_url(self): 
        return reverse('foro-carrera', args=[str(self.id)])

class Materia (models.Model):
    descripcion = models.CharField(max_length=50, null=False, blank=False, default='')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, null=False, blank=False,default='')
    año = models.IntegerField(default=0)

    def get_absolute_url(self): 
        return reverse('foro_materia', args=[str(self.id)])

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
    descripcion = models.CharField(max_length=200, null=True, blank=True, default='')
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
        ('g', 'Grupo')
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
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, default='')

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
        if self.tipo_publicacion == 'n':
            url = 'publicacion-detalle'
        elif self.tipo_publicacion == 'f':
            url = 'tema-detail'

        return reverse(url, args=[str(self.id)])
    
    def get_aboslute_url_modificar(self): 
        return reverse ('noticia_update', args=[str(self.id)])

    def cambiar_estado_eliminado(self): 
        return reverse ('noticia_delete', args=[str(self.id)])

    def __unicode__(self,):
        return str(self.image)

    def get_aboslute_url_usuario_autor(self):
        return reverse ('perfil_usuario', args=[str(self.usuario.id)])



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


    def get_aboslute_url_usuario_autor(self):
        return reverse ('perfil_usuario', args=[str(self.usuario.id)])

class Denuncia(models.Model):
    """
    Modelo que representa una publicacion, tanto noticia como documento.
    """

    comentario = models.CharField(max_length=1000, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, null=True, blank=True)
    fecha_alta = models.DateTimeField(default=timezone.now, null=True)
    fecha_baja = models.DateTimeField(null=True, blank=True)
    motivo_baja = models.CharField(max_length=200, null=True, blank=True)
    usuarioDenunciado = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    grupoDenunciado = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

   
    def __str__(self):
        return self.comentario


class MeGusta(models.Model):
    """
    Modelo que representa una publicacion, tanto noticia como documento.
    """

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    fecha_alta = models.DateTimeField(default=timezone.now, null=True)
   
    def __str__(self):
        return self.usuario.username


"""
GRUPOS
"""

MIN_GROUPNAME_LENGTH = 5

class GroupError(Exception):
    def __init__(self, message):
        self.message = message


class GroupProperties(models.Model):
    group = models.OneToOneField(Group, related_name='properties', on_delete=models.CASCADE)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL,
            related_name='admin_of')
    public_members = models.BooleanField(default=False)

class GroupProxy(object):
    def __init__(self, group):
        self.group = group

    def add_member(self, user):
        group = self.group
        group.user_set.add(user)

    def remove_member(self, user, check_sole_admin=False):
            properties = self.group.properties
            if check_sole_admin:
                self._raise_if_sole_admin(user)
            properties.admins.remove(user)
            self.group.user_set.remove(user)
    
    def grant_admin(self, user):
        self.group.properties.admins.add(user)

    def revoke_admin(self, user):
        self._raise_if_sole_admin(user)
        self.group.properties.admins.remove(user)

    def is_admin(self, user):
        return bool(self.group.properties.admins.filter(pk=user.pk).count())

    def is_member(self, user):
        return bool(self.group.user_set.filter(pk=user.pk).count())

    def _raise_if_sole_admin(self, user):
        properties = self.group.properties
        if self.is_admin(user):
            num_admins = properties.admins.count()
            if num_admins == 1:
                msg = ('You are the sole group admin. Please terminate the group or appoint another group admin.')
                raise GroupError(msg)


class GroupInvitation(models.Model):
    date_invited = models.DateTimeField(default=timezone.now)
    group = models.ForeignKey(Group, related_name='invitations', on_delete=models.CASCADE)
    invitee = models.ForeignKey(settings.AUTH_USER_MODEL,
            related_name='invitations', on_delete=models.CASCADE)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL,
            related_name='given_invitations', on_delete=models.CASCADE)

    def __unicode__(self):
        return u'Invitation to {0} for {1}'.format(self.group, self.invitee)

    def accept(self):
        group_proxy = GroupProxy(self.group)
        group_proxy.add_member(self.invitee)
        self.delete()

    def refuse(self):
        self.delete()

_group_name_re = re.compile(r'^[a-zA-Z]([a-zA-Z0-9-]*)$')
def create_usergroup(user, name):

    if len(name) < 5:
        err_msg = ('El nombre del grupo debe tener 5 caracteres como mínimo')
        raise GroupError(err_msg)
    
    if Group.objects.filter(name__iexact=name).count():
        raise GroupError(('El grupo ya existe'))
    
    group = Group.objects.create(name=name)

    group_proxy = GroupProxy(group)
    group_proxy.add_member(user)

    group.properties.admins.add(user)

    return group


def _change_group_cb(sender, instance, created, **kwargs):
    if created:
        props = GroupProperties.objects.create(group=instance)
        instance.properties = props

post_save.connect(_change_group_cb, sender=Group)

class Estado_Grupo(models.Model):
    estadosCargados = (
        ('p', 'Publicado'),
        ('b', 'Borrador'),
        ('d', 'Denunciado'),
        ('e', 'Eliminado'),
    )

    grupo = models.ForeignKey(Group, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    estado = models.CharField(max_length=1, choices=estadosCargados, blank=True, default='b',
        help_text='situacion actual de la publicacion')

    def __str__(self):
        return self.estado

class Evento(models.Model):
    
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE)
    usuarioCreador = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    titulo = models.CharField(max_length=100)
    cuerpo = models.TextField(max_length=200)
    fecha_evento = models.DateTimeField(default=timezone.now, null=True)
    lugarEvento = models.CharField(max_length=100)
    
    def __str__(self):
        return self.titulo

class PersonaEvento(models.Model):
    
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)

    
    def __str__(self):
        return self.usuario.username
