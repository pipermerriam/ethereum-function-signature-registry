This is how to do the ssl update every few months.

```
sudo certbot certonly --manual
h config:set LETS_ENCRYPT_SECRET="the-secret" LETS_ENCRYPT_SECRET_PATH="the path" DJANGO_SECURE_SSL_REDIRECT="False"
sudo heroku certs:update --app bytes4 /etc/letsencrypt/live/www.4byte.directory/fullchain.pem /etc/letsencrypt/live/www.4byte.directory/privkey.pem
```
