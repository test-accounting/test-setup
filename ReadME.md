# Ibuqa API Screening Test

A DjangoREST API with basic CRUD functionalities of adding customers and orders with integrated third party services:
-   `OpenID Connect`: implements authentication and authorization of users. The provider of choice being [Google](https://developers.google.com/identity/protocols/oauth2/openid-connect#python).
-   `SMS gateway`: enables sending of SMS alerts triggered by an event(adding an order). Development and testing implemented done in SANDBOX using [Africa's Talking API](https://africastalking.com/).
-   `CI/CD`: implements Continuous Integration, runs tests and Continous Deployment by [GitHub Actions](https://github.com/features/actions).

## Development
---

Create a python virtual environment.
- `Note`: used Ubuntu 20.04 for this project.
```
python3 -m venv virtual_environment_name
```

Clone the repository to your local machine
```
git clone https://github.com/kevogaba/ibuqa-api.git
```
Add the following key enviromental variables in `.env` file in the root of your project.
- Google OpenID Connect credentials
- Africa's talking credentials
- Database setting for Postgresql


### 1. Using Docker(Preferably)
---

First, you should build/ create image for the application using the `Dockerfile` in the root of the application.
```
docker-compose build
```

Then you launch the application in a detached mode. This will also pull the postgres image from dockerhub registry to be used as the database in your application.
```
docker-compose up -d
```

Then you run migrations to create the necessary table in the created database.
```
docker-compose exec ibuqa python manage.py migrate --noinput
```

Via the home page http://localhost:8000/ you can access and test the API on your browser.

Access the database by issuing the following command and applicable parameters:
```
docker-compose exec db --username=<> --dbname=<>
```

Your can view the logs of the containers running using:
```
docker-compose logs -f
```

Terminate the application by stopping the containers:
```
docker-compose down
```

When you make the changes in your application you will have to rebuild the image and it is advisable to get rid of the volumes before building new images. This can be done using the following commands:
```
docker-compose down -v
docker-compose up -d --build 
```


### 2. Local environment(Without use of docker)
---
Activate virtual environment in the directory with `env` folder.
```
. env/bin/activate
```

Install the requirements; make sure you are in the root folder of the applications to run these commands.
```
pip install --upgrade pip
pip install -r requirements.txt
```
Make sure you are connected to the database and it is accepting TCP/IP connection on the specified port if you are using `Postgres` database. You may also use the default `sqlite3` which does not require much configurations and you application will work just fine.

Make and run migrations to fire up the database before starting the application
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
The application will run in the link http://127.0.0.1:8000/ where you can perform various tests on the browser.


## Tests
---
Tests are exempted from authentication to ensure that they run successfully. They cover all the API endpoints, CRUD functionalities and related models.

You can perform unit tests with coverage, enabled by the `django_nose` package by running the command:
```
python manage.py test
```
Add or modify the tests in the `tests` folders inside each app.

Customise how the tests are run by declaring or removing arguements in NOSE_ARGS inside the `settings.py` file.


## CI/CD Pipeline
---
use github actions


## Contribution
---
Feel free to fork this repository and modify to your needs.

Happy coding!!!