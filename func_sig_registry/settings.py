"""
Django settings for func_sig_registry project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

import dj_database_url
import excavator as env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get('DJANGO_SECRET_KEY', required=True)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.get('DJANGO_DEBUG', type=bool, default=False)

ALLOWED_HOSTS = env.get('DJANGO_ALLOWED_HOSTS', type=list, required=not DEBUG)

SECURE_SSL_REDIRECT = env.get('DJANGO_SECURE_SSL_REDIRECT', type=bool, default=True)

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'func_sig_registry.registry',
    'rest_framework',
    'django_tables2',
    'storages',
    's3_folder_storage',
    'huey.contrib.djhuey',
]


DJANGO_DEBUG_TOOLBAR_ENABLED = env.get(
    'DJANGO_DEBUG_TOOLBAR_ENABLED', type=bool, default=True,
)

if DJANGO_DEBUG_TOOLBAR_ENABLED:
    # Django Debug Toolbar
    # Provides useful tools for debugging sites either in development or
    # production.
    try:
        import debug_toolbar  # NOQA
        INSTALLED_APPS.append('debug_toolbar')
    except ImportError:
        pass

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'func_sig_registry.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(APP_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'func_sig_registry.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {}

DATABASES['default'] = dj_database_url.config(
    default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
)

DATABASES['default']['ATOMIC_REQUESTS'] = env.get(
    'DJANGO_ATOMIC_REQUESTS',
    type=bool,
    default=True,
)


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Files
# https://docs.djangoproject.com/en/1.9/topics/files/
DEFAULT_FILE_STORAGE = env.get(
    'DJANGO_DEFAULT_FILE_STORAGE',
    type=str,
    default='django.core.files.storage.FileSystemStorage',
)

MEDIA_ROOT = env.get(
    'DJANGO_MEDIA_ROOT',
    type=str,
    default=os.path.join(BASE_DIR, 'public', 'media'),
)
MEDIA_URL = env.get(
    'DJANGO_MEDIA_URL',
    type=str,
    default='/media/',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(APP_DIR, 'static'),
]


STATIC_ROOT = env.get(
    'DJANGO_STATIC_ROOT',
    type=str,
    default=os.path.join(BASE_DIR, 'public', 'static'),
)

STATIC_URL = env.get(
    'DJANGO_STATIC_URL',
    type=str,
    default='/static/',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = env.get(
    'DJANGO_STATICFILES_STORAGE',
    type=str,
    default='django.contrib.staticfiles.storage.StaticFilesStorage',
)


# AWS Configuration
DEFAULT_S3_PATH = "media"
STATIC_S3_PATH = "static"

AWS_ACCESS_KEY_ID = env.get('AWS_ACCESS_KEY_ID', type=str, default=None)
AWS_SECRET_ACCESS_KEY = env.get('AWS_SECRET_ACCESS_KEY', type=str, default=None)
AWS_STORAGE_BUCKET_NAME = env.get('AWS_STORAGE_BUCKET_NAME', type=str, default=None)
AWS_DEFAULT_REGION = env.get('AWS_DEFAULT_REGION', type=str, default=None)

# Boto config
AWS_REDUCED_REDUNDANCY = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = True
AWS_S3_SECURE_URLS = True
AWS_IS_GZIPPED = False
AWS_PRELOAD_METADATA = True
AWS_HEADERS = {
    "Cache-Control": "public, max-age=86400",
}

if AWS_DEFAULT_REGION:
    # Fix for https://github.com/boto/boto/issues/621
    AWS_S3_HOST = "s3-{0}.amazonaws.com".format(AWS_DEFAULT_REGION)


# DRF
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.DjangoFilterBackend',
    ),
}

# HUEY
HUEY = {
    'name': 'func_sig_registry',
    'connection': {
        'host': env.get('HUEY_REDIS_HOST', required=True),
        'port': env.get('HUEY_REDIS_PORT', type=int, default=6379),
    },
    'consumer': {
        'workers': env.get('HUEY_WORKER_COUNT', type=int, default=2),
        'worker_type': env.get('HUEY_WORKER_TYPE', default='greenlet'),
    },
}
