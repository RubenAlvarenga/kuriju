from django.conf.urls import patterns, url
from .views import  clienteSingleTableView, cliente_add
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from apps.decorators import custom_permission_required
urlpatterns = patterns('',

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='entidades'),
    url(r'^entidades/$', login_required(clienteSingleTableView.as_view()), name ='lst_cliente'),
    url(r'^entidades/addCliente/$', custom_permission_required('pais.add_cliente')(cliente_add), name ='add_cliente'),
    # url(r'^entidades/updCliente/(?P<pk>[\d]+)$', custom_permission_required('pais.change_pais')(paisUpdateView.as_view()), name='upd_pais'),
    # url(r'^entidades/delCliente/(?P<pk>[\d]+)$', custom_permission_required('pais.delete_pais')(paisDeleteView.as_view()), name='del_pais'),
    # url(r'^entidades/detCliente/(?P<pk>[\d]+)$', login_required(paisDetailView.as_view()), name='det_pais'),
)


