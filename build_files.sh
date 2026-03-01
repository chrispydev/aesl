#!/bin/bash

# Exit on error
set -e

# Install dependencies (Vercel already does pip install -r requirements.txt, but we ensure)
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput
