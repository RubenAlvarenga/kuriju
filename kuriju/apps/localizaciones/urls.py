from django.conf.urls import patterns, url
from .views import paisSingleTableView, paisCreateView, paisUpdateView, paisDeleteView, paisDetailView, departamentoSingleTableView, departamentoCreateView, departamentoDetailView, departamentoDeleteView, departamentoUpdateView 
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from apps.decorators import custom_permission_required

#from django.conf import settings

#from wkhtmltopdf.views import PDFTemplateView

urlpatterns = patterns('',

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='localizaciones'),

    # url(r'^listarPaises/$', login_required(listarPaises.as_view()), name ='listar_paises'),
    # url(r'^listarPaises/addPais/$', addPais.as_view(), name ='add_pais'),
    # url(r'^listarPaises/updPais/(?P<pk>[\d]+)$', permission_required('pais.change_pais')(updPais.as_view()), name='upd_pais'),
    # url(r'^listarPaises/delPais/(?P<pk>[\d]+)$', delPais.as_view(), name='del_pais'),
    # url(r'^listarPaises/detPais/(?P<pk>[\d]+)$', detPais.as_view(), name='det_pais'),

    url(r'^paises/$', login_required(paisSingleTableView.as_view()), name ='lst_pais'),
    url(r'^paises/addPais/$', custom_permission_required('pais.add_pais')(paisCreateView.as_view()), name ='add_pais'),
    url(r'^paises/updPais/(?P<pk>[\d]+)$', custom_permission_required('pais.change_pais')(paisUpdateView.as_view()), name='upd_pais'),
    url(r'^paises/delPais/(?P<pk>[\d]+)$', custom_permission_required('pais.delete_pais')(paisDeleteView.as_view()), name='del_pais'),
    url(r'^paises/detPais/(?P<pk>[\d]+)$', login_required(paisDetailView.as_view()), name='det_pais'),

    # url(r'^listarDepartamentos/$', listarDepartamentos.as_view(), name ='listar_departamentos'),
    # url(r'^listarDepartamentos/addDepartamento/$', addDepartamento.as_view(), name ='add_departamento'),
    # url(r'^listarCiudades/$', 'apps.localizaciones.views.listarCiudades', name ='listar_ciudades'),

    url(r'^departamentos/$', login_required(departamentoSingleTableView.as_view()), name ='lst_departamento'),
    url(r'^departamentos/addDepartamento/$', custom_permission_required('departamento.add_departamento')(departamentoCreateView.as_view()), name ='add_departamento'),
    url(r'^departamentos/updDepartamento/(?P<pk>[\d]+)$', custom_permission_required('departamento.change_departamento')(departamentoUpdateView.as_view()), name='upd_departamento'),
    url(r'^departamentos/delDepartamento/(?P<pk>[\d]+)$', custom_permission_required('departamento.delete_departamento')(departamentoDeleteView.as_view()), name='del_departamento'),
    url(r'^departamentos/detDepartamento/(?P<pk>[\d]+)$', login_required(departamentoDetailView.as_view()), name='det_departamento'),

)


