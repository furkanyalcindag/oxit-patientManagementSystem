from oxiterp.settings.base import *

# Override base.py settings here


DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dfrdqvu734v8c',
        'USER': 'zdqozojtqxtaef',
        'PASSWORD': '616ad722cef96d815d78b1f0beb2c0cd5a4a596440c78644a827864ef88b6a93',
        'HOST': 'ec2-54-196-111-158.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

EMAIL_HOST = "smtp.yandex.com.tr"
EMAIL_HOST_USER = "servis@kulmer.com.tr"
EMAIL_HOST_PASSWORD ="Servis2021"
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False

STATIC_ROOT = "/var/www/static/service"

STAICFILES_DIR = [

    "/var/www/static/service"

]

try:
    from oxiterp.settings.local import *
except:
    pass
