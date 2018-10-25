from django.conf.urls import url, include

from . import forms
from . import views


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^registracion/$',views.registracion, name ='registracion'),
	url(r'^confirmacion/$', views.confirmacion, name = 'confirmacion'),
	url(r'^bienvenido/(?P<tokenActivacion>\w+)/', views.bienvenido, name = 'bienvenido'),
	url(r'^configuracionCuenta/$', views.configuracionCuenta, name='configuracionCuenta'),
	url(r'^noticia/(?P<pk>\d+)$', views.noticiaDetailForm.as_view(), name="publicacion-detail"),
    url(r'^foroMateria/materia/(?P<pk>\d+)$', views.publicacionDetailForm.as_view(), name="tema-detail"),
	url(r'^noticia/create/$', views.NoticiaCreate.as_view(), name='noticia_create'),
    url(r'^noticia/(?P<pk>\d+)/update/$', views.NoticiaUpdate.as_view(), name='noticia_update'),
    url(r'^noticia/(?P<pk>\d+)/delete/$', views.NoticiaDelete, name='noticia_delete'),
    url(r'^foroUSCE/$', views.ForoGeneral, name ='foro_general'),
    url(r'^foroUSCE/(?P<pk>\d+)$', views.ForoGeneralComentarios, name ='foro_general_comentarios'),
    url(r'^foroCarrera/(?P<pk>\d+)$', views.ForoCarreraForm.as_view(), name ='foro_carrera'),
    url(r'^foroMateria/(?P<pk>\d+)$', views.ForoMateriaForm.as_view(), name ='foro_materia'),
    url(r'^noticia/comentario_noticia/$', views.ComentarioNoticia, name ='comentario_noticia'),
    url(r'^noticia/denunciar/$', views.DenunciarNoticia, name ='denunciar_noticia'),
    url(r'^noticia/comentario_noticia/delete$', views.EliminarComentarioNoticia, name ='eliminar_comentario_noticia'),
    url(r'^noticia/me_gusta/$', views.MeGustaNoticia, name ='me_gusta_noticia'),
    url(r'^foroMateria/materia/comentario_publicacion/$', views.ComentarioPublicacion, name ='comentario_publicacion'),
    url(r'^foroMateria/materia/denunciar/$', views.DenunciarPublicacion, name ='denunciar_publicacion'),
    url(r'^foroMateria/materia/comentario_publicacion/delete$', views.EliminarComentarioPublicacion, name ='eliminar_comentario_publicacion'),
    url(r'^foroMateria/materia/me_gusta/$', views.MeGustaPublicacion, name ='me_gusta_publicacion'),



    #url(r'^noticiaDetail/(?P<pk>\d+)$', views.noticiaDetailView.as_view(), name='publicacion-detail'),
	# url(r'^user/new/$', views.new_user, name='new-user'),
	#url(r'^nuevaNoticia/$', views.nuevaNoticia, name="nuevaNoticia"),
] 
