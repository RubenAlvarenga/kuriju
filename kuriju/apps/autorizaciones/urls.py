from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .views import listarUsuarios, addUsuario, updUsuario, detUsuario, addGrupo, listarGrupos, detGrupo, updGrupo, delGrupo
from apps.decorators import custom_permission_required
#from django.contrib.auth.decorators import login_required, permission_required



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myApp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^$', 'apps.autorizaciones.views.index'),
    # url(r'index/$', index2.as_view()),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='autorizaciones'),
    url(r'^listarUsuarios/$', listarUsuarios.as_view(), name ='listar_usuarios'),
    #url(r'^listarUsuarios/addUsuario/$', addUsuario.as_view(), name ='add_usuario'),
    url(r'^listarUsuarios/addUsuario/$', 'apps.autorizaciones.views.addUsuario', name='add_usuario'),

	url(r'^listarUsuarios/updUsuario/(?P<pk>[\d]+)$', 'apps.autorizaciones.views.updUsuario', name='upd_usuario'),
	#url(r'^listarUsuarios/detUsuario/(?P<pk>[\d]+)$', 'apps.autorizaciones.views.detUsuario', name='det_usuario'),
	url(r'^listarUsuarios/detUsuario/(?P<pk>[\d]+)$', detUsuario.as_view(), name='det_usuario'),

    url(r'^listarGrupos/$', listarGrupos.as_view(), name='listar_grupos'),
    url(r'^listarGrupos/addGrupo/$', 'apps.autorizaciones.views.addGrupo', name='add_grupo'),
    url(r'^listarGrupos/updGrupo/(?P<pk>[\d]+)$', 'apps.autorizaciones.views.updGrupo', name='upd_grupo'),
    url(r'^listarGrupos/detGrupo/(?P<pk>[\d]+)$', detGrupo.as_view(), name='det_grupo'),
    url(r'^listarGrupos/delGrupo/(?P<pk>[\d]+)$', custom_permission_required('Group.delete_group')(delGrupo.as_view()), name='del_grupo'),


)


