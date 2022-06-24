web: gunicorn bookstore.bookstore.wsgi --log-file=-
heroku ps:scale web=1
python manage.py migrate
