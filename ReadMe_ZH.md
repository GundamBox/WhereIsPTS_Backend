# Where is PTS

## Table of Contents

* [Introduction](#Introduction)
    * [What is PTS](#What_is_PTS)
* [Dependencies](#Dependencies)
* [Installation](#Installation)
* [Usage](#Usage)

## Introduction

本專案受[新聞頻道轉台運動](https://www.facebook.com/ChangeChannelMov/)所啟發，認為台灣人民應該拒看充斥垃圾資訊的新聞頻道，所以決定寫這個專案來紀錄全台灣有哪些小吃店在播放優質的公共電視節目，哪些小吃店拒絕客人轉台，還給大家清淨的用餐環境。

感謝 NoobTW 提供網頁服務

### What is PTS

PTS is [公共電視文化事業基金會](https://www.pts.org.tw/)

## Dependencies

* PostgreSQL
* libpq-dev

## Installation

- **development**

    ```bash
    sh ./build.sh
    source pyenv/bin/activate
    pip install -r requirements/dev.txt
    ```

- **prodution**

    ```bash
    sh ./build.sh
    source pyenv/bin/activate
    pip install -r requirements/prod.txt
    ```

- **heroku**

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

