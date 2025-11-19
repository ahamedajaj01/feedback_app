# PRODUCTION.md — Beginner-friendly deployment notes

## Purpose
Short, clear reference for deploying this Django app to Railway.

## Important rules
- Never commit secrets.
- Local uses dev settings; Railway uses prod settings.
- Packages must be in requirements.txt.

## Railway Environment Variables
(Replace placeholders)

DJANGO_SECRET_KEY=REPLACE
DJANGO_SETTINGS_MODULE=feedback.prod_settings
DJANGO_DEBUG=False
ALLOWED_HOSTS=.railway.app,yourdomain.com

MYSQL_DATABASE=...
MYSQL_USER=...
MYSQL_PASSWORD=...
MYSQL_HOST=...
MYSQL_PORT=...

SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://your-railway-domain
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=StrongPassword123

## Start Command
python manage.py collectstatic --noinput --settings=feedback.prod_settings && python -c "import os,django; os.environ.setdefault('DJANGO_SETTINGS_MODULE','feedback.prod_settings'); django.setup(); from django.contrib.auth import get_user_model; U=get_user_model(); u=os.environ.get('DJANGO_SUPERUSER_USERNAME'); e=os.environ.get('DJANGO_SUPERUSER_EMAIL'); p=os.environ.get('DJANGO_SUPERUSER_PASSWORD'); 0 if (u and p and U.objects.filter(username=u).exists()) else (U.objects.create_superuser(u,e,p) if u and p else None)" && python -m gunicorn feedback.wsgi:application --bind 0.0.0.0:$PORT

## Local workflow
python manage.py runserver --settings=feedback.settings
python manage.py migrate

## Deployment summary
1. Push to GitHub
2. Railway → Deploy from GitHub
3. Add MySQL database
4. Add ENV variables
5. Set Start Command
6. Deploy
7. Visit /admin/
