#!/usr/bin/env bash

# exit on first error
set -e

cd demosite

# activate virtual environment
source .venv/bin/activate

# Install (or update) requirements
pip install -r requirements.txt

./manage.py runserver 0.0.0.0:8000
