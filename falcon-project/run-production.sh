#!/usr/bin/env bash
set -e

pip install -r requirements.txt

gunicorn \
    --workers=16 \
    --timeout=1 \
    -b 127.0.0.1:8000 \
    falcon-project:app
#    2>> falcon-project-err.log 1>> falcon-project-out.log

