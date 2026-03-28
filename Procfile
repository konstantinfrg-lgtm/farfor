release: python manage.py migrate --noinput
web: gunicorn milkers_collection.wsgi --bind 0.0.0.0:$PORT
