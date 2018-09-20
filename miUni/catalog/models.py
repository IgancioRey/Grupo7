from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid # Requerida para las instancias de libros únicos
# Create your models here.

class Genre(models.Model):
    """
    Modelo que representa un género de la publicacion (p. ej. urgente, noticia, notificacion de cambio).
    """
    name = models.CharField(max_length=200, help_text="Ingresar un género para la publicacion (e.g. Urgente, Noticia, Notificacion, etc.)")

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej en el sitio de Administración)
        """
        return self.name

class Publicacion(models.Model):
    """
    Modelo que representa una publicacion (pero no de una específica).
    """
    #El ID hay que sacarlo, se genera solo, sino es complicado para pasarselo como parametro, si se genera solo es un numero autoincremental, si lo generamos en una convinacion de numeros, letras y simbolos
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    title = models.CharField(max_length=200)
    # ForeignKey, ya que una publicacion tiene un solo autor, pero el mismo autor puede haber escrito muchas publicaciones.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.
    ##author = models.ForeignKey('Author', on_delete=models.SET_NULL) --> FALTA VER ESO
    summary = models.CharField(max_length=200, help_text="Ingrese una descripcion breve de la publicacion", null = False)
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Seleccione el genero de esta publiacion")
    # ManyToManyField, porque un género puede contener muchas publicaciones y una publicacion puede cubrir varios géneros.
    # La clase Genre ya ha sido definida, entonces podemos especificar el objeto arriba.
    text = models.TextField(max_length=2000, help_text="Ingrese la noticia breve de la publicacion")
    createDate= models.DateField(null=True, blank=True)
    postDate= models.DateField(null=True, blank=True)

    POST_STATUS = (
        ('b', 'Borrador'),
        ('e', 'Eliminado'),
        ('d', 'Denunciado'),
        ('p', 'Publicado'),
    )
    status = models.CharField(max_length=1, choices=POST_STATUS, default='b', help_text='Estado dela publicacion')

    class Meta:
        ordering = ["title", "-postDate"]

    def __str__(self):
        """
        String que representa al objeto Publicacion
        """
        return self.title

    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Publicavion
        """
        return reverse('publicacion-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'

class Documentacion(models.Model):
    title = models.CharField(max_length=200)
    # ForeignKey, ya que una publicacion tiene un solo autor, pero el mismo autor puede haber escrito muchas publicaciones.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.
    ##author = models.ForeignKey('Author', on_delete=models.SET_NULL) --> FALTA VER ESO
    summary = models.CharField(max_length=200, help_text="Ingrese una descripcion breve de la docuemntacion", null = False)
    # ManyToManyField, porque un género puede contener muchas publicaciones y una publicacion puede cubrir varios géneros.
    # La clase Genre ya ha sido definida, entonces podemos especificar el objeto arriba.
    text = models.TextField(max_length=2000, help_text="Ingrese informacion de la documentacion")
    createDate= models.DateField(null=True, blank=True)

    DOCUMENTACION_STATUS = (
        ('g', 'General'),
        ('e', 'Indivual por carrera'),
    )
    status = models.CharField(max_length=1, choices=DOCUMENTACION_STATUS, default='g', help_text='Tipo de documentacion')

    class Meta:
        ordering = ["title", "-createDate"]

        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """
        String que representa al objeto Publicacion
        """
        return self.title


    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Publicavion
        """
        return reverse('documentacion-detail', args=[str(self.id)])