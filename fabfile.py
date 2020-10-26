import tempfile
import secrets
import pathlib
import string

from fabric import task



PYTHON_VERSION = "3.7.9"


@task
def provision(conn, domain):
    postgres_password = "".join((
        secrets.choice(string.ascii_letters + string.digits)
        for _ in range(12)
    ))
    django_secret_key = "".join((
        secrets.choice(string.ascii_letters + string.digits)
        for _ in range(64)
    ))

    # Install apt deps
    apt_deps = " ".join(APT_DEPENDENCIES)
    conn.run(f"apt install -y {apt_deps}")

    # Setup PyEnv
    conn.run("curl https://pyenv.run | bash")
    _append_bashrc(conn, PYENV_BASHRC)
    conn.run(f"pyenv install {PYTHON_VERSION}")
    conn.run(f"pyenv global {PYTHON_VERSION}")

    # Create the `web` user with their own home director and group
    conn.run("useradd --create-home --user-group web")

    # Clone the repository
    conn.run("git clone https://github.com/pipermerriam/ethereum-function-signature-registry.git /home/web/ethereum-function-signature-registry")

    #
    # Setup and Install project dependencies
    #
    conn.run("pip install virtualenv")
    conn.run("python -m virtualenv /home/web/venv")

    conn.run("/home/web/venv/bin/pip install -r /home/web/ethereum-function-signature-registry/requirements.txt")

    with tempfile.TemporaryDirectory() as base_path:
        dotenv_file_path = pathlib.Path(base_path) / '.env'
        dotenv_file_path.write_text(DOTENV.format(
            DOMAIN=domain,
            POSTGRES_PASSWORD=postgres_password,
            SECRET_KEY=django_secret_key,
        ))

        conn.put(str(dotenv_file_path), remote='/home/web/ethereum-function-signature-registry/.env')


     Setup Postgres User and Database

    with tempfile.TemporaryDirectory() as base_path:
        # systemd service for worker
        pgpass_file_path = pathlib.Path(base_path) / '.pgpass'
        pgpass_file_path.write_text(f"*.*.*.bytes4.{postgres_password}")

        conn.put(str(pgpass_file_path), remote='/root/.pgpass')
        conn.run("chmod 600 /root/.pgpass")

    conn.run(f"sudo -u postgres psql -c \"CREATE ROLE bytes4 PASSWORD '{postgres_password}' SUPERUSER LOGIN;\"")
    conn.run("sudo -u postgres createdb --no-password bytes4")

    #
    # Setup Redis
    #
    conn.run('sed -i "s/supervised no/supervised systemd/g" /etc/redis/redis.conf')
    conn.run("service redis restart")

    #
    # Setup config files for uwsgi/nginx/4byte-worker
    #
    with tempfile.TemporaryDirectory() as base_path:
        # systemd service for worker
        worker_service_file_path = pathlib.Path(base_path) / '4byte.service'
        worker_service_file_path.write_text(SYSTEMD_WORKER_SERVICE)

        conn.put(str(worker_service_file_path), remote='/etc/systemd/system/4byte.service')

        # nginx configuration file
        nginx_4byte_conf = pathlib.Path(base_path) / '4byte'
        nginx_4byte_conf.write_text(NGINX_4BYTE.format(DOMAIN=domain))

        conn.put(str(nginx_4byte_conf), remote='/etc/nginx/sites-available/4byte')
        conn.run('ln -s /etc/nginx/sites-available/4byte /etc/nginx/sites-enabled/')

        # uwsgi configuration file
        uwsgi_4byte_conf = pathlib.Path(base_path) / '4byte.ini'
        uwsgi_4byte_conf.write_text(UWSGI_CONF)

        conn.put(str(uwsgi_4byte_conf), remote='/etc/uwsgi/apps-available/4byte.ini')
        conn.run('ln -s /etc/uwsgi/apps-available/4byte.ini /etc/uwsgi/apps-enabled/')




def _append_bashrc(conn, content: str) -> None:
    for line in content.splitlines():
        if not line:
            continue
        conn.run(line)
        conn.run(f"echo '{line}' >> /root/.bashrc")


APT_DEPENDENCIES = (
    # build
    "automake",
    "build-essential",
    "curl",
    "gcc",
    "git",
    "gpg",
    "software-properties-common",
    "pkg-config",
    "zlib1g",
    "zlib1g-dev",
    "libbz2-dev",
    "libreadline-dev",
    "libssl-dev",
    "libsqlite3-dev",
    "libffi-dev",
    # application
    "nginx",
    "uwsgi",
    "uwsgi-plugin-python3",
    "redis-server",
    "postgresql",
    "postgresql-contrib",
    "postgresql-server-dev-11",
    # convenience
    "htop",
    "tmux",
)


SYSTEMD_WORKER_SERVICE = """[Unit]
Description=4byte worker
After=network.target
StartLimitIntervalSec=0

[Service]
WorkingDirectory=/home/web/ethereum-function-signature-registry
Type=simple
Restart=always
RestartSec=1
User=web
ExecStartPre=
ExecStart=/home/web/venv/bin/python /home/web/ethereum-function-signature-registry/manage.py run_huey --verbosity 3
"""


PYENV_BASHRC = """export PATH="/root/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
"""

NGINX_4BYTE = """server {{
    server_name {DOMAIN};

    listen 80;
    listen [::]:80;

    if ($host = {DOMAIN}) {{
        return 301 https://$host$request_uri;
    }} # managed by Certbot

    return 404; # managed by Certbot
}}


server {{
    server_name {DOMAIN}; # customize with your domain name

    location / {{
        # django running in uWSGI
        uwsgi_pass unix:///run/uwsgi/app/4byte/socket;
        include uwsgi_params;
        uwsgi_read_timeout 300s;
        client_max_body_size 32m;
    }}

    # location /static/ {{
    #    # static files
    #    alias /home/web/static/; # ending slash is required
    # }}

    # location /media/ {{
    #     # media files, uploaded by users
    #     alias /home/web/media/; # ending slash is required
    # }}

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/{DOMAIN}/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/{DOMAIN}/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


}}
"""


UWSGI_CONF = """[uwsgi]
plugin=python3
uid=web
chdir=/home/web/ethereum-function-signature-registry
module=func_sig_registry.wsgi:application
master=True
vacuum=True
max-requests=5000
processes=4
virtualenv=/home/web/venv
"""


DOTENV = """DATABASE_URL=postgres://bytes4:{POSTGRES_PASSWORD}@127.0.0.1:5432/bytes4
DJANGO_ALLOWED_HOSTS={DOMAIN}
DJANGO_DEBUG=False
DJANGO_DEBUG_TOOLBAR_ENABLED=False
DJANGO_SECRET_KEY={SECRET_KEY}
DJANGO_SECURE_SSL_REDIRECT=False
HUEY_WORKER_TYPE=thread
REDIS_URL=redis://127.0.0.1:6379
"""
