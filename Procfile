web: gunicorn bookstore.wsgi:bookstore --log-file=-
heroku ps:scale web=1
python manage.py migrate
