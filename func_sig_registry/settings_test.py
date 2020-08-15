import os
import getpass

os.environ.setdefault('DJANGO_SECRET_KEY', 'not-a-real-secret-key')
os.environ.setdefault('DJANGO_ALLOWED_HOSTS', '*')
os.environ.setdefault('DJANGO_SECURE_SSL_REDIRECT', 'False')
os.environ.setdefault('REDIS_URL', 'redis://localhost:6379')
os.environ.setdefault(
    'DATABASE_URL',
    'postgres://postgres:postgres@localhost/func_sig_registry',
    # 'postgres://{user}@localhost/func_sig_registry'.format(user=getpass.getuser()),
)
os.environ.setdefault('ROLLBAR_ACCESS_TOKEN', 'not-a-real-access-token')
os.environ.setdefault('ROLLBAR_ENVIRONMENT', 'test')

from .settings import *  # NOQA
