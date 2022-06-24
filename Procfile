web: gunicorn bookstore.wsgi --log-file=-
heroku ps:scale web=1
python bookstore/manage.py migrate
