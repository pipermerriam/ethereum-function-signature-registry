import os

os.environ.setdefault('DJANGO_SECRET_KEY', 'not-a-real-secret-key')
os.environ.setdefault('DJANGO_ALLOWED_HOSTS', '*')

from .settings import *  # NOQA
