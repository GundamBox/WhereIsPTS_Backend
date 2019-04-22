# Where is PTS

## Table of Contents

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

- **development**

    ```bash
    sh ./build_venv.sh
    source pyenv/bin/activate
    pip install -r requirements/dev.txt
    ```

- **prodution**

    ```bash
    sh ./build_venv.sh
    source pyenv/bin/activate
    pip install -r requirements/prod.txt
    ```

- **heroku**

    ```bash
    sh ./build_venv.sh
    source pyenv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

1. **export environment**

```bash 
export FLASK_CONFIG="<env>"
# `<env>` can be {development, testing, production, heroku, default}
# export APP_SETTINGS="prod"
```

2. **edit config.py**

```bash
cp config_example.py config.py
vim config.py
```

3. **migrate database**

```bash
python manage.py db upgrade
```

4. **run**

```bash
python manage.py run
```