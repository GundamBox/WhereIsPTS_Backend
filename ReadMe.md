[![Build Status](https://travis-ci.com/GundamBox/WhereIsPTS_API.svg?branch=dev)](https://travis-ci.com/GundamBox/WhereIsPTS_API)
[![Coverage Status](https://coveralls.io/repos/github/GundamBox/WhereIsPTS_API/badge.svg?branch=dev)](https://coveralls.io/github/GundamBox/WhereIsPTS_API?branch=dev)

# Where is PTS

## Table of Contents

<!-- TOC -->

- [Where is PTS](#where-is-pts)
    - [Table of Contents](#table-of-contents)
    - [Introduction](#introduction)
        - [What is PTS](#what-is-pts)
    - [Installation](#installation)
        - [Dependencies](#dependencies)
        - [Environment](#environment)
    - [Usage](#usage)
        - [Deploy](#deploy)
        - [Development](#development)
        - [Run Unitttest](#run-unitttest)
    - [API documents](#api-documents)

<!-- /TOC -->

## Introduction

Because many stores' TV channels are locked in specific junk information channels. So I decided to develop a map website to mark the stores that broadcast high-quality TV programs, so that everyone can search and return the store information.

Thanks for the Web service by NoobTW.

### What is PTS

PTS is 'Public Television Service Foundation'

This is [english link](http://eng.pts.org.tw/)

## Installation

### Dependencies

* PostgreSQL
* Postgis
* libpq-dev

### Environment

1. **Edit env file**

    Copy `default env file` to `custom env file` and edit it.

    ```bash
    cp default_env.sh custom_env.sh
    ```
    
    - **VENV**
        python virtualenv directory path
    - **RECAPTCHA_PUBLIC_KEY**, **RECAPTCHA_PRIVATE_KEY**
        google recaptcha key
    - **PSQL_*_ROLE_NAME**, **PSQL_*_ROLE_PWD**, **PSQL_*_DB_NAME**
        postgresql role name, role password, database name 

2. **Install environment**

    ```bash
    ./install.sh
    ```

    If you encounter problems that cannot be executed, you can execute the `chmod + x ./install.sh` command to give the script executable permissions.

## Usage

### Deploy

1. **Edit config.py**

    ```bash
    vim config.py
    ```

2. **Deploy**

    ```bash
    ./deploy.sh
    ```

    If you encounter problems that cannot be executed, you can execute the `chmod + x ./deploy.sh` command to give the script executable permissions.

### Development

**Install dev package**

```bash
pip install -r requirements/dev.txt
```

### Run Unitttest

```bash
sh ./tests/build.sh
env FLASK_ENV='testing' coverage run --source=app tests/v1/api.py
coverage report
```

## API documents

```sh
npm install -g aglio
# or you can use yarn add
aglio -i docs/api.apib --theme-template triple -o index.html
python -m http.server
```
