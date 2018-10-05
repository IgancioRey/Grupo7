from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from .models import Publicacion, Carrera, Materia, Usuario
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from .forms import *
import random
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin




def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    lista_noticias = Publicacion.objects.all().filter(tipo_publicacion__exact='n').order_by('-fecha_alta')
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
        context={'lista_noticias': lista_noticias, 'numero_materias': numero_materias,
                 'lista_carreras': lista_carreras},
    )

class noticiaDetailView(LoginRequiredMixin,generic.DetailView):
    model = Publicacion
    #queryset = Publicacion.objects.all().filter(tipo_publicacion__exact='n').order_by('-fecha_alta')
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
                    usuario          = Usuario(usuario = user, tokenActivacion = token)

                    email_subject   = 'Bienvenido a Cursivia - Activación de usuario'
                    email_body      = " <p>Hola %s,</p> <p>Se ha registrado una cuenta con el correo %s.</p> <p> Para activarla has clic en el siguiente link: http://127.0.0.1:8000/home/bienvenido/%s </p>" % (nombre, email, token)
                    
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
