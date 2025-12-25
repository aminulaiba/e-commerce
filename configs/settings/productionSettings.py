from .settings import *

DEBUG = False


SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['e-commerce-production-2463.up.railway.app', 'https://e-commerce-production-2463.up.railway.app']
CSRF_TRUSTED_ORIGINS = ['https://e-commerce-production-2463.up.railway.app']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}