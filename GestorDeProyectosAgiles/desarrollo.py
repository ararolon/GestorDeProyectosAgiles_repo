from decouple import config
from GestorDeProyectosAgiles.settings import *

"""
Archivo setting del ambiente de desarrollo
"""


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

"""
Base de datos configurada con POSTGRESQL
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'GestorDeProyectosAgiles',
        'USER': 'admin',
        'PASSWORD': config('PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',

    }
}
