"""
WSGI config for func_sig_registry project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

import dotenv

from django.core.wsgi import get_wsgi_application

dotenv.load_dotenv('.env')  # Local overrides (not tracked)
dotenv.load_dotenv('.env_defaults')  # Development defaults (tracked)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "func_sig_registry.settings")

application = get_wsgi_application()
