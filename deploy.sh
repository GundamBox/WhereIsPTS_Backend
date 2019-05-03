#!/bin/bash

# Create production user
sudo -u postgres -H -- psql -c "SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = 'pts';" | grep -q 1 || sudo -u postgres -H -- psql -c  "CREATE ROLE user LOGIN PASSWORD 'please_change_password';"

# Create production database if not exists
sudo -u postgres -H -- psql -c "SELECT 1 FROM pg_database WHERE datname = 'whereispts';" | grep -q 1 || sudo -u postgres -H -- psql -c  "CREATE DATABASE whereispts OWNER user;"

# Create extension
sudo -u postgres -H -- psql -d whereispts -c "CREATE EXTENSION postgis;"

# Install production requirements
sudo pip3 install -r requirements.txt

# Migrate database to newest
env FLASK_CONFIG="production" sudo -E python3 manage.py db upgrade