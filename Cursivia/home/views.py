from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from .models import Publicacion, Carrera, Materia, Usuario
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


def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    lista_noticias = Publicacion.objects.all().filter(tipo_publicacion__exact='n').order_by('-fecha_alta')
    paginator = Paginator(lista_noticias, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    noticias = paginator.get_page(page)

    lista_carreras = Carrera.objects.all() 


    n = User.objects.filter(username__exact='iganciorey')
    """
    nueva = Publicacion()
    nueva.titulo = 'entro alguien!'
    nueva.cuerpo = 'acaba de entrar alguien al sitio'
    nueva.usuario = n[0]
    nueva.tipo_publicacion = 'n'
    nueva.estado_publicacion = 'p'
    nueva.alcance = 'g'
    nueva.save()
    """


    return render(request, 'index.html', {'noticias': noticias, 'lista_carreras': lista_carreras})
    """
    # Genera contadores de algunos de los objetos principales
    lista_noticias = Publicacion.objects.all().filter(tipo_publicacion__exact='n').order_by('-fecha_alta')
    lista_aux=[]
    noticias_final=[]
    x=0
    for noticia in lista_noticias:
        if len(lista_aux)<2:
            lista_aux.append(noticia)
            x=x+1
        else:
            x=0
            lista_aux=[]
            noticias_final.append(lista_aux)
    
    numero_materias = []
    lista_materias =  []
    lista_carreras = Carrera.objects.all()
    for c in lista_carreras:
        lista_materias.append((c.descripcion,Materia.objects.filter(carrera__exact =c).count()))

    # Publicaciones que sean noticias (tipoPublicacion = 'n')
    # numero_noticias = Publicacion.objects.filter(tipoPublicacion__exact='n').count()
    # Publicaciones que sean documentacion (tipoPublicacion = 'd')
    # numero_documentacion = Publicacion.objects.filter(tipoPublicacion__exact='d').count()

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html', 
        context={'lista_noticias': noticias_final, 'numero_materias': numero_materias,
                 'lista_carreras': lista_carreras},
    )
    """

class noticiaDetailView(LoginRequiredMixin,generic.DetailView):
    model = Publicacion
    #queryset = Publicacion.objects.all().filter(tipo_publicacion__exact='n').order_by('-fecha_alta')
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    


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
                    usuario          = Usuario(usuario = user, tokenActivacion = token)

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
    user.is_active  = True
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

class NoticiaCreate(CreateView):
    model = Publicacion
    fields = ['estado_publicacion']
    template_name= "home/publicacion_form.html"

    def post(self, request, *args, **kwargs):
        titulo = request.POST['titulo']
        cuerpo = request.POST['cuerpo']
        usuario = request.user
        tipo_publicacion =  'n'
        estado_publicacion = request.POST['estado_publicacion']

        noticia = Publicacion(titulo= titulo, cuerpo= cuerpo, tipo_publicacion= tipo_publicacion, estado_publicacion= estado_publicacion, usuario= usuario )
        
        noticia.save()
        prueba = get_object_or_404(Publicacion, pk=noticia.id)
        return render(request, 'home/publicacion_detail.html', {'object': prueba})

class NoticiaUpdate(UpdateView):
    model = Publicacion
    fields = ['titulo','cuerpo','estado_publicacion']

def NoticiaDelete(request, pk):

    noticia = get_object_or_404(Publicacion, id = pk )    
    noticia.estado_publicacion = 'e'
    noticia.fecha_baja = timezone.now()
    noticia.save()

    print("informacion de la noticia")
    print(noticia.id)
    print(noticia.titulo)
    print(noticia.estado_publicacion)
    return redirect('/')



