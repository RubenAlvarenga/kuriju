from django import forms
from .models import departamento, pais


class departamentoForm(forms.ModelForm):
    class Meta:
        model = departamento
        exclude = []
        widgets = {
            'nombre' : forms.TextInput(attrs = {
                    'class':'form-control',
                    'id' : 'nombre',
                    'placeholder' : 'Ingrese Nombre'
                }),
            'pais' : forms.Select(attrs = {
                    'class':'form-control',
                    'id' : 'pais',
                    'placeholder' : 'Ingrese Pais'
                }),
        }


    def clean_nombre(self):
        return self.cleaned_data['nombre'].capitalize()


class paisForm(forms.ModelForm):
    class Meta:
        model = pais
        exclude = []
        widgets = {
            'nombre' : forms.TextInput(attrs = {
                    'class':'form-control',
                    'id' : 'nombre',
                    'placeholder' : 'Ingrese Nombre'
                }),
            'countryiso_a2' : forms.TextInput(attrs = {
                    'class':'form-control',
                    'id' : 'countryiso_a2',
                    'placeholder' : 'Ingrese Codigo ISO A2'
                }),
            'countryiso_a3' : forms.TextInput(attrs = {
                    'class':'form-control',
                    'id' : 'countryiso_a3',
                    'placeholder' : 'Ingrese Codigo ISO A3'
                }),
            'bandera' : forms.FileInput(attrs = {
                    'class':'form-control',
                    'id' : 'countryiso_a3',
                    'placeholder' : 'Ingrese Codigo ISO A3'
                }),
        }

    def clean_nombre(self):
        return self.cleaned_data['nombre'].capitalize()

    def clean_countryiso_a2(self):
        return self.cleaned_data['countryiso_a2'].upper()

    def clean_countryiso_a3(self):
        return self.cleaned_data['countryiso_a3'].upper()
