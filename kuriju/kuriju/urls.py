from django.conf.urls import patterns, include, url
from wkhtmltopdf.views import PDFTemplateView
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.views import login

urlpatterns = patterns('',
    url(r'^accounts/login/$', login),
    url(r'^$', 'django.contrib.auth.views.login', {'template_name':'index.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),

    url(r'^pdf/$', PDFTemplateView.as_view(template_name='my_template.html', filename='my_pdf.pdf'), name='pdf'),
    #url(r'^topdf/$','to_pdf',name= "to_pdf"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^autorizaciones/', include('apps.autorizaciones.urls', namespace="autorizaciones")),
    url(r'^localizaciones/', include('apps.localizaciones.urls', namespace="localizaciones")),
    url(r'^entidades/', include('apps.entidades.urls', namespace="entidades")),



    url(r'^about/$', TemplateView.as_view(template_name='index.html'), name='about'),
)
