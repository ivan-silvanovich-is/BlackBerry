# BlackBerry: Clothing store

This is an api for clothing store created with [Django](http://www.djangoproject.com) and [Django REST](https://www.django-rest-framework.org/) that you can use to handle backend functional for internet shop.

**NOTE:** This version was tested with Python 3.9, Django 4.1, DRF 3.13, PostgreSQL 13.4. And works only with **postgress** database currently.

## Quick demo

![alt text](https://drive.google.com/uc?export=view&id=1uRjtzZDl64S5uqzLtShyt1hDmKIX99AI "main")

![alt text](https://drive.google.com/uc?export=view&id=138jk7M8LszvfuTUdLjVhAhZDFJT4tkeK "products")

## Installing

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

```
virtualenv venv
```

That will create a new folder `venv` in your project directory. Next activate it with this command:

**mac/linux:** `source venv/bin/active`

**windows:** `venv\Scripts\active`

Install the project dependencies with

```
pip install -r requirements.txt
```

Your next step - connect a database. After installing PostgreSQL, configure your `.env` file and provide vital settings. Except for db settings, there are another important settings, like `SECRET_KEY`, provide them too. You can find an example of `.env` file in `.env.example` file:

```
# vital app settings
SECRET_KEY =        your secret key
DEBUG =             debug mode (0 - False, 1 - True)
ALLOWED_HOSTS =     allowed hosts (divided by spaces)

# admin app settings
LANGUAGE_CODE =     your language code in admin app ('en-us' for U.S. English)
TIME_ZONE =         your time zone ('UTC' for UTC+0)

# database settings
NAME =              name of database
HOST =              your db host ('localhost' for example)
PORT =              your db port ('5432' for example)
USER =              username of database owner
PASSWORD =          password of database owner
```

Then fill you database with test data (fixtures). This command will install all fixtures from all apps:

```
python manage.py loaddata fixtures.json
```

Now you can run the project with this command

```
python manage.py runserver
```

## Enjoy project 😁
