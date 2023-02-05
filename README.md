# BlackBerry: Clothing store

This is an api for a clothing store created with [Django](http://www.djangoproject.com) and [Django REST](https://www.django-rest-framework.org/) that you can use to handle backend functional for the internet shop.

**NOTE:** This version was tested with Python 3.9, Django 4.1, DRF 3.13, PostgreSQL 15.1. And works only with **postgress** database currently.

## Quick demo

![alt text](https://drive.google.com/uc?export=view&id=1uRjtzZDl64S5uqzLtShyt1hDmKIX99AI "main")

![alt text](https://drive.google.com/uc?export=view&id=1vSMFiiZit2JqDqeoypSg-8Nd-bzbqlI8 "products")

## Installing

To get this project up and running you should install [Docker](https://www.docker.com/products/docker-desktop/). Make sure you have Docker on your OS before you move on to the next step.


In the case you have Docker your next step is to configure a `.env` file and provide vital settings. Except for db settings, there are another important settings, like `SECRET_KEY`, email settings, etc., provide them too. You can find an example of `.env` file in `.env.example` file:

```
# api prefix
API_PREFIX=api/v1/                     # the prefix that each api begins with

# vital app settings
SECRET_KEY='secret_key'                # your secret key
DEBUG=1                                # a debug mode preference (0 - False, 1 - True)
ALLOWED_HOSTS='127.0.0.1 localhost'    # allowed hosts (divided by spaces)

# admin app settings
LANGUAGE_CODE=en                       # your language code in admin app ('en-us' for U.S. English)
TIME_ZONE=Europe/London                # your time zone ('UTC' for UTC+0)

# database settings
DB_NAME=my_db                          # the name of the database
DB_HOST=127.0.0.1                      # your db host ('localhost' for example)
DB_PORT=5432                           # your db port ('5432' for example)
DB_USER=user                           # username of database owner
DB_PASSWORD=1234                       # password of database owner

# email settings
EMAIL_HOST=smtp.gmail.com              # the email server which serves site's email address
EMAIL_PORT=587                         # the port of the server which accept connections
EMAIL_USE_TLS=1                        # using of TLS preference (0 - False, 1 - True)
EMAIL_HOST_USER=my.store@gmail.com     # site's email address
EMAIL_HOST_PASSWORD=1234               # the email password to access the email address
```

Preparations are almost done. The final step is to run Docker containers. Just type the next command in the project work directory:

```
docker-compose -f .\docker-compose.dev.yaml up -d
```

If you want to start the project in a production mode, just use `docker-compose.prod.yaml` instead of `docker-compose.dev.yaml` command.

## Enjoy the project 😁
