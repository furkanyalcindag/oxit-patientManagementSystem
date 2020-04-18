from oxiterp.settings.base import *

# Override base.py settings here


DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'oxit_booqe',
        'USER': 'oxitowner',
        'PASSWORD': 'oxit2016',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_ROOT = "/var/www/static/booqe"

STAICFILES_DIR = [

    "/var/www/static/booqe"

]

try:
    from oxiterp.settings.local import *
except:
    pass
