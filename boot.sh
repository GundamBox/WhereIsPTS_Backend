#!/bin/bash

# Set enivornment 
export FLASK_CONFIG="production"

# Run server
gunicorn "app:create_app()" -b 127.0.0.1:8000 –reload –max-requests 1