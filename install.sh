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

# Install python package
pip3 install -r requirements/common.txt

# Make config
sudo cp config_example.py config.py