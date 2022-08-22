from core.settings.base import *

import dj_database_url
from decouple import config

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

CSRF_TRUSTED_ORIGINS = [
    'https://gestordeproyec-prod-gestordeproyectosagiles-2cdwsx.mo2.mogenius.io'
]
