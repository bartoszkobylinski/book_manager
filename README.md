# BOOKS MANAGER

## Table of contents

* [General info] (#general-info)
* [Technologies] (#technologies)
* [Setup] (#setup)

## General info

Books manager is an app for manage books added by user or imported from Google API. User can filter and sort books.

## Technologies

* Python 3.8
* Django 3.1
* Django Rest Framework

## Setup

To run this project, clone repository:

and run:

```
$ sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
```

### CREATE POSTGRES DATABASE AND USER

Log in to an interactive Postgres session:

```
$ sudo -u postgres psql
```

Create database wit your name myproject:

```postgres
postgres=# CREATE DATABASE myproject;
```

Create user with your password:

```postgres
postgres=# CREATE USER myprojectuser WITH PASSWORD 'password';
```

Give to user all neede privileges:

```postgres
postgres=# GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
```

When you are finished exit out Postgres prompt by typing

```postgres
postgres=# \q
```

### CREATE VIRTUAL ENVIRONMENT

Create a virtual environment

```
$ python3 -m venv /path/to/new/virtual/env
```

Activate virtual environment

```
source ~/env_catalog_name/bin/activate
```

### STEPS WITH DJANGO SETTINGS

Install dependencies

```
$ pip install -r requirements.txt
```

Create json file with SECRET_KEY and credentials to Postgresql like:

```js
{
    "SECRET_KEY" : "your_secret_key",
    "NAME" : "myproject_name",
    "USER" : "user",
    "PASSWORD" : "password"
}
```

Change in CONSTANTS.py file in django project value of PATH_TO_CONFIG_SECRET_KEY_FILE to path to this json file

To run server locally

```
$ python manage.py runserver
```
