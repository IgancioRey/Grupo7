from django.conf.urls import url, include

from . import forms
from . import views


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^registracion/$',views.registracion, name ='registracion'),
	url(r'^confirmacion/$', views.confirmacion, name = 'confirmacion'),
	url(r'^bienvenido/(?P<tokenActivacion>\w+)/', views.bienvenido, name = 'bienvenido'),
	url(r'^noticiaDetail/(?P<pk>\d+)$', views.noticiaDetailView.as_view(), name='publicacion-detail'),
	url(r'^configuracionCuenta/$', views.configuracionCuenta, name='configuracionCuenta'),
	url(r'^noticiaD/(?P<pk>\d+)$', views.noticiaDetailForm.as_view(), name="publicacion-detail"),
	url(r'^nuevaNoticia/$', views.nuevaNoticia, name="nuevaNoticia")



	# url(r'^user/new/$', views.new_user, name='new-user'),
] 
