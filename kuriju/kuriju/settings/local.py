from .base import *
import os

DEBUG = True

TEMPLATE_DEBUG = True

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kuriju',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

MEDIA_ROOT = BASE_DIR.child('media')
MEDIA_URL = 'http://127.0.0.1:8000/media/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] #(BASE_DIR.child('static'),)
STATIC_ROOT = '/'#os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
AUTH_PROFILE_MODULE = 'apps.autorizaciones.perfil'
