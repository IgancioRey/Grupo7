from django.conf.urls import url, include

from . import views


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^registracion/$',views.registracion, name ='registracion'),
	url(r'^confirmacion/$', views.confirmacion, name = 'confirmacion'),
	url(r'^bienvenido/(?P<tokenActivacion>\w+)/', views.bienvenido, name = 'bienvenido'),
	url(r'^noticiaDetail/(?P<pk>\d+)$', views.noticiaDetailView.as_view(), name='publicacion-detail')


	# url(r'^user/new/$', views.new_user, name='new-user'),
] 
