from oxiterp.settings.base import *

# Override base.py settings here


DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'oxiterp',
        'USER': 'oxitowner',
        'PASSWORD': 'oxit2016',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_ROOT = "/var/www/static/"

STAICFILES_DIR = [

    "/var/www/static/"

]

try:
    from oxiterp.settings.local import *
except:
    pass
