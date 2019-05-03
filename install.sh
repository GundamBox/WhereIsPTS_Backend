#!/bin/bash

# Python
sudo apt-get install -y python3 python3-dev python3-pip

# libpq-dev
sudo apt-get install -y libpq-dev

# PostgreSQL
sudo apt-get install -y postgresql postgresql-contrib
# PostGIS
sudo add-apt-repository -y ppa:ubuntugis/ppa
sudo apt-get update
sudo apt-get install -y postgis

# Supervisor
sudo apt-get install -y supervisor
# Virtualenv
sudo apt-get install -y virtualenv

# Install python common package
virtualenv pyenv --python=python3
source pyenv/bin/activate
pip install -r requirements/common.txt

# Make config
sudo cp config_example.py config.py

# Copy Supervisor config
sudo cp WhereIsPTS_API.conf /etc/supervisor/conf.d/WhereIsPTS_API.conf

# Make run_production executable
sudo chmod u+x boot.sh