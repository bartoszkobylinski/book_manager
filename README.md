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

```
postgres=# GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
```






Create a virtual environment

```
$ python3 -m venv /path/to/new/virtual/env
```
Activate virtual environment
```
source ~/env_catalog_name/bin/activate
```
install depencies 

```
$ cd ../mountain_weather
$ pip install -r requirements.txt
```
install virtual environment
```
export DB_NAME='name of your database'
export DB_USER='name of user'
export DB_PASS='password'
export ACCU_API_KEY='your api key on accu weather services'
export DB_HOST='localhost'
export PATH_SCRAPER='path to chromedriver file on your computer'
```
To run server locally

```
$ python manage.py runserver
```
