# Where is PTS

## Table of Contens

* [Introduction](#Introduction)
    * [What is PTS](#What_is_PTS)
* [Dependencies](#Dependencies)
* [Installation](#Installation)
* [Usage](#Usage)

## Introduction

Because many stores' TV channels are locked in specific junk information channels. So I decided to develop a map website to mark the stores that broadcast high-quality TV programs, so that everyone can search and return the store information.

Thanks for the Web service by NoobTW.

### What is PTS

PTS is 'Public Television Service Foundation'

This is [english link](http://eng.pts.org.tw/)

## Dependencies

* PostgreSQL
* libpq-dev

## Installation

```bash
sh ./build.sh
source pyenv/bin/activate
pip install -r requirements.txt
```

## Usage

1. **Setup env**

```bash 
export APP_SETTINGS="<env>"
# `<env>` can be {dev, test, staging, prod}
# export APP_SETTINGS="prod"
```

2. **generate screte key**

```bash
python manage.py generate-key
```

3. **edit database connection string**

```bash
vim app/settings/<env>.ini
```

Ex: `vim app/settings/dev.ini`

```ini
#dev.ini
[FLASK]
HOST = 0.0.0.0
PORT = 8080
ENV = development
DEBUG = true
TESTING = true
SECRET_KEY = please_generate_secret_string
# setup user_name and user_password
SQLALCHEMY_DATABASE_URI = postgresql://<user_name>:<user_password>@localhost/whereispts
```

4. **migrate database**

```bash
python manage.py db upgrade
```

5. **run**

```bash
python manage.py run
```