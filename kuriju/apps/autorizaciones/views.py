from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User, Group, Permission
from django.core.urlresolvers import reverse_lazy
import django_tables2 as tables
from apps.actions import export_as_csv, export_table_to_csv, export_as_pdf, eliminar_bulk
from django_tables2 import SingleTableView, RequestConfig
from .models import perfil
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.conf import settings
from apps.decorators import custom_permission_required
from django.db import IntegrityError
from django.shortcuts import render
from wkhtmltopdf.views import PDFTemplateResponse



# Create your views here.
ITEM_POR_PAGINA=25

class ImageColumn(tables.Column):
    def render(self, value):
        #return mark_safe('<img src='+settings.MEDIA_URL+'%s height="19" width="31"/>' % escape(value))
        return mark_safe('<img src= %s height="25" width="25"/>' % escape(value.url_30x30))
class EnlaceColumn(tables.Column):
    def render(self, value): return mark_safe('<a href="'+str(self.attrs["url"])+str(value)+'"><span class="glyphicon '+str(self.attrs["icono"])+'"></span></a>')

class usersTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    username=tables.Column(verbose_name='usuario')
    email=tables.Column(verbose_name='e-mail')
    last_login=tables.DateTimeColumn(verbose_name="ultimo ingreso")
    is_superuser=tables.BooleanColumn(verbose_name='admin')
    is_staff=tables.BooleanColumn(verbose_name='staff')
    get_full_name = tables.Column(verbose_name='nombres', order_by =("first_name"))
    perfil=ImageColumn(verbose_name='avatar', accessor="perfil.avatar")

    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./detUsuario/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./updUsuario/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./delUsuario/", "icono":"glyphicon-remove" }, )
    class Meta:
        model = User
        per_page=ITEM_POR_PAGINA
        exclude = ('password', 'last_name', 'first_name')
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection","perfil", "id", 'username', 'email', 'get_full_name'  )



class listarUsuarios(SingleTableView):
    template_name='autorizaciones/listarUsuarios.html'
    model = User
    table_class = usersTable
    def get_queryset(self):
        table = super(listarUsuarios, self).get_queryset()
        q=self.request.GET.get("q")
        if q:
            return table.filter(username__icontains=q)#.order_by(sort)
        else:
            return table

from .forms import usuarioForm, updUsuarioForm, GruposForm
from django.contrib.auth.models import User

# class addUsuario(SuccessMessageMixin, CreateView):
#     template_name='autorizaciones/addUsuario.html'
#     form_class = usuarioForm
#     success_url=reverse_lazy('autorizaciones:listar_usuarios')
#     success_message = ("El usuario %(username)s registrado con exito")

# class updUsuario(SuccessMessageMixin, UpdateView):
#     template_name='autorizaciones/updUsuario.html'
#     model=User
#     form_class = usuarioForm
#     success_url=reverse_lazy('autorizaciones:listar_usuarios')
#     success_message = ("El usuario %(username)s modificado con exito")
from django.contrib import messages
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, HttpResponseRedirect, urlresolvers
def addUsuario(request):
    if request.method == 'POST':
        form = usuarioForm(request.POST or None, request.FILES)
        if form.is_valid():
            usuario=form.save()
            userPerfil=perfil.objects.get(user_id=usuario.id)
            if request.FILES:
                userPerfil.avatar=request.FILES['avatar']
                userPerfil.save()
            # else:
            #     userPerfil.avatar="avatar_user/default.png"
            #     userPerfil.save()                
            success_message = "El Usuario "+str(usuario.username)+" creado con exito"
            messages.add_message(request, messages.SUCCESS, success_message)
            url = urlresolvers.reverse('autorizaciones:det_usuario', args=(usuario.id,))
            return HttpResponseRedirect(url)
        else:
           pass
    else:
        form = usuarioForm()

    template='autorizaciones/addUsuario.html'
    return render_to_response(template, {"form": form}, context_instance=RequestContext(request, locals()))

def updUsuario(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = updUsuarioForm(request.POST or None, request.FILES or None, instance=user)

    #form.fields['username'].widget.attrs['readonly'] = True
    if request.method == 'POST':
        if form.is_valid():
            usuario = form.save()
            try:
                userPerfil = perfil.objects.get(user_id=usuario.id)
            except:
                userPerfil=perfil()
                userPerfil.user=usuario
                userPerfil.save()
            if request.FILES:
                userPerfil.avatar=request.FILES['avatar']
                userPerfil.save()

            url = urlresolvers.reverse('autorizaciones:det_usuario', args=(pk,))
            return HttpResponseRedirect(url)
        else:
           pass
    template='autorizaciones/updUsuario.html'
    return render_to_response(template, {"form": form}, context_instance=RequestContext(request, locals()))


class detUsuario(DetailView):
    model=User
    template_name='autorizaciones/detUsuario.html'
    def get_context_data(self, **kwargs):
        context = super(detUsuario, self).get_context_data(**kwargs)
        permisos = Permission.objects.filter(user=context['object'])
        permisos_grupo= Permission.objects.filter(group__user=context['object'])
        context['user_permissions'] = permisos
        context['user_group_permissions'] = permisos_grupo
        return context


# from psycopg2 import connect
# conexion = connect("dbname=myapp host=localhost port=5432 user=postgres password=postgres") 
# cursor = conexion.cursor()

# def consultarp(sql,params):
#     existe=[]
#     cursor.execute(sql,params)
#     existe=cursor.fetchall()
#     return existe

class groupTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False, attrs = {"th__input":{"onclick": "", "id":'todosLosCheck', "name":"option"}, "td__input":{"class":"checkboxList", "name":"checks"} } )
    permissions=tables.Column(verbose_name='permisos', accessor="id")    
    ver     = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./detGrupo/", "icono":"glyphicon-eye-open" }, )
    editar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./updGrupo/", "icono":"glyphicon-pencil" }, )
    borrar  = EnlaceColumn( accessor="id", verbose_name=" ", attrs={"td": {"width": "2%"}, "url":"./delGrupo/", "icono":"glyphicon-remove" }, )
    def render_permissions(self, record):
        return [ str(i.name) for i in record.permissions.get_queryset() ]
    class Meta:
        model = Group
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }
        sequence = ("selection", "...",  )

class groupTablePDF(tables.Table):
    permissions=tables.Column(verbose_name='permisos', accessor="id")    
    def render_permissions(self, record):
        return [ str(i.name) for i in record.permissions.get_queryset() ]
    class Meta:
        model = Group
        per_page=ITEM_POR_PAGINA
        attrs = {"class": "table table-striped table-hover" }



class listarGrupos(SingleTableView):
    template_name='autorizaciones/listarGrupos.html'
    model = Group
    table_class = groupTable

    def get_queryset(self):
        table = super(listarGrupos, self).get_queryset()
        q=self.request.GET.get("q")
        if q:
            return table.filter(name__icontains=q)
        else:            
            return table
    def get_context_data(self, **kwargs):
        context = super(listarGrupos, self).get_context_data(**kwargs)
        context['sort']= self.request.GET.get("sort")
        return context



    def post(self, request, *args, **kwargs):
        checks = request.POST.getlist('checks')
        accion=request.POST.get('accion')
        sort=request.POST.get('sort')
        ids = map(int, checks)
        grupos=Group.objects.filter(pk__in=ids)        
        table = groupTablePDF(grupos)
        if sort!='None':
            table.order_by = sort 

        if accion=='A csv':
            RequestConfig(request).configure(table)
            return export_table_to_csv(Group, request, table)

        elif accion=='A pdf':
            table.model=Group
            RequestConfig(request).configure(table)            
            pdf_name = 'localizaciones/pdfListarPaises.html'
            return PDFTemplateResponse(request, pdf_name, {'table':table})

        elif accion=='Eliminar':
            perm = 'Group.delete_group'
            if request.user.has_perm(perm):
                if request.POST.get("confirmar")=='True':
                    return eliminar_bulk(request, grupos)
                else:
                    dic={'object_list':grupos}
                    template_name='autorizaciones/delGrupo.html'
                    return render_to_response(template_name, dic, context_instance=RequestContext(request, locals()))


            else:
                mensaje = "ACCESO RESTRINGIDO | Permiso Requerido: "+str(perm)
                messages.add_message(request, messages.ERROR, mensaje, extra_tags='danger')
                url = request.META['HTTP_REFERER']
                return HttpResponseRedirect(url)




@custom_permission_required('Group.add_group')
def addGrupo(request):
    form = GruposForm(request.POST or None)
    #table = permissionTable(Permission.objects.all())
    permisos = Permission.objects.all()
    #RequestConfig(request).configure(table)
    template='autorizaciones/addGrupo.html'
    if request.method == 'POST':
        checks = request.POST.getlist('duallistbox_permisos')
        ids = map(int, checks)
        permisosSeleccionados=Permission.objects.filter(pk__in=ids)
        if form.is_valid():
            grupo=form.save(commit=False)
            grupo.save()
            for permiso in permisosSeleccionados:
                grupo.permissions.add(permiso)
            grupo.save()
            success_message = "El Grupo "+str(grupo.name)+" fue creado con exito"
            messages.add_message(request, messages.SUCCESS, success_message)
            url = urlresolvers.reverse('autorizaciones:det_grupo', args=(grupo.id,))
            return HttpResponseRedirect(url)
        else:
            for id_permiso_seleccionado in ids:
                for permiso in permisos:
                    if id_permiso_seleccionado==permiso.id:
                        permiso.seleccionado='selected="selected"'
                        break
    return render_to_response(template, {"form": form, "permisos":permisos}, context_instance=RequestContext(request, locals()))

class detGrupo(DetailView):
    model=Group
    template_name='autorizaciones/detGrupo.html'
    def get_context_data(self, **kwargs):
        context = super(detGrupo, self).get_context_data(**kwargs)

        permisos = context['object'].permissions.get_queryset()
        context['group_permissions']= permisos

        return context


def updGrupo(request, pk):
    grupo = get_object_or_404(Group, pk=pk)
    form = GruposForm(request.POST or None,  instance=grupo)
    permisosActuales = grupo.permissions.get_queryset()
    permisos = Permission.objects.all()
    for permiso_seleccionado in permisosActuales:
        for permiso in permisos:
            if permiso_seleccionado.id==permiso.id:
                permiso.seleccionado='selected="selected"'
                break

    if request.method == 'POST':
        checks = request.POST.getlist('duallistbox_permisos')
        ids = map(int, checks)
        permisosSeleccionados=Permission.objects.filter(pk__in=ids)
        if form.is_valid():
            conjActuales= set(permisosActuales)
            conjSeleccionados = set(permisosSeleccionados)
            grupo=form.save(commit=False)
            grupo.save()
            aBorrar= conjActuales - conjSeleccionados
            for permiso in aBorrar:
                grupo.permissions.remove(permiso)
            for permiso in permisosSeleccionados:
                grupo.permissions.add(permiso)
            grupo.save()
            success_message = "El Grupo "+str(grupo.name)+" fue creado con exito"
            messages.add_message(request, messages.SUCCESS, success_message)
            url = urlresolvers.reverse('autorizaciones:det_grupo', args=(grupo.id,))
            return HttpResponseRedirect(url)
        else:
            for id_permiso_seleccionado in ids:
                for permiso in permisos:
                    if id_permiso_seleccionado==permiso.id:
                        permiso.seleccionado='selected="selected"'
                        break

    template='autorizaciones/updGrupo.html'
    return render_to_response(template, {"form": form, "permisos": permisos}, context_instance=RequestContext(request, locals()))


class delGrupo(SuccessMessageMixin, DeleteView):
    template_name='autorizaciones/delGrupo.html'
    model=Group
    success_url=reverse_lazy('autorizaciones:listar_grupos')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            success_message = "El Grupo "+str(self.object.name)+" eliminado con exito"
            messages.add_message(request, messages.SUCCESS, success_message )
            return HttpResponseRedirect(self.get_success_url(), )
        except IntegrityError as e:
            e.tags='danger'
            dic={'messages': (e,)}
            return render_to_response(self.template_name, dic, context_instance=RequestContext(request))
