from django.shortcuts import render, render_to_response, HttpResponseRedirect

from django_tables2 import SingleTableView, RequestConfig
from .models import cliente, view_cliente
from .tables import clientesTable, clientesTablePDF
from apps.functions import msg_render
from django.contrib import messages
from wkhtmltopdf.views import PDFTemplateResponse
from apps.actions import export_as_csv, export_table_to_csv, eliminar_bulk

class clienteSingleTableView(SingleTableView):
    template_name='base/generic_list.html'
    model = view_cliente
    table_class = clientesTable
    def get_queryset(self):
        table = super(clienteSingleTableView, self).get_queryset()
        q=self.request.GET.get("q")
        if q: return table.filter(nombre__icontains=q)#.order_by(sort)
        else: return table

    def get_context_data(self, **kwargs):
        context = super(clienteSingleTableView, self).get_context_data(**kwargs)
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
        clientes=view_cliente.objects.filter(pk__in=ids)
        accion=request.POST.get('accion')
        
        table = clientesTablePDF(clientes)
        if sort!='None':
            table.order_by = sort 

        if accion=='A csv':
            RequestConfig(request).configure(table)
            return export_table_to_csv(cliente, request, table)

        elif accion=='A pdf':
            table.model=cliente
            RequestConfig(request).configure(table)            
            pdf_name = 'base/generic_pdf_list.html'
            return PDFTemplateResponse(request, pdf_name, {'table':table})

    #     elif accion=='Eliminar':
    #         perm = 'cliente.delete_cliente'
    #         if request.user.has_perm(perm):
    #             if request.POST.get("confirmar")=='True':
    #                 return eliminar_bulk(request, clientees)
    #             else:
    #                 dic={'object_list':clientees}
    #                 template_name='base/generic_delete.html'
    #                 return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))
    #         else:
    #             mensaje = "ACCESO RESTRINGIDO | Permiso Requerido: "+str(perm)
    #             messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
    #             url = request.META['HTTP_REFERER']
    #             return HttpResponseRedirect(url)



def cliente_add(request):


    
    object_list=ciudad.objects.all()
    template='localizaciones/listarCiudades.html'
    #PARA PAGINACION
    paginator = Paginator(object_list, ITEM_POR_PAGINA)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    if page_obj.paginator.num_pages > 1:
        is_paginated=True

    return render_to_response(template, {"page_obj": page_obj}, context_instance=RequestContext(request, locals()))
