# customer geocoder

Django REST API which provides information about customers

python manage.py migrate
python manage.py createsuperuser --email admin@example.com --username admin
python manage.py makemigrations api
python manage.py migrate
python manage.py customers_from_csv ./oowlish~/customers_geocoded.csv

heroku create app-name
heroku config:set SECRET_KEY=SOME_SECRET_VALUE
heroku config:set DEPLOY_HOST=APP_URL
heroku config:set PRODUCTION=1

```yml
# heroku.yml
build:
  docker:
    web: Dockerfile
```

git add heroku.yml
git commit -m "add heroku.yml"

heroku stack:set container -a app-name
heroku plugins:install @heroku-cli/plugin-manifest
heroku git:remote -a customer-geocoder
git push heroku main

heroku run python manage.py makemigrations
heroku run python manage.py makemigrations api
heroku run python manage.py migrate
heroku run python manage.py createsuperuser --email admin@example.com --username admin
heroku run python manage.py customers_from_csv customers_geocoded.csv
heroku auth:token
