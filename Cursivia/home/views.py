from urllib.parse import quote_plus
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Publicacion, Carrera, Materia, Usuario, Comentario, Denuncia, MeGusta, Evento, PersonaEvento
#from .models import GroupInvitation, GroupProxy, GroupError, create_usergroup 
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from .forms import *
import random
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json  
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from Cursivia.serializers import tokenSerializer, meGustaSerializer, UserSerializer, NoticiaSerializer, CarrerasSerializer, MateriasSerializer, UsuariosSerializer, ComentariosSerializer

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import datetime


def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    lista_noticias = Publicacion.objects.all().filter(tipo_publicacion__exact='n', estado_publicacion__exact='p').order_by('-fecha_alta')
    
    #CREE NUEVA LISTA
    lista_noticias_completa =[]
    for l in lista_noticias: 
        lista_noticias_completa.append([l,Comentario.objects.all().filter(publicacion__exact=l, estado_comentario__exact='p').count()])
    #HASTA ACA

    #LA ASIGNE AL PAGINADO
    paginator = Paginator(lista_noticias_completa, 5) # Show 25 contacts per page
    #HASTA ACA

    page = request.GET.get('page')
    noticias = paginator.get_page(page)

    lista_carreras = Carrera.objects.all() 
    materiasC =[]
    for l in lista_carreras: 
        materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])


    return render(request, 'index.html', {'noticias': noticias, 'lista_carreras': lista_carreras, 'lista_cantMaterias': materiasC})
  

class noticiaDetailForm(FormMixin,generic.DetailView):
    template_name='home/publicacion_detail.html'
    model = Publicacion
    form_class = formNoticia


    lista_carreras = Carrera.objects.all() 

    def get_success_url(self):
        return reverse('publicacion-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(noticiaDetailForm, self).get_context_data(**kwargs)
        context['form'] = formNoticia(initial={'post': self.object})
        return context

    def menuCarreras(self):
        lista_carreras = Carrera.objects.all() 
        materiasC =[]
        for l in lista_carreras:
            materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])
        return materiasC

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(noticiaDetailForm, self).form_valid(form)

    def get_comentarios(self):
        noticia = get_object_or_404(Publicacion, id = self.object.id )    
        lista_comentario = Comentario.objects.all().filter(publicacion= noticia, estado_comentario= 'p')
        return lista_comentario
    
    def get_megusta(self):
        noticia = get_object_or_404(Publicacion, id =   self.object.id )  
        lista_meGusta = MeGusta.objects.all().filter(publicacion= noticia)
        
        lista_meGusta_usuario =[]
        for l in lista_meGusta:
            lista_meGusta_usuario.append(l.usuario.id)

        return lista_meGusta_usuario

class publicacionDetailForm(FormMixin,generic.DetailView):
    template_name='home/tema_detail.html'
    model = Publicacion
    form_class = formNoticia


    lista_carreras = Carrera.objects.all() 

    def get_success_url(self):
        return reverse('tema-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(publicacionDetailForm, self).get_context_data(**kwargs)
        context['form'] = formNoticia(initial={'post': self.object})
        return context

    def menuCarreras(self):
        lista_carreras = Carrera.objects.all() 
        materiasC =[]
        for l in lista_carreras:
            materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])
        return materiasC

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(publicacionDetailForm, self).form_valid(form)

    def get_comentarios(self):
        publicacion = get_object_or_404(Publicacion, id = self.object.id )    
        lista_comentario = Comentario.objects.all().filter(publicacion= publicacion, estado_comentario= 'p')
        return lista_comentario
    
    def get_megusta(self):
        publicacion = get_object_or_404(Publicacion, id =   self.object.id )  
        lista_meGusta = MeGusta.objects.all().filter(publicacion= publicacion)
        
        lista_meGusta_usuario =[]
        for l in lista_meGusta:
            lista_meGusta_usuario.append(l.usuario.id)

        return lista_meGusta_usuario

class PublicacionCreate(LoginRequiredMixin, CreateView):
    model = Publicacion
    fields = ['estado_publicacion']
    
    def dispatch(self, request, *args, **kwargs):
        """
        Overridden so we can make sure the `Ipsum` instance exists
        before going any further.
        """
        self.materia = get_object_or_404(Materia, pk=kwargs['pkM'])
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  
        titulo = request.POST['titulo']
        cuerpo = request.POST['cuerpo']
        usuario = request.user
        materia = self.materia
        tipo_publicacion =  'f'
        estado_publicacion = request.POST['estado_publicacion']

        try:
            image = request.FILES['image']
            noticia = Publicacion(image = image, titulo= titulo, cuerpo= cuerpo, tipo_publicacion= tipo_publicacion, estado_publicacion= estado_publicacion, usuario= usuario, materia = materia )
        except Exception as e:
            noticia = Publicacion(titulo= titulo, cuerpo= cuerpo, tipo_publicacion= tipo_publicacion, estado_publicacion= estado_publicacion, usuario= usuario, materia = materia )
            print (e)

        noticia.save()
        prueba = get_object_or_404(Publicacion, pk=noticia.id)
        return render(request, 'home/tema_detail.html', {'object': prueba})
    
    def menuCarreras(self):
        lista_carreras = Carrera.objects.all() 
        materiasC =[]
        for l in lista_carreras:
            materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])
        return materiasC
    
    def usuarioNoLogueado():
        login_url = '/accounts/login/'
        redirect_field_name = 'redirect_to'


def registracion(request):
    if request.method=='POST':
        form = formRegistracion(request.POST)
        if not User.objects.filter(username=request.POST['nombreUsuario']).exists():
            if not User.objects.filter(email=request.POST['email']).exists():
                if request.POST['password'] == request.POST['confpassword']:
                    nombreUsuario        = request.POST['nombreUsuario']
                    nombre          = request.POST['nombre']
                    apellido        = request.POST['apellido']
                    email           = request.POST['email']
                    password        = request.POST['password']
                    user            = User.objects.create_user(username=nombreUsuario, email=email, password=password, first_name=nombre, last_name=apellido)
                    user.is_active  = False                    
                  
                    N               = 20
                    token           = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
                    usuario         = Usuario(usuario = user, tokenActivacion = token, nombre = nombre, apellido= apellido, eMail=email)

                    email_subject   = 'Bienvenido a Cursivia - Activación de usuario'
                    email_body      = " Hola %s, se ha registrado una cuenta con el correo %s. Para activarla has clic en el siguiente link: https://cursivia.herokuapp.com/home/bienvenido/%s " % (nombre, email, token)
                    
                    send_mail(email_subject,email_body, 'cursiviaweb@gmail.com',[email] )

                    user.save()
                    usuario.save()

                    return HttpResponseRedirect("/home/confirmacion/")
                else:
                    messages.error(request, "Las contraseñas no coinciden")
            else:
                messages.error(request, "El eMail ya pose una cuenta asociada")
        else:
            messages.error(request, "Usuario no disponible")
    else:
        form = formRegistracion()
    return render(request,'registration/registracion.html', { 'form': form })


def bienvenido(request, tokenActivacion):
    usuario  = get_object_or_404(Usuario, tokenActivacion = tokenActivacion )    
    user            = usuario.usuario
    usuario.estado = 'a'
    user.is_active  = True
    usuario.save()
    user.save()
    return render(
        request, 
        'registration/bienvenido.html',
        context={'nombre_usuario': user.first_name},
        )


def confirmacion(request):
    return render(request, 'registration/confirmacion.html')

def configuracionCuenta(request):
    return render(request, 'cuenta/configuracionCuenta.html')

def logout_view(request):
    return render(request, 'index.html')

"""
@login_required(login_url= '/accounts/login/')
def nuevaNoticia(request):
    if request.method=='POST':
        form                = formNoticia(request.POST)
        
        titulo              = request.POST['titulo']
        cuerpo              = request.POST['cuerpo']
        usuario             = request.user
        fecha_alta          = datetime.date.today()
        estado_publicacion  = request.POST['estado_publicacion']

        if form.is_valid():
            formNoticia     = form.save(commit = False) 
            formNoticia.save()

        return HttpResponseRedirect("/noticiaD/", 1) 
    else:
        form = formRegistracion()
    return render(request,'home/nueva_noticia.html', { 'form': form })
"""
class NoticiaCreate(LoginRequiredMixin, CreateView):
    model = Publicacion
    fields = ['estado_publicacion']

    def post(self, request, *args, **kwargs):
        print ('pasa por aca')        
        titulo = request.POST['titulo']
        cuerpo = request.POST['cuerpo']
        usuario = request.user
        tipo_publicacion =  'n'
        estado_publicacion = request.POST['estado_publicacion']

        try:
            image = request.FILES['image']
            noticia = Publicacion(image = image, titulo= titulo, cuerpo= cuerpo, tipo_publicacion= tipo_publicacion, estado_publicacion= estado_publicacion, usuario= usuario )
        except Exception as e:
            noticia = Publicacion(titulo= titulo, cuerpo= cuerpo, tipo_publicacion= tipo_publicacion, estado_publicacion= estado_publicacion, usuario= usuario )
            print (e)

        noticia.save()
        prueba = get_object_or_404(Publicacion, pk=noticia.id)
        return render(request, 'home/publicacion_detail.html', {'object': prueba})
    
    def menuCarreras(self):
        lista_carreras = Carrera.objects.all() 
        materiasC =[]
        for l in lista_carreras:
            materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])
        return materiasC
    
    def usuarioNoLogueado():
        login_url = '/accounts/login/'
        redirect_field_name = 'redirect_to'
        
    
class NoticiaUpdate(LoginRequiredMixin, UpdateView):
    model = Publicacion
    fields = ['titulo','cuerpo','estado_publicacion', 'image']

    def menuCarreras(self):
        lista_carreras = Carrera.objects.all() 
        materiasC =[]
        for l in lista_carreras:
            materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])
        return materiasC

    def usuarioNoLogueado():
        login_url = '/accounts/login/'
        redirect_field_name = 'redirect_to'


@login_required(login_url= '/accounts/login/')
def NoticiaDelete(request, pk):
    noticia = get_object_or_404(Publicacion, id = pk )    
    noticia.estado_publicacion = 'e'
    noticia.fecha_baja = timezone.now()
    noticia.save()
    return redirect('/')

@csrf_exempt
def ForoGeneral(request):
    if request.method=='POST':

        cuerpo = request.POST['cuerpo']
        usuario = request.user
        fecha_alta = timezone.now()
        estado_publicacion = 'p'
        tipo_publicacion = 'f'
        titulo = "Publicacion - Foro"
        if (cuerpo == ''):
            print("Tendriamos que tirar mensaje")        
        else:
            publicacion = Publicacion(titulo = titulo, tipo_publicacion = tipo_publicacion, cuerpo= cuerpo, estado_publicacion= estado_publicacion, usuario= usuario )
            publicacion.save()
        

    lista_publicaciones = Publicacion.objects.all().filter(tipo_publicacion__exact='f', estado_publicacion__exact='p', materia__exact=None).order_by('-fecha_alta')
    lista_carreras = Carrera.objects.all() 


    lista_publicaciones_comentarios=[]
    for l in lista_publicaciones: 
        lista_meGusta = MeGusta.objects.all().filter(publicacion= l)
        lista_meGusta_usuario =[]
        for lista in lista_meGusta:
            lista_meGusta_usuario.append(lista.usuario.id)

        lista_publicaciones_comentarios.append([l,Comentario.objects.all().filter(publicacion__exact=l, estado_comentario__exact='p').order_by('fecha_alta'), lista_meGusta_usuario])


    materiasC =[]
    for l in lista_carreras:
        materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])


    return render(request, 'home/foro_general.html', {'lista_publicaciones': lista_publicaciones_comentarios, 'lista_carreras': lista_carreras, 'lista_cantMaterias': materiasC})



class ForoCarreraForm(FormMixin,generic.DetailView):
    template_name='home/foro_carrera.html'
    model = Carrera
    form_class = formCarrera

    def get_success_url(self):
        return reverse('foro_carrera', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ForoCarreraForm, self).get_context_data(**kwargs)
        context['form'] = formCarrera(initial={'post': self.object})
        return context

    def menuCarreras(self):
        lista_carreras = Carrera.objects.all() 
        materiasC =[]
        for l in lista_carreras:
            materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])
        return materiasC


    def materias(self): 
        carrera = get_object_or_404(Carrera, id = self.object.id )  
        materiasA =[]
        for l in range(1,carrera.cant_años+1):
            materiasA.append([l,Materia.objects.all().filter(carrera=carrera, año=l)])
        return materiasA


class ForoMateriaForm(FormMixin,generic.DetailView):
    template_name='home/foro_materia.html'
    model = Materia
    form_class = formMateria

    def get_success_url(self):
        return reverse('foro_materia', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(ForoMateriaForm, self).get_context_data(**kwargs)
        context['form'] = formMateria(initial={'post': self.object})
        return context

    def menuCarreras(self):
        lista_carreras = Carrera.objects.all() 
        materiasC =[]
        for l in lista_carreras:
            materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])
        return materiasC

    def publicaciones(self): 
        materia = get_object_or_404(Materia, id = self.object.id )

        lista_publicaciones = Publicacion.objects.all().filter(tipo_publicacion__exact='f', estado_publicacion__exact='p', materia=materia).order_by('-fecha_alta')
        paginator = Paginator(lista_publicaciones, 5) # Show 25 contacts per page

        page = self.request.GET.get('page')
        publicaciones = paginator.get_page(page)

        return publicaciones


def ForoGeneralComentarios (request, pk):
    foro = get_object_or_404(Publicacion, id = pk )    

    lista_comentario = Comentario.objects.all().filter(publicacion= foro)
    print (lista_comentario) 


@csrf_exempt
def ComentarioNoticia(request):
   
    if request.method=='POST':

        noticia = get_object_or_404(Publicacion, id = request.POST['id'] )
        comentario = request.POST['comentario']
        usuario = request.user
        fecha_alta = timezone.now()
        estado_comentario = 'p'
        if (comentario == ''):
            print("Tendriamos que tirar mensaje")        
        else:
            comentarioCreado = Comentario(fecha_alta=fecha_alta, publicacion= noticia, comentario= comentario, estado_comentario= estado_comentario, usuario= usuario )
            comentarioCreado.save()

    lista_carreras = Carrera.objects.all() 
    materiasC =[]
    for l in lista_carreras:
        materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])

    data = {
               'mensaje' : "Denuncia Exitosa"
            } 

    return JsonResponse(data)

@csrf_exempt
def DenunciarNoticia(request):
    if request.method=='POST':        

        tipo_denuncia = request.POST['tipo_denuncia']
        comentario = request.POST['comentario']
        usuario = request.user
        fecha_alta = timezone.now()
        

        if (tipo_denuncia == 'publicacion'):
            noticia = get_object_or_404(Publicacion, id = request.POST['id'] )   
            cantidad_denuncias = Denuncia.objects.all().filter(publicacion= noticia).count()
            if  (cantidad_denuncias >= 3):
                noticia.estado_publicacion = 'd'
                noticia.save() 

            if (comentario == ''):
                print("Tendriamos que tirar mensaje")        
            else:
                denuncia = Denuncia(publicacion= noticia, comentario= comentario, usuario= usuario, fecha_alta= fecha_alta)
                denuncia.save()

        else:
            usuarioDenunciado = get_object_or_404(Usuario, id = request.POST['id'] )

            cantidad_denuncias = Denuncia.objects.all().filter(usuarioDenunciado= usuarioDenunciado).count()
            if  (cantidad_denuncias >= 3):
                usuarioDenunciado.estado = 's'
                usuarioDenunciado.save() 

            if (comentario == ''):
                print("Tendriamos que tirar mensaje")        
            else:
                denuncia = Denuncia(usuarioDenunciado= usuarioDenunciado, comentario= comentario, usuario= usuario, fecha_alta= fecha_alta)
                denuncia.save()

    return render(request, 'home/publicacion_detail.html')
   


@csrf_exempt
def EliminarComentarioNoticia(request):
    if request.method=='POST':

        comentario = get_object_or_404(Comentario, id = request.POST['id'] )   
        comentario.fecha_baja = timezone.now()
        comentario.motivo_baja = "Usuario elimino su comentario"
        comentario.estado_comentario = 'e'

        comentario.save()

    return render(request, 'home/publicacion_detail.html')


@csrf_exempt
def MeGustaNoticia(request):
    if request.method=='POST':
        noticia = get_object_or_404(Publicacion, id = request.POST['id'] )  
       
        usuario = request.user
        fecha_alta = timezone.now()

        try:
            meGusta = MeGusta.objects.get(publicacion= noticia, usuario= usuario)
        except MeGusta.DoesNotExist:
            meGusta = None

        if (meGusta == None):
            megusta = MeGusta(publicacion= noticia, usuario= usuario, fecha_alta= fecha_alta)
            megusta.save()
            noticia.aprovacion =  noticia.aprovacion + 1

        else:
            meGustaEliminado = MeGusta.objects.get(publicacion= noticia, usuario= usuario)
            meGustaEliminado.delete()

            noticia.aprovacion =  noticia.aprovacion - 1


        noticia.save()
        
        
    return render(request, 'home/publicacion_detail.html')     


@csrf_exempt
def ComentarioPublicacion(request):
   
    if request.method=='POST':

        publicacion = get_object_or_404(Publicacion, id = request.POST['id'] )    
        comentario = request.POST['comentario']
        usuario = request.user
        fecha_alta = timezone.now()
        estado_comentario = 'p'
        if (comentario == ''):
            print("Tendriamos que tirar mensaje")        
        else:
            comentarioCreado = Comentario(fecha_alta=fecha_alta, publicacion= publicacion, comentario= comentario, estado_comentario= estado_comentario, usuario= usuario )
            comentarioCreado.save()

    lista_carreras = Carrera.objects.all() 
    materiasC =[]
    for l in lista_carreras:
        materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])

    return render(request, 'home/tema_detail.html', {'object': comentarioCreado})

@csrf_exempt
def DenunciarPublicacion(request):
    if request.method=='POST':

        publicacion = get_object_or_404(Publicacion, id = request.POST['id'] )   
        cantidad_denuncias = Denuncia.objects.all().filter(publicacion= publicacion).count()
        print (cantidad_denuncias)
        if  (cantidad_denuncias >= 3):
            publicacion.estado_publicacion = 'd'
            publicacion.save() 
        comentario = request.POST['comentario']
        usuario = request.user
        fecha_alta = timezone.now()
        if (comentario == ''):
            print("Tendriamos que tirar mensaje")        
        else:
            denuncia = Denuncia(publicacion= publicacion, comentario= comentario, usuario= usuario, fecha_alta= fecha_alta)
            denuncia.save()

    return render(request, 'home/tema_detail.html', {'object': publicacion})
   


@csrf_exempt
def EliminarComentarioPublicacion(request):
    if request.method=='POST':

        comentario = get_object_or_404(Comentario, id = request.POST['id'] )   
        comentario.fecha_baja = timezone.now()
        comentario.motivo_baja = "Usuario elimino su comentario"
        comentario.estado_comentario = 'e'

        print (comentario)
        comentario.save()

    return render(request, 'home/tema_detail.html')


@csrf_exempt
def MeGustaPublicacion(request):
    if request.method=='POST':
        publicacion = get_object_or_404(Publicacion, id = request.POST['id'] )  
       
        usuario = request.user
        fecha_alta = timezone.now()

        try:
            meGusta = MeGusta.objects.get(publicacion= publicacion, usuario= usuario)
        except MeGusta.DoesNotExist:
            meGusta = None

        if (meGusta == None):
            megusta = MeGusta(publicacion= publicacion, usuario= usuario, fecha_alta= fecha_alta)
            megusta.save()
            publicacion.aprovacion =  publicacion.aprovacion + 1

        else:
            meGustaEliminado = MeGusta.objects.get(publicacion= publicacion, usuario= usuario)
            meGustaEliminado.delete()

            publicacion.aprovacion =  publicacion.aprovacion - 1


        publicacion.save()
        
        
    return render(request, 'home/tema_detail.html')     



"""
GRUPOS
"""

@login_required
def grupoCreate(request):
    error = None
    group_name = ''
    if request.method == 'POST':
        group_name = request.POST.get('group_name', '')
        try:
            grupo = create_usergroup(request.user, group_name)
            estado = Estado_Grupo(grupo= grupo, estado= 'p', admin=request.user)
            estado.save()

            msg = ('Se ha creado el grupo "{0}".').format(group_name)
            messages.success(request, msg) 
            return redirect('groups_list')
        except GroupError as e:
            messages.error(request, e.message)

    lista_carreras = Carrera.objects.all() 
    materiasC =[]
    for l in lista_carreras: 
        materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])

    return render(request, 'home/grupo_form.html', { 
        'group_name': group_name,
        'lista_cantMaterias': materiasC,
    })

    return redirect('/')


@login_required
def gruposList(request):
    groups = request.user.groups.order_by('name').all()

    lista_carreras = Carrera.objects.all() 
    materiasC =[]
    for l in lista_carreras: 
        materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])

    grupos_publicados = []
    for grupoTotales in groups:
        propiedad_extra = Estado_Grupo.objects.get(grupo= grupoTotales)

        if (propiedad_extra.estado == 'p'):
            grupos_publicados.append(propiedad_extra.grupo)


    return render(request, 'home/grupos-list.html', {'grupos': grupos_publicados,'lista_cantMaterias': materiasC})

@csrf_exempt
@login_required 
def foroGrupo(request,pk):
    group= get_object_or_404(Group, id = pk)  
    GProxy = GroupProxy(group)
    if not (GProxy.is_member(request.user)):
        return redirect('groups_list')

    if request.method=='POST':
        cuerpo = request.POST['cuerpo']
        usuario = request.user
        grupo = group
        fecha_alta = timezone.now()
        estado_publicacion = 'p'
        tipo_publicacion = 'g'
        titulo = "Publicacion - Grupo"
        if (cuerpo == ''):
            print("Tendriamos que tirar mensaje")        
        else:
            publicacion = Publicacion(titulo = titulo, tipo_publicacion = tipo_publicacion, cuerpo= cuerpo, estado_publicacion= estado_publicacion, usuario= usuario, grupo = grupo )
            publicacion.save()
        

    lista_publicaciones = Publicacion.objects.all().filter(grupo=group,tipo_publicacion__exact='g', estado_publicacion__exact='p').order_by('-fecha_alta')
    lista_carreras = Carrera.objects.all() 

    eventoPersona = []
    miembrosOrtivas= []
    miembrosOrtivasposta = []
    lista_evento = Evento.objects.all().filter(grupo=group, fecha_evento__gte = datetime.date.today()).order_by('fecha_evento')    
    for evento in lista_evento:
        miembrosOrtivas = PersonaEvento.objects.all().filter(evento=evento)
        for m in miembrosOrtivas:
            miembrosOrtivasposta.append(m.usuario)
        eventoPersona.append((evento,miembrosOrtivasposta))
        miembrosOrtivasposta = []

    lista_publicaciones_comentarios=[]
    for l in lista_publicaciones: 
        lista_meGusta = MeGusta.objects.all().filter(publicacion= l)
        lista_meGusta_usuario =[]
        for lista in lista_meGusta:
            lista_meGusta_usuario.append(lista.usuario.id)

        lista_publicaciones_comentarios.append([l,Comentario.objects.all().filter(publicacion__exact=l, estado_comentario__exact='p').order_by('fecha_alta'), lista_meGusta_usuario])


    materiasC =[]
    for l in lista_carreras:
        materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])

    usuarios_no_miembro =[]
    estado = Estado_Grupo.objects.get(grupo= group)
    usuario_no_admin = []
    usuarios_miembro= group.user_set.all()
    for usuarioM in usuarios_miembro:
        if (usuarioM != estado.admin):
            usuario_no_admin.append(usuarioM)
        else:
            usuario_admin = usuarioM

    lista_usuarios = Usuario.objects.all()
    for usuario in lista_usuarios:
        if (usuario.usuario not in usuarios_miembro):
            usuarios_no_miembro.append(usuario)

    return render(request, 'home/grupo-foro.html', {'eventoPersona':eventoPersona,'lista_evento': lista_evento,'usuario_admin': usuario_admin, 'usuarios_no_admin':usuario_no_admin,'lista_usuarios_miembros': usuarios_miembro, 'lista_usuarios' : usuarios_no_miembro, 'lista_publicaciones': lista_publicaciones_comentarios, 'lista_carreras': lista_carreras, 'lista_cantMaterias': materiasC, 'group': group})

@login_required
@csrf_exempt
def invitacionGrupo(request):

    if request.method=='POST':
        grupo = get_object_or_404(Group, id = request.POST['idGroup'] )
        usuario = Usuario.objects.get(usuario=request.user)
        """       
        grupo.user_set.add(usuario.usuario)
        grupo.save()
        """
        invitacion = GroupInvitation.objects.get(group= grupo, invitee= usuario.usuario)
        if int(request.POST['idAction'])  == 1:        
            invitacion.accept()
        else:
            invitacion.refuse()
        #invitacion.delete()

    return render(request, 'home/grupo-foro.html')

@login_required
@csrf_exempt
def enviarInvitacionGrupo (request):
    if request.method=='POST':

        grupo = get_object_or_404(Group, id = request.POST['idGroup'] )
        usuario = get_object_or_404(Usuario, id=request.POST['idUser'])
        usuarioMiembro = get_object_or_404(User, id=request.user.id)

        invitacion = GroupInvitation(group= grupo, invitee= usuario.usuario, invited_by= usuarioMiembro)        
        invitacion.save()

        email_subject   = 'Cursivia - Invitación a grupo'
        email_body      = " Hola %s, ha sido invitado a formar parte del grupo %s. Para aceptar la invitación has clic en el siguiente link: https://cursivia.herokuapp.com/home/invitacion/%s " % (usuario.nombre, grupo.name , usuario.usuario.id)
        
        send_mail(email_subject,email_body, 'cursiviaweb@gmail.com',[usuario.eMail] )
        
        return render(request, 'home/grupo-foro.html')


def PerfilUsuario(request, pk):
    user = User.objects.get(id__exact=pk)
    usuario = Usuario.objects.get(usuario=user)
    lista_noticias = Publicacion.objects.all().filter(tipo_publicacion__exact='n', usuario__exact=user)
    lista_publicaciones = Publicacion.objects.all().filter(tipo_publicacion__exact='p', usuario__exact=user)
    lista_denuncia = Publicacion.objects.all().filter(usuario__exact=user, tipo_publicacion='d')

    lista_carreras = Carrera.objects.all() 
    materiasC =[]
    for l in lista_carreras: 
        materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])


    return render(request,'home/perfil_usuario.html', {'materiasC':materiasC, 'usuario':usuario, 'cantidad_noticias':lista_noticias.count(), 'cantidad_publicaciones': lista_publicaciones.count(),'cantidad_denuncia': lista_denuncia.count()})


@login_required
def invitacion (request, pk):

    if not (int(pk)==int(request.user.id)):
        return redirect('invitacion', request.user.id)

    user = User.objects.get(id__exact=pk)
    lista_invitacion = GroupInvitation.objects.all().filter(invitee = user)
    lista_carreras = Carrera.objects.all() 
    materiasC =[]
    for l in lista_carreras: 
        materiasC.append([l,Materia.objects.all().filter(carrera=l).count()])



    return render(request,'home/invitaciones_grupo.html', {'lista_cantMaterias':materiasC, 'lista_invitacion': lista_invitacion})

@csrf_exempt
def denunciarGrupo (request):
    if request.method=='POST':      

        comentario = request.POST['comentario']
        usuario = request.user
        fecha_alta = timezone.now()
        grupo = get_object_or_404(Group, id = request.POST['idGroup'] )

        cantidad_denuncias = Denuncia.objects.all().filter(grupoDenunciado= grupo).count()
        propiedad_extra = Estado_Grupo.objects.get(grupo= grupo)
        if  (cantidad_denuncias >= 3):
                propiedad_extra.estado= 'd'
                propiedad_extra.save() 
            
        if (comentario == ''):
            print("Tendriamos que tirar mensaje")        
        else:
            denuncia = Denuncia(grupoDenunciado= grupo, comentario= comentario, usuario= usuario, fecha_alta= fecha_alta)
            denuncia.save()

        
    return render(request, 'home/publicacion_detail.html')

@csrf_exempt
def designarAdministrador (request):
    grupo = get_object_or_404(Group, id = request.POST['idGroup'] )
    usuario = get_object_or_404(User, id = request.POST['idUser'] )
    estado = Estado_Grupo.objects.get(grupo= grupo)
    estado.admin = usuario
    estado.save()


    return render(request, 'home/publicacion_detail.html')

@csrf_exempt
def crearEvento(request):
    grupo = get_object_or_404(Group, id = request.POST['idGroup'])
    usuario = get_object_or_404(User, id = request.user.id)
    descripcion = request.POST['descripcion']
    titulo = request.POST['titulo']
    lugar = request.POST['lugar']
    fecha = request.POST['fecha']
    envento = Evento(grupo= grupo, usuarioCreador= usuario, cuerpo=descripcion, titulo= titulo, lugarEvento=lugar, fecha_evento=fecha)
    envento.save()

    return render(request, 'home/grupo-foro.html')


@csrf_exempt
def sacarEvento(request):
    evento = get_object_or_404(Evento, id = request.POST['idEvento'])
    usuario = get_object_or_404(User, id = request.user.id)
    personaEvento = PersonaEvento(evento= evento, usuario= usuario)
    personaEvento.save()

    return render(request, 'home/grupo-foro.html')

""" APIS.""" 

class NoticiaViewSet(viewsets.ModelViewSet):
    queryset =  Publicacion.objects.all().filter(estado_publicacion__exact='p').order_by('-fecha_alta')
    serializer_class = NoticiaSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend) 

class CarrerasViewSet(viewsets.ModelViewSet):
    queryset = Carrera.objects.all() 
    serializer_class = CarrerasSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)

class MateriasViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriasSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuariosSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)

class ComentariosViewSet(viewsets.ModelViewSet):
    queryset = Comentario.objects.all()
    serializer_class = ComentariosSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)

class MeGustaViewSet(viewsets.ModelViewSet):
    queryset = MeGusta.objects.all()
    serializer_class = meGustaSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)

class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = tokenSerializer

    

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
"""
User = get_user_model()
for user in User.objects.all():
    Token.objects.get_or_create(user=user)
"""

"""FIN APIS"""

def admin(request):
    print("EBTRA")
    return HttpResponseRedirect("/admin/")

