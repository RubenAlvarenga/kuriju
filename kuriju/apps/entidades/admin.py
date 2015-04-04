from django.contrib import admin
from .models import empresa, persona, personacliente, empresacliente, cliente

class empresaAdmin(admin.ModelAdmin):
	list_display=('id','nombrereal', 'nombrefantasia',)
	list_display_links=('nombrereal',)

class clienteAdmin(admin.ModelAdmin):
	list_display=('id', cliente, 'tipo', )
	list_display_links=(cliente,)


admin.site.register(persona)
admin.site.register(empresa, empresaAdmin)
admin.site.register(cliente, clienteAdmin)
admin.site.register(personacliente)
admin.site.register(empresacliente)
