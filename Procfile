web: gunicorn -w 2 -b 0.0.0.0:8000 --chdir /mnt/WindowsDaneNTFS/Programowanie/BookStore/bookstore bookstore.wsgi --reload --timeout 900
heroku ps:scale web=1
python manage.py migrate
