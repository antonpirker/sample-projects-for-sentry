#!/usr/bin/env bash

# exit on first error
set -e

redis-server &

cd demosite

celery --app demosite worker --loglevel INFO