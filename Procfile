web: gunicorn func_sig_registry.wsgi -c func_sig_registry/gunicorn.conf -w 3
worker: python manage.py run_huey --verbosity=3
