import os

os.environ.setdefault('DJANGO_SECRET_KEY', 'not-a-real-secret-key')
os.environ.setdefault('DJANGO_ALLOWED_HOSTS', '*')
os.environ.setdefault('DJANGO_SECURE_SSL_REDIRECT', 'False')
os.environ.setdefault('HUEY_REDIS_HOST', '127.0.0.1')

from .settings import *  # NOQA
