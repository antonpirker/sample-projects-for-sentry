#!/usr/bin/env bash

# exit on first error
set -e

# create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install (or update) requirements
pip install -r requirements.txt

cd movie_search && gunicorn project.asgi:application -k uvicorn.workers.UvicornWorker      