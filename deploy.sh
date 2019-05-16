#!/bin/bash

# Install Supervisor
sudo apt-get install -y supervisor

# Install production requirements
sudo pip3 install -r requirements.txt

# Create production user
sudo -u postgres -H -- psql -c "SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'prod_user';" | grep -q 1 || sudo -u postgres -H -- psql -c  "CREATE ROLE prod_user LOGIN PASSWORD 'please_change_password';"

# Create production database if not exists
sudo -u postgres -H -- psql -c "SELECT 1 FROM pg_database WHERE datname = 'whereispts';" | grep -q 1 || sudo -u postgres -H -- psql -c  "CREATE DATABASE whereispts OWNER prod_user;"

# Create extension
sudo -u postgres -H -- psql -d whereispts -c "CREATE EXTENSION IF NOT EXISTS postgis;"

# Copy Supervisor config
sudo cp WhereIsPTS_API.conf /etc/supervisor/conf.d/WhereIsPTS_API.conf

# Make run_production executable
sudo chmod u+x boot.sh

# Migrate database to newest
env FLASK_CONFIG="production" sudo -E python3 manage.py db upgrade

# Start supervisor service
sudo supervisorctl reread
sudo service supervisor restart
