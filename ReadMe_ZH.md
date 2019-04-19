# Where is PTS

## Table of Contens

* [Introduction](#Introduction)
    * [What is PTS](#What_is_PTS)
* [Dependencies](#Dependencies)
* [Installation](#Installation)
* [Usage](#Usage)

## Introduction

本專案受[新聞頻道轉台運動](https://www.facebook.com/ChangeChannelMov/)所啟發，認為台灣人民應該拒看充斥垃圾資訊的新聞頻道，所以決定寫這個專案來紀錄全台灣有哪些小吃店在播放優質的公共電視節目，哪些小吃店拒絕客人轉台，還給大家清淨的用餐環境。

### What is PTS

PTS is [公共電視文化事業基金會](https://www.pts.org.tw/)

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

1. **設定執行環境**

```bash 
export APP_SETTINGS="<env>"
# `<env>` can be {dev, test, staging, prod}
# export APP_SETTINGS="prod"
```

2. **產生 screte key**

```bash
python manage.py generate-key
```

3. **設定連線字串**

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
# 設定使用者名稱與密碼
SQLALCHEMY_DATABASE_URI = postgresql://<user_name>:<user_password>@localhost/whereispts
```

4. **migrate database**

```bash
python manage.py db upgrade
```

5. **執行server**

```bash
python manage.py run
```

