# Where is PTS

## Introduction

本專案受[新聞頻道轉台運動](https://www.facebook.com/ChangeChannelMov/)所啟發，認為台灣人民應該拒看充斥垃圾資訊的新聞頻道，所以決定寫這個專案來紀錄全台灣有哪些小吃店在播放優質的公共電視節目，哪些小吃店拒絕客人轉台，還給大家清淨的用餐環境。

## Installation

```bash
sh ./build.sh
source pyenv/bin/activate
pip install -r requirements.txt
```

## Usage

`<env>` can be {dev, test, staging, prod}

1. **generate screte key**

```bash
python manage.py generate-key <env>
```

2. **run**

```bash
python manage.py run <env>
```

## What is PTS

PTS is [公共電視文化事業基金會](https://www.pts.org.tw/)