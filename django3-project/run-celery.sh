#!/usr/bin/env bash

# exit on first error
set -e

cd demosite

# activate virtual environment
source .venv/bin/activate

# Install (or update) requirements
pip install -r requirements.txt

# Start Redis server in background
redis-server &

# Start Celery
celery --app demosite worker --loglevel INFO