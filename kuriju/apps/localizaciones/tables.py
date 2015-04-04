#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django_tables2 as tables
from .models import pais, departamento, ciudad
from django.utils.safestring import mark_safe
from django.conf import settings


from django.utils.html import escape
#from django_tables2.utils import A
ITEM_POR_PAGINA = 50
# class CustomTextLinkColumn(tables.LinkColumn):
#     def __init__(self, viewname, urlconf=None, args=None, kwargs=None, current_app=None, attrs=None, custom_text=None, empty_values=None, **extra):
#         super(CustomTextLinkColumn, self).__init__(viewname, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app, attrs=attrs,  **extra)
#         self.custom_text = "dsadasd"
#     def render(self, value, record, bound_column):
#         return super(CustomTextLinkColumn, self).render(self, self.custom_text if self.custom_text else value, record, bound_column)

class ImageColumn(tables.Column):
    def render(self, value):
        return mark_safe('<img src='+settings.MEDIA_URL+'%s height="19" width="31"/>' % escape(value))
class EnlaceColumn(tables.Column):
    def render(self, value): return mark_safe('<a title="'+str(self.attrs["title"])+'" data-toggle="tooltip" data-placement="left" href="'+str(self.attrs["url"])+str(value)+'"><span class="glyphicon '+str(self.attrs["icono"])+'"></span></a>')

class paisesTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    bandera = ImageColumn(orderable=False)
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detPais/", "title":'Ver', "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"updPais/", "title":'Editar', "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"delPais/", "title":'Eliminar', "icono":"glyphicon-remove" }, )
    # ver = tables.LinkColumn( 'localizaciones:det_pais', args=[A('pk')], orderable=False, verbose_name=' ', attrs={"td": {"width": "2%"}}, empty_values=(), accessor="id" )
    # borrar = tables.LinkColumn( 'localizaciones:del_pais', args=[A('pk')], orderable=False, verbose_name=' ', attrs={"td": {"width": "2%"}}, empty_values=(),  accessor="id")
    class Meta:
        model = pais
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection", "id", "nombre", "bandera", "...", "ver", "editar", "borrar" )

class paisesTablePDF(tables.Table):
    class Meta:
        model = pais
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        #sequence = ("selection", "id", "nombre", "bandera", "...", "ver", "editar", "borrar" )


class departamentosTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detDepartamento/", "title":'Ver',  "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"updDepartamento/", "title":'Editar',  "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"delDepartamento/", "title":'Eliminar',  "icono":"glyphicon-remove" }, )
    class Meta:
        model = departamento
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection", "id", "nombre", "...", "ver", "editar", "borrar" )

class departamentosTablePDF(tables.Table):
    class Meta:
        model = departamento
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
