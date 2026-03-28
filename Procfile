release: python manage.py migrate --noinput && python manage.py createsuperuser --noinput || true
web: gunicorn milkers_collection.wsgi --bind 0.0.0.0:$PORT
