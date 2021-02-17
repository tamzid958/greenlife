web: gunicorn greenlife.wsgi --log-file -
heroku config:set DISABLE_COLLECTSTATIC= 1
heroku ps:scale web= 1