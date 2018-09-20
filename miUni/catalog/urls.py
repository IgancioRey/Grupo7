from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^documentacion/$', views.DocumentacionListView.as_view(), name='documentacion'),
    url(r'^documentacion/(?P<pk>\d+)$', views.DocumentacionDetailView.as_view(), name='documentacion-detail'),
    url(r'^user/new/$', views.new_user, name='new-user'),
]