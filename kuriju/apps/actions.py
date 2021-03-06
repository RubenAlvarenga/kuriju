# -*- coding: utf-8 -*-
# taken from http://weitlandt.com/theme/2010/05/wir-djangonauten-csv-export-nach-excel-mit-umlauten/
# + mucho amor de @julian_amaya y @votaguz

import csv
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template import Context, Template, RequestContext
from wkhtmltopdf.views import PDFTemplateResponse
from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect, urlresolvers
from datetime import datetime
from django.contrib import messages
from django.db import IntegrityError


def get_csv_from_dict_list(field_list, data):
    csv_line = ";".join(['{{ row.%s|addslashes }}' % field for field in field_list])
    template = "{% for row in data %}" + csv_line + "\n{% endfor %}"
    return Template(template).render(Context({"data": data}))


def export_as_pdf(request, table, *args, **kwargs):
    pdf_name = 'localizaciones/pdfListarPaises.html'
    return render(request, pdf_name, {'table':table})

def eliminar_bulk(request, queryset, *args, **kwargs):
    eliminados=[]
    #errores=[]
    modelo=queryset.model._meta.verbose_name_plural.capitalize()
    for obj in queryset:
        try:
            obj.delete()
            eliminados.append(str(obj))
        except IntegrityError as e:
            #dic={'messages': (e,)}
            #return render_to_response(self.template_name, dic, context_instance=RequestContext(request))
            #import pdb; pdb.set_trace()
            #errores.append(+" "+str(e))
            messages.add_message(request, messages.ERROR,  str(obj)+" "+str(e), extra_tags='danger' )


    success_message = "los "+str(modelo)+": "+str(eliminados)+" han sido eliminados con exito"
    if eliminados: messages.add_message(request, messages.SUCCESS, success_message )
    #if errores: messages.add_message(request, messages.ERROR, "dewfefesfsf fdsf" + str(errores) )
    url = request.META['HTTP_REFERER']
    return HttpResponseRedirect(url)


def export_as_csv(modelo, request, queryset):
    #if not request.user.is_staff:
        #raise PermissionDenied
    replace_dc = {'\n': '* ', '\r': '', ';': ',', '\"': '|', '\'': '|', 'True': 'Si', 'False': 'No'}
    #opts = modelo.model._meta
    opts = modelo._meta
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    #response = HttpResponse(mimetype='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
    w = csv.writer(response, delimiter=';')
    # import pdb; pdb.set_trace()
    try:
        field_names = modelo.get_csv_fields()
        v_field_names = field_names
    except:
        field_names = [field.name for field in opts.fields]
        v_field_names = [getattr(field, 'verbose_name') or field.name for field in opts.fields]
    v_field_names = map(lambda x: x.encode('utf-8') if x != 'ID' else 'Id', v_field_names)
    w.writerow(v_field_names)
    ax = []

    for obj in queryset:
        acc = {}
        for field in field_names:
            try:
                uf = unicode(getattr(obj, field)()).encode('utf-8')
            except:
                try:
                    uf = unicode(getattr(obj, field)).encode('utf-8')
                except:
                    uf = ''
            for i, j in replace_dc.iteritems():
                uf = uf.replace(i, j)
            if uf == 'None':
                uf = ''
            acc[field] = uf
        ax.append(acc)
    response.write(get_csv_from_dict_list(field_names, ax))
    return response

#export_as_csv.short_description = "Exportar como CSV"



def export_table_to_csv(modelo, request, table):
    #if not request.user.is_staff:
        #raise PermissionDenied
    replace_dc = {'\n': '* ', '\r': '', ';': ',', '\"': '|', '\'': '|', 'True': 'Si', 'False': 'No'}
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    #response = HttpResponse(mimetype='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(table.data.verbose_name_plural.title()+"_"+str(datetime.now().date())).replace('.', '_')
    w = csv.writer(response, delimiter=';')
    
    #try:
    #    field_names = modelo.get_csv_fields()
    #    v_field_names = field_names
    #except:
    field_names = [field.name for field in table.columns]
    v_field_names = [getattr(field, 'verbose_name') or field.name for field in table.columns]
    v_field_names = map(lambda x: x.encode('utf-8') if x != 'ID' else 'Id', v_field_names)
    w.writerow(v_field_names)
    ax = []



    for obj in table.rows:
        acc = {}
        for columna in range(len(field_names)):             
            uf = unicode(obj[columna]).encode('utf-8').replace("\'", "")
            acc[field_names[columna]]=uf
            # try:
            #     uf = unicode(getattr(obj.record, field)()).encode('utf-8')
            # except:
            #     try:
            #         uf = unicode(getattr(obj.record, field)).encode('utf-8')
            #     except:
            #         uf = ''
            # for i, j in replace_dc.iteritems():
            #     uf = uf.replace(i, j)
            # if uf == 'None':
            #     uf = ''
            # acc[field] = uf
        ax.append(acc)

    response.write(get_csv_from_dict_list(field_names, ax))
    return response
