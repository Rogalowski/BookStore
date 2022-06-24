web: gunicorn books.wsgi --log-file=-
heroku ps:scale web=1
python manage.py migrate
