web: gunicorn --bind 0.0.0.0:$PORT bookstore.wsgi
heroku ps:scale web=1
python manage.py migrate
