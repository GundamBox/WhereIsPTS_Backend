# Where is PTS

## Introduction

Because many stores' TV channels are locked in specific junk information channels. So I decided to develop a map website to mark the stores that broadcast high-quality TV programs, so that everyone can search and return the store information.

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

PTS is 'Public Television Service Foundation'

This is [english link](http://eng.pts.org.tw/)