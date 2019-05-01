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

本專案受[新聞頻道轉台運動](https://www.facebook.com/ChangeChannelMov/)所啟發，認為台灣人民應該拒看充斥垃圾資訊的新聞頻道，所以決定寫這個專案來紀錄全台灣有哪些小吃店在播放優質的公共電視節目，哪些小吃店拒絕客人轉台，還給大家清淨的用餐環境。

感謝 NoobTW 提供網頁服務

### What is PTS

PTS is [公共電視文化事業基金會](https://www.pts.org.tw/)

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

1. **設定執行環境**

```bash
export FLASK_CONFIG="<env>"
# `<env>` can be {development, testing, production, default}
# export FLASK_CONFIG="development"
```

2. **設定 config.py**

```bash
vim config.py
```

3. **migrate database**

```bash
python manage.py db upgrade
```

4. **執行server**

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
