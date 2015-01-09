import sys

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pammy',
        'HOST': 'localhost',
        'USER': 'pamela',
        'PASSWORD': 'anderson',
    }
}

TASTYPIE_FULL_DEBUG = True
