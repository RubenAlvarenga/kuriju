from django.forms import ModelForm
from django.contrib.auth.models import User, Group, Permission
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import perfil
from django.core.files.images import get_image_dimensions

class usuarioForm(UserCreationForm):
    #username= forms.CharField(widget=forms.TextInput(attrs={'readonly':'True'}))
    #email = forms.EmailField(required = True)
    avatar = forms.ImageField(required = False)
    class Meta:
        model = User
        fields = ['username',]
        widgets = {'password': forms.PasswordInput(),}

    # def clean_avatar(self):
    #     avatar = self.cleaned_data['avatar']
    #     try:
    #         w, h = get_image_dimensions(avatar)
    #         #validate dimensions
    #         max_width = max_height = 100
    #         if w > max_width or h > max_height:
    #             raise forms.ValidationError(
    #                 u'Please use an image that is %s x %s pixels or smaller.' % (max_width, max_height))
    #         #validate content type
    #         main, sub = avatar.content_type.split('/')
    #         if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
    #             raise forms.ValidationError(u'Please use a JPEG, GIF or PNG image.')
    #         #validate file size
    #         if len(avatar) > (20 * 1024):
    #             raise forms.ValidationError( u'Avatar file size may not exceed 20k.')
    #     except AttributeError:
    #         """
    #         Handles case when we are updating the user profile
    #         and do not supply a new avatar
    #         """
    #         pass
    #     return avatar


class updUsuarioForm(ModelForm):
    #username= forms.CharField(widget=forms.TextInput(attrs={'readonly':'True'}))
    email = forms.EmailField(required = True)
    avatar = forms.ImageField(required = False)
    class Meta:
        model = User
        exclude = ['password', 'groups', 'is_superuser', 'last_login', 'date_joined', 'is_active', 'user_permissions', 'is_staff']
    def clean_first_name(self):
        return self.cleaned_data['first_name'].capitalize()
    def clean_last_name(self):
        return self.cleaned_data['last_name'].capitalize()

class GruposForm(ModelForm):
    name = forms.CharField(required=True)
    #permissions = forms.MultipleChoiceField(Permission.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        exclude=( 'permissions', )
        model = Group
        # fields = ["title", "body", "category"]
        # widgets = {
        #     'body': forms.Textarea(),
        #     'category': forms.CheckboxSelectMultiple()
        # }