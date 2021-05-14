FROM python:3.8-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps


COPY ./requirements.txt .
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

COPY ./customer_geocoder ./customer_geocoder
COPY ./manage.py .
COPY ./files/*.csv .

RUN python manage.py collectstatic --noinput

USER 1001

CMD gunicorn customer_geocoder.wsgi:application --bind 0.0.0.0:$PORT
