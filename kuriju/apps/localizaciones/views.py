#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from .models import pais, departamento
from django.core.urlresolvers import reverse_lazy
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponseRedirect
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.messages.views import SuccessMessageMixin
from .forms import departamentoForm, paisForm
from .tables import paisesTable, departamentosTable, paisesTablePDF, departamentosTablePDF
from django.db import IntegrityError
from apps.actions import export_as_csv, export_as_pdf, export_table_to_csv, eliminar_bulk
from django.contrib.auth.decorators import login_required
from wkhtmltopdf.views import PDFTemplateResponse
from django.contrib import messages
from apps.functions import msg_render
from django_tables2 import SingleTableView, RequestConfig





# @login_required
# def listarCiudades(request):
#     object_list=ciudad.objects.all()
#     template='localizaciones/listarCiudades.html'
#     #PARA PAGINACION
#     paginator = Paginator(object_list, ITEM_POR_PAGINA)
#     page = request.GET.get('page')
#     try:
#         page_obj = paginator.page(page)
#     except PageNotAnInteger:
#         page_obj = paginator.page(1)
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages)
#     if page_obj.paginator.num_pages > 1:
#         is_paginated=True
#     return render_to_response(template, {"page_obj": page_obj}, context_instance=RequestContext(request, locals()))


class paisSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = pais
    table_class = paisesTable
    def get_queryset(self):
        table = super(paisSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(nombre__icontains=q)#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(paisSingleTableView, self).get_context_data(**kwargs)
        context['sort']= self.request.GET.get("sort")
        return context

    def post(self, request, *args, **kwargs):
        checks = request.POST.getlist('checks')
        if not checks:
            mensaje = msg_render("<strong>Favor seleccione por lo menos un item</strong>")
            messages.add_message(request, messages.INFO, mensaje)
            url = request.META['HTTP_REFERER']
            return HttpResponseRedirect(url)


        sort=request.POST.get('sort')
        ids = map(int, checks)
        paises=pais.objects.filter(pk__in=ids)
        accion=request.POST.get('accion')
        
        table = paisesTablePDF(paises)
        if sort!='None':
            table.order_by = sort 

        if accion=='A csv':
            RequestConfig(request).configure(table)
            return export_table_to_csv(pais, request, table)

        elif accion=='A pdf':
            table.model=pais
            RequestConfig(request).configure(table)            
            pdf_name = 'base/generic_pdf_list.html'
            return PDFTemplateResponse(request, pdf_name, {'table':table})

        elif accion=='Eliminar':
            perm = 'pais.delete_pais'
            if request.user.has_perm(perm):
                if request.POST.get("confirmar")=='True':
                    return eliminar_bulk(request, paises)
                else:
                    dic={'object_list':paises}
                    template_name='base/generic_delete.html'
                    return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))
            else:
                mensaje = "ACCESO RESTRINGIDO | Permiso Requerido: "+str(perm)
                messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                url = request.META['HTTP_REFERER']
                return HttpResponseRedirect(url)




class paisUpdateView(SuccessMessageMixin, UpdateView):
    template_name='base/generic_update.html'
    model=pais
    form_class = paisForm
    #success_url=reverse_lazy('localizaciones:lst_pais')
    success_message = "El pais %(nombre)s modificado con exito"
    def get_success_url(self):
        return reverse_lazy('localizaciones:det_pais', args=(self.object.id, ))



    # def get_context_data(self, **kwargs):
    #     context = super(updPais, self).get_context_data(**kwargs)
    #     data = self.kwargs['id']
    #     context['object'] = pais.objects.filter(rna_id=data)
    #     return context    

class paisCreateView(SuccessMessageMixin, CreateView):
    template_name='base/generic_add.html'
    form_class = paisForm
    success_message = "El pais %(nombre)s registrado con exito"
    def get_success_url(self):
        return reverse_lazy('localizaciones:det_pais', args=(self.object.id, ))

    # def post(self, request, *args, **kwargs):
    #     estado=False
    #     obj=pais()
    #     obj.nombre=request.POST['nombre']
    #     obj.countryiso_a2=request.POST['countryiso_a2']
    #     obj.countryiso_a3=request.POST['countryiso_a3']
    #     obj.save()
    #     estado=True
    #     dic={'estado': estado}
    #     render_to_response('localizaciones/lstPais.html', dic, context_instance=RequestContext(request))

class paisDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=pais
    success_url=reverse_lazy('localizaciones:lst_pais')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render(u"El Pais <strong>"+unicode(self.object.nombre)+u"</strong> eliminado con éxito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))


class paisDetailView(DetailView):
    model=pais
    template_name='localizaciones/detPais.html'



class departamentoSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = departamento
    table_class = departamentosTable
    def get_queryset(self):
        table = super(departamentoSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(nombre__icontains=q)#.order_by(sort)
        else: return table
    def get_context_data(self, **kwargs):
        context = super(departamentoSingleTableView, self).get_context_data(**kwargs)
        context['sort']= self.request.GET.get("sort")
        return context
    def post(self, request, *args, **kwargs):
        checks = request.POST.getlist('checks')
        sort=request.POST.get('sort')
        ids = map(int, checks)
        departamentos=departamento.objects.filter(pk__in=ids)
        accion=request.POST.get('accion')
        
        table = departamentosTablePDF(departamentos)
        if sort!='None':
            table.order_by = sort 
        if accion=='A csv':
            RequestConfig(request).configure(table)
            return export_table_to_csv(departamento, request, table)
        elif accion=='A pdf':
            table.model=departamento
            RequestConfig(request).configure(table)            
            pdf_name = 'base/generic_pdf_list.html'
            return PDFTemplateResponse(request, pdf_name, {'table':table})

        elif accion=='Eliminar':
            perm = 'departamento.delete_departamento'
            if request.user.has_perm(perm):
                if request.POST.get("confirmar")=='True':
                    return eliminar_bulk(request, departamentos)
                else:
                    dic={'object_list':departamentos}
                    template_name='base/generic_delete.html'
                    return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))
            else:
                mensaje = "ACCESO RESTRINGIDO | Permiso Requerido: "+str(perm)
                messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                url = request.META['HTTP_REFERER']
                return HttpResponseRedirect(url)

class departamentoCreateView(SuccessMessageMixin, CreateView):
    template_name='base/generic_add.html'
    form_class = departamentoForm
    success_message = "El departamento %(nombre)s registrado con exito"
    def get_success_url(self):
        return reverse_lazy('localizaciones:det_departamento', args=(self.object.id, ))

class departamentoUpdateView(UpdateView):
    template_name='base/generic_update.html'
    model=departamento
    form_class = departamentoForm
    success_message = "El departamento %(nombre)s modificado con exito"
    def get_success_url(self):
        return reverse_lazy('localizaciones:det_departamento', args=(self.object.id, ))

class departamentoDetailView(DetailView):
    model=departamento
    template_name='localizaciones/detDepartamento.html'

class departamentoDeleteView(SuccessMessageMixin, DeleteView):
    template_name='base/generic_delete.html'
    model=departamento
    success_url=reverse_lazy('localizaciones:lst_departamento')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = msg_render("El departamento <strong>"+str(self.object.nombre)+"</strong> eliminado con exito")
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,), 'object': self.object}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))
