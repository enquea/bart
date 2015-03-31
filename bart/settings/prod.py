from shared import *

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bart_app',
        'USER': 'bart_app_user',
        'PASSWORD': PG_PASSWORD,
        'HOST': '',
        'PORT': '',
    }
}


