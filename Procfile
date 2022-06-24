release: python bookstore/manage.py migrate & runserver
web:
 gunicorn bookstore.wsgi --log-file=-
