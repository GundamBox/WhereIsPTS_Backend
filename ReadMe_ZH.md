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
        - [佈署](#佈署)
        - [開發](#開發)
        - [執行單元測試](#執行單元測試)
    - [API documents](#api-documents)

<!-- /TOC -->

## Introduction

本專案受[新聞頻道轉台運動](https://www.facebook.com/ChangeChannelMov/)所啟發，認為台灣人民應該拒看充斥垃圾資訊的新聞頻道，所以決定寫這個專案來紀錄全台灣有哪些小吃店在播放優質的公共電視節目，哪些小吃店拒絕客人轉台，還給大家清淨的用餐環境。

感謝 NoobTW 提供網頁服務

### What is PTS

PTS is [公共電視文化事業基金會](https://www.pts.org.tw/)

## Installation

### Dependencies

* PostgreSQL
* Postgis
* libpq-dev

### Environment

1. 設定變數

    複製`default env file` 命名為 `custom env file` 並編輯。

    ```bash
    cp default_env.sh custom_env.sh
    ```

    - **VENV**
        python virtualenv 資料夾路徑
    - **RECAPTCHA_PUBLIC_KEY**, **RECAPTCHA_PRIVATE_KEY**
        google recaptcha 金鑰
    - **PSQL_*_ROLE_NAME**, **PSQL_*_ROLE_PWD**, **PSQL_*_DB_NAME**
        postgresql 使用者名稱, 密碼, 資料庫名稱

2. **安裝一般環境**

    ```bash
    sh ./install.sh
    ```

    如果遇到無法執行的問題，可以執行`chmod + x ./install.sh`命令為腳本提供可執行權限。

## Usage

### 佈署

1. **編輯 config.py**

    ```bash
    vim config.py
    ```

2. **部署**

    ```bash
    sh ./deploy.sh
    ```

    如果遇到無法執行的問題，可以執行`chmod + x ./deploy.sh`命令為腳本提供可執行權限。

### 開發

**安裝開發用套件**

```bash
pip install -r requirements/dev.txt
```

### 執行單元測試

```bash
sh ./tests/build.sh
env FLASK_ENV='testing' sudo -E python manage.py test
```

## API documents

    ```sh
    npm install -g aglio
    # or you can use yarn add
    aglio -i docs/api.apib --theme-template triple -o index.html
    python -m http.server
    ```
