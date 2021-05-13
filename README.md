# customer geocoder

Django REST API which provides information about customers

python manage.py migrate
python manage.py createsuperuser --email admin@example.com --username admin
python manage.py makemigrations api
python manage.py migrate
python manage.py customers_from_csv ./oowlish~/customers_geocoded.csv

heroku create app-name
heroku config:set SECRET_KEY=SOME_SECRET_VALUE -a app-name
heroku config:set DEPLOY_HOST=APP_URL -a app-name
heroku config:set PRODUCTION=1 -a app-name

```yml
# heroku.yml
build:
  docker:
    web: Dockerfile
```

git add heroku.yml
git commit -m "Add heroku.yml"

heroku stack:set container -a app-name
heroku plugins:install @heroku-cli/plugin-manifest
heroku git:remote -a customer-geocoder
git push heroku main
