import os

os.environ.setdefault('DJANGO_SECRET_KEY', 'not-a-real-secret-key')
os.environ.setdefault('DJANGO_ALLOWED_HOSTS', '*')
os.environ.setdefault('DJANGO_SECURE_SSL_REDIRECT', 'False')

from .settings import *  # NOQA
