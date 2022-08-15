
import os
from GestorDeProyectosAgiles.settings import *

"""
Archivo setting para el ambiente de produccion
"""

DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1','localhost']
SECRET_KEY = os.environ['SECRET_KEY']

#HTTP SETTINGS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
ECURE_SSL_REDIRECT = True

#HSTS SETTINGS
#HTTP STRICT TRANSPORT SECURITY
SECURE_HSTS_SECONDS =31536000 #1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True # permite solo https


SECURE_BROWSER_XSS_FILTER = True #para que soporte todos los navegadores

#DJANGO_SETTINGS_MODULE = os.environ.get('DJANGO_SETTINGS_MODULE')