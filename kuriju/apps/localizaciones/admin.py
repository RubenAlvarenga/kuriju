from django.contrib import admin
from .models import pais, departamento, ciudad, barrio

# class departamentoInline(admin.StackedInline):
# 	model=departamento
# 	extra=1


class paisAdmin(admin.ModelAdmin):
	list_display=('id','nombre', 'countryiso_a2', 'countryiso_a3',)
	list_display_links=('nombre',)
	#inlines=[departamentoInline]

class departamentoAdmin(admin.ModelAdmin):
	list_display=('id','nombre', 'pais')
	list_display_links=('nombre',)
class ciudadAdmin(admin.ModelAdmin):
	list_display=('id','nombre', 'departamento',)
	list_display_links=('nombre',)
class barrioAdmin(admin.ModelAdmin):
	list_display=('id','nombre', 'ciudad',)
	list_display_links=('nombre',)


admin.site.register(pais, paisAdmin)
admin.site.register(departamento, departamentoAdmin)
admin.site.register(ciudad, ciudadAdmin)
admin.site.register(barrio, barrioAdmin)
