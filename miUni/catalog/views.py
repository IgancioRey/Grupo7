from django.shortcuts import render
from .models import Publicacion, Genre, Documentacion
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Genera contadores de algunos de los objetos principales
    num_publicaciones = Publicacion.objects.all().count()
    num_genre = Genre.objects.all().count()
    # publicaciones disponibles (status = 'p') p --> publicado
    num_publicaciones_available = Publicacion.objects.filter(status__exact='p').count()

    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context={'num_publicaciones': num_publicaciones, 'num_genre': num_genre,
                 'num_publicaciones_available': num_publicaciones_available, 'num_visits': num_visits},
    )

class DocumentacionListView(generic.ListView):
    model = Documentacion
    paginate_by = 2

class DocumentacionDetailView(LoginRequiredMixin,generic.DetailView):
    model = Documentacion
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'


def new_user(request):

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = UserCreationForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            form.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # If this is a GET (or any other method) create the default form.
    else:

        form = UserCreationForm()
    return render(request,'catalog/newUser.html', {'form': form})
