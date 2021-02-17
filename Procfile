heroku ps:scale web=4
heroku config:set DISABLE_COLLECTSTATIC=1
web: gunicorn greenlife.wsgi:application --log-file - --log-level debug
manage.py migrate