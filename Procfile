web: gunicorn bookstore.wsgi:app --log-file=-
heroku ps:scale web=1
python manage.py migrate
