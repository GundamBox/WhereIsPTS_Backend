#!/bin/bash

# Run server
gunicorn "app:create_app(\"production\")" -b 127.0.0.1:8000 --reload --max-requests 1