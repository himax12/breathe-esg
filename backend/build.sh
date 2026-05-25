#!/bin/bash
set -e
echo "Running migrations..."
python manage.py migrate --noinput
echo "Seeding flag rules..."
python manage.py seed_flag_rules
echo "Build complete."