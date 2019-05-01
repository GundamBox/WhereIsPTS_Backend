#!/bin/bash

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

# Make run_production executable
sudo chmod u+x boot_production.sh

# Install python common package
virtualenv pyenv --python=python3
source pyenv/bin/activate
pip install -r requirements/common.txt

# Make config
cp config_example.py config.py