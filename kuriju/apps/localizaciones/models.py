#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
#from django.utils.safestring import mark_safe


#VALIDAR LOGITUD
def validarLongitud_2(value,length=2):
    if len(str(value))!=length:
        raise ValidationError(u'debe tener exactamente %s caracteres' % length)
def validarLongitud_3(value,length=3):
    if len(str(value))!=length:
        raise ValidationError(u'debe tener exactamente %s caracteres' % length)

class pais(models.Model):
    nombre=models.CharField(max_length=100, verbose_name='nombre', unique=True, validators=[
        RegexValidator(
                regex = '^[^0-9<>,;:.@]*$',
                message = 'Este campo no debe contener numeros ni caracteres especiales'
            )
        ])
    countryiso_a2=models.CharField(validators=[validarLongitud_2], max_length=2, verbose_name='codigo ISO A2', unique=True)
    countryiso_a3=models.CharField(validators=[validarLongitud_3], max_length=3, verbose_name='codigo ISO A3', unique=True)
    bandera=models.ImageField(upload_to='bandera_pais/',  null=True, blank=True, verbose_name='bandera')
    class Meta:
        verbose_name = 'pais'
        verbose_name_plural = 'paises'
        ordering=['nombre']
    def __unicode__(self):
        return self.nombre
    # def editarEnlace(self):
    #     return mark_safe("<strong>coso</strong>")
    #Capitaliza nombre, Mayusquea country
    def save(self, *args, **kwargs):
        nombre = getattr(self, 'nombre', False)
        if nombre:
            setattr(self, 'nombre', nombre.capitalize())
        for campo in ['countryiso_a2', 'countryiso_a3']:
            val = getattr(self, campo, False)
            if val:
                setattr(self, campo, val.upper())
        super(pais, self).save(*args, **kwargs)



class departamento(models.Model):
    nombre=models.CharField(max_length=100, verbose_name='nombre')
    pais=models.ForeignKey(pais, on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name = ('departamento')
        verbose_name_plural = ('departamentos')
    def __unicode__(self):
        return '%s, %s' % (self.nombre, self.pais.nombre)
    #Capitaliza nombre, Mayusquea country
    def save(self, *args, **kwargs):
        nombre = getattr(self, 'nombre', False)
        if nombre:
            setattr(self, 'nombre', nombre.capitalize())
        super(departamento, self).save(*args, **kwargs)
    

class ciudad(models.Model):
    nombre=models.CharField(max_length=100, verbose_name='nombre')
    departamento=models.ForeignKey(departamento, on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name = ('ciudad')
        verbose_name_plural = ('ciudades')

    def __unicode__(self):
        return '%s, %s' % (self.nombre, self.departamento.nombre)

class barrio(models.Model):
    nombre=models.CharField(max_length=100, verbose_name='nombre')
    ciudad=models.ForeignKey(ciudad, on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name = ('barrio')
        verbose_name_plural = ('barrios')

    def __unicode__(self):
        return '%s, %s' % (self.nombre, self.ciudad.nombre)
    
    