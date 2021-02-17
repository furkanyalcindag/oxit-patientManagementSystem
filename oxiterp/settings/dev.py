from oxiterp.settings.base import *

# Override base.py settings here


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'carservice',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }



}

GCM_APIKEY = "AAAAEgdR9KM:APA91bGJbWnT6MzzKIxRi9aAkfgyWCCRKxMNypBgpVjiM0ywTTU3xUyyK4_8Q3O8j-vVeY_k_genzinOnul2wDJKWQa3cnhuaHvG-3BVmdnjq3H1da1DHeKGjbF9ykimR-DlsC2ktnUw"

try:
    from oxiterp.settings.local import *
except:
    pass
