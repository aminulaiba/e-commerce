from .settings import *

DEBUG = False


SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")

ALLOWED_HOSTS = ['e-commerce-production-2463.up.railway.app']
CSRF_TRUSTED_ORIGINS = ['https://e-commerce-production-2463.up.railway.app']


INSTALLED_APPS += [
    'cloudinary',
    'django_cloudinary_storage',
]


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



# This storage backend compresses files (gzip/brotli) and adds hashed filenames 
# so browsers can cache them safely and load updated versions automatically.
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # optional but recommended


DEFAULT_FILE_STORAGE = 'django_cloudinary_storage.storage.MediaCloudinaryStorage'
# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': os.environ.get('CLOUD_NAME'),
#     'API_KEY': os.environ.get('API_KEY'),
#     'API_SECRET': os.environ.get('API_SECRET')
# }



