# Where is PTS

## Table of Contents

- [Where is PTS](#where-is-pts)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
    - [What is PTS](#what-is-pts)
  - [Installation](#installation)
    - [Dependencies](#dependencies)
    - [Environment](#environment)
  - [Usage](#usage)
  - [API documents](#api-documents)

## Introduction

Because many stores' TV channels are locked in specific junk information channels. So I decided to develop a map website to mark the stores that broadcast high-quality TV programs, so that everyone can search and return the store information.

Thanks for the Web service by NoobTW.

### What is PTS

PTS is 'Public Television Service Foundation'

This is [english link](http://eng.pts.org.tw/)



## Installation

### Dependencies

* PostgreSQL
* libpq-dev

```bash
# libpq-dev
sudo apt-get install libpq-dev
# PostgreSQL
sudo apt-get install postgresql postgresql-contrib
# PostGIS
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get update
sudo apt-get install postgis
# Supervisor
sudo apt-get install supervisor
```

### Environment

- **development**

    ```bash
    sh ./install.sh
    source pyenv/bin/activate
    pip install -r requirements/dev.txt
    ```

- **prodution**

    ```bash
    sh ./install.sh
    source pyenv/bin/activate
    pip install -r requirements/prod.txt
    ```

## Usage

1. **export environment**

```bash
export FLASK_CONFIG="<env>"
# `<env>` can be {development, testing, production, default}
# export FLASK_CONFIG="development"
```

2. **edit config.py**

```bash
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

## API documents

```sh
npm install -g aglio
# or you can use yarn add
aglio -i docs/api.apib --theme-template triple -o index.html
python -m http.server
```
