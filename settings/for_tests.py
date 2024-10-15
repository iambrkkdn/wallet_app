from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': TEST_DB_NAME,
        'USER': DB_ROOT_USER,
        'PASSWORD': DB_ROOT_PASS,
        'HOST': DB_HOST,
        'PORT': int(DB_PORT),
    }
}
