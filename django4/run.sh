#!/usr/bin/env bash

# exit on first error
set -e

# create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install (or update) requirements
pip install -r requirements.txt

./manage.py runserver