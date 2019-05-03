#!/bin/bash

# Create production database if not exists
sudo -u postgres -H -- psql -c "SELECT 1 FROM pg_database WHERE datname = 'whereispts';" | grep -q 1 || sudo -u postgres -H -- psql -c  "CREATE DATABASE whereispts;"

# Install production requirements
source pyenv/bin/activate
sudo pip install -r reqirements.txt

# Set enivornment 
export FLASK_CONFIG="production"

# Migrate database to newest
python3 manage.py upgrade