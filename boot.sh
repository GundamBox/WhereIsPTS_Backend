#!/bin/bash

# Set enivornment 
export FLASK_CONFIG="production"

# Run server
pyenv/bin/gunicorn "app:create_app()"