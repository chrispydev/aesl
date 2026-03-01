#!/bin/bash

set -e

echo "Python version:"
python --version

echo "uv version:"
uv --version || echo "uv not found (should be available)"

echo "Installing dependencies with uv..."
uv pip install --system -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Build complete!"
