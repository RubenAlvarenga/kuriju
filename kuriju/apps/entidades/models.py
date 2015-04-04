from django.db import models
from apps.localizaciones.models import barrio, pais

class empresa(models.Model):
    nombrereal=models.CharField(max_length=100, verbose_name='Nombre Real')
    nombrefantasia=models.CharField(max_length=100, verbose_name='Nombre Comercial')
    class Meta:
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'
        ordering=['nombrereal']
    def __unicode__(self):
        return self.nombrereal

class persona(models.Model):
    nombre1=models.CharField(max_length=50, verbose_name='Primer Nombre')
    nombre2=models.CharField(max_length=50, verbose_name='Segundo Nombre', blank=True)
    apellido1=models.CharField(max_length=50, verbose_name='Primer Apellido')
    apellido2=models.CharField(max_length=50, verbose_name='Segundo Apellido', blank=True)
    cedula=models.CharField(max_length=10)
    nacionalidad=models.ForeignKey(pais, null=True)
    fechanacimiento=models.DateField(null=True)
    barrio=models.ForeignKey(barrio, null=True, blank=True)
    empresa=models.ForeignKey(empresa, null=True, blank=True)
    class Meta:
        verbose_name = 'persona'
        verbose_name_plural = 'personas'
        ordering =[ 'apellido1', 'apellido2', 'nombre1']
    def __unicode__(self):
        return '%s, %s' % (self.apellido1, self.nombre1)

class cliente(models.Model):
    ruc=models.CharField(max_length=10, blank=True, verbose_name='Ruc')
    @property
    def tipo(self):
        try:
            nombre=personacliente.objects.get(pk=self.id)
            nombre='Persona'
        except:
            nombre=empresacliente.objects.get(pk=self.id)
            nombre='Empresa'
        return str(nombre)
    @property
    def nombre(self):
        try: nombre=personacliente.objects.get(pk=self.id)
        except: nombre=empresacliente.objects.get(pk=self.id)
        return unicode(nombre)
    class Meta:
        verbose_name='cliente'
        verbose_name_plural='clientes'

    def __unicode__(self):
        try:
            nombre=personacliente.objects.get(pk=self.id)
            nombre=str(nombre.persona.apellido1)+', '+str(nombre.persona.nombre1)
        except:
            nombre=empresacliente.objects.get(pk=self.id)
            nombre=nombre.empresa.nombrereal
        return str(nombre)


class personacliente(cliente):
    persona=models.OneToOneField(persona)
    class Meta:
        verbose_name = 'cliente persona'
        verbose_name_plural = 'clientes personas'
    def __unicode__(self):
        return '%s, %s' % (self.persona.apellido1, self.persona.nombre1)
    def save(self, *args, **kwargs):
        
        super(personacliente, self).save(*args, **kwargs)


class empresacliente(cliente):
    empresa=models.OneToOneField(empresa)
    class Meta:
        verbose_name = 'cliente empresa'
        verbose_name_plural = 'clientes empresas'
    def __unicode__(self):
        return self.empresa.nombrereal
    def save(self, *args, **kwargs):
        
        super(empresacliente, self).save(*args, **kwargs)

class view_cliente(models.Model):
    ruc=models.CharField(max_length=10, blank=True, verbose_name='Ruc')
    tipo=models.CharField(max_length=10, blank=True, verbose_name='Tipo')
    nombre=models.CharField(max_length=100, verbose_name='Nombre')
    class Meta:
        managed = False
        verbose_name='cliente'
        verbose_name_plural='clientes'
