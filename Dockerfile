FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /bookstore

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY bookstore .

RUN mkdir -p /vol/web/
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/database

RUN adduser -D user
# CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8080

# EXPOSE 8080