#import os
#BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from unipath import Path
BASE_DIR=Path(__file__).ancestor(3)

SECRET_KEY = '-8z3+g*myhmrtn88#^5*_u=%cqactoc1x=u&s&3jqq-qbunk+m'

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
LOCAL_APPS = (
    'apps.entidades',
    'apps.autorizaciones',
    'apps.localizaciones',   
)
THIRD_PARTY_APPS = (
    'wkhtmltopdf',
    #'debug_toolbar.apps.DebugToolbarConfig',
    'django_tables2',
)
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

WKHTMLTOPDF_CMD='/usr/bin/wkhtmltopdf'
WKHTMLTOPDF_CMD_OPTIONS = {
   'quiet':True,
}

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'apps.context_processors.menu',
    'django.contrib.messages.context_processors.messages',
)

from django.core.urlresolvers import reverse_lazy
LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')

MIDDLEWARE_CLASSES = (
    'apps.middleware.RequestTimeLoggingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'breadcrumbs.middleware.BreadcrumbsMiddleware',
    #'webstack_django_sorting.middleware.SortingMiddleware',
)

ROOT_URLCONF = 'kuriju.urls'

WSGI_APPLICATION = 'kuriju.wsgi.application'

LANGUAGE_CODE = 'es-py'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TEMPLATE_DIRS = (
    BASE_DIR.child('templates'),
)
