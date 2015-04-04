#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django_tables2 as tables
from .models import cliente, view_cliente
from django.utils.safestring import mark_safe
from django.conf import settings
from  django_tables2  import  A

from django.utils.html import escape
ITEM_POR_PAGINA = 50

class EnlaceColumn(tables.Column):
    def render(self, value): return mark_safe('<a href="'+str(self.attrs["url"])+str(value)+'"><span class="glyphicon '+str(self.attrs["icono"])+'"></span></a>')

class clientesTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"td": {"width": "2%"}, "th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    tipo    = tables.Column(verbose_name='tipo', order_by =("tipo", "nombre"))
    nombre  = tables.Column(verbose_name='nombre')#, order_by =("personacliente", 'empresacliente'))
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"detPais/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"updPais/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"delPais/", "icono":"glyphicon-remove" }, )
    class Meta:
        model = view_cliente
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection", "...", "ver", "editar", "borrar" )

class clientesTablePDF(tables.Table):
    class Meta:
        model = view_cliente
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
