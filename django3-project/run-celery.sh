#!/usr/bin/env bash

set -e

redis-server &

cd demosite

celery --app demosite worker --loglevel INFO