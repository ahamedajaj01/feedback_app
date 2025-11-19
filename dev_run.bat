@echo off
REM Run Django using a custom settings file
python manage.py runserver 8000 --settings=feedback.settings
pause
