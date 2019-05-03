#!/bin/bash

# Set enivornment 
export FLASK_CONFIG="production"

# Run server
gunicorn "app:create_app()"