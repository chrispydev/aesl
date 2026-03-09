#!/usr/bin/env bash
# build.sh
set -e

python -m pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
