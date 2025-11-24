# Procfile (used by Railway or Heroku)
# -----------------------------------
# This file tells the hosting platform how to run our Django app.
#
# 1) `release:` runs BEFORE each deploy. 
#    We use it to run database migrations so new models/tables are created.
#
# 2) `web:` is the actual command that starts the Django server.
#
# Important:
# - File name must be exactly "Procfile" with NO extension.
# - This must be in the root folder (same level as manage.py).
# - Railway automatically reads these commands during deployment.

release: python manage.py migrate
web: gunicorn yourproject.wsgi

