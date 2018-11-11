from django.conf.urls import url, include
from django.urls import path, include
from . import forms
from . import views
from rest_framework.authtoken import views as viewsapi


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^registracion/$',views.registracion, name ='registracion'),
	url(r'^confirmacion/$', views.confirmacion, name = 'confirmacion'),
	url(r'^bienvenido/(?P<tokenActivacion>\w+)/', views.bienvenido, name = 'bienvenido'),
	url(r'^configuracionCuenta/$', views.configuracionCuenta, name='configuracionCuenta'),
	url(r'^noticia/(?P<pk>\d+)$', views.noticiaDetailForm.as_view(), name="publicacion-detalle"),
    url(r'^foroMateria/materia/(?P<pk>\d+)$', views.publicacionDetailForm.as_view(), name="tema-detail"),
    url(r'^foroMateria/publicacion/create/(?P<pkM>\d+)$', views.PublicacionCreate.as_view(), name="tema-create"),
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
    url(r'^grupo/create$', views.grupoCreate, name='groups_create'),
    url(r'^grupo/list/$', views.gruposList, name='groups_list'),
    #url(r'^grupo/([a-zA-Z0-9_-]+)/$', show, name='groups_detail'),
    #url(r'^foroGrupo/([a-zA-Z0-9_-]+)/$', views.foroGrupo, name ='foro_grupo'), 
    url(r'^perfil/(?P<pk>\d+)$', views.PerfilUsuario, name ='perfil_usuario'),
    url(r'^foroGrupo/(?P<pk>\d+)$', views.foroGrupo, name ='foro_grupo'), 
    url(r'^foroGrupo/invitacion/$', views.invitacionGrupo, name ='invitacion_grupo'), 
    url(r'^invitacion/(?P<pk>\d+)$', views.invitacion, name ='invitacion'), 
    url(r'^foroGrupo/enviarInvitacion/$', views.enviarInvitacionGrupo, name ='enviar_invitacion_grupo'), 
    url(r'^foroGrupo/denunciar/$', views.denunciarGrupo, name ='denunciar_grupo'), 
    url(r'^foroGrupo/designarAdministrador/$', views.designarAdministrador, name ='designar_administrador'), 
    url(r'^api-token-auth/', viewsapi.obtain_auth_token),

]



    #url(r'^noticiaDetail/(?P<pk>\d+)$', views.noticiaDetailView.as_view(), name='publicacion-detail'),
	# url(r'^user/new/$    ', views.new_user, name='new-user'),
	#url(r'^nuevaNoticia/$', views.nuevaNoticia, name="nuevaNoticia"),

