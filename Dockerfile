FROM python:3.9-slim-buster

RUN pip install --upgrade pip


COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./bold /app

WORKDIR /app

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
