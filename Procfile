heroku ps:scale web=1
web: gunicorn greenlife.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate