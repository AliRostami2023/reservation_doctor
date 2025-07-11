#!/bin/sh

export PYTHONPATH=/app

echo "Waiting for Postgres to be ready..."
while ! nc -z $DATABASE_HOST 5432; do
  sleep 1
done

echo "Collecting static files..."
python manage.py collectstatic --noinput || exit 1

echo "Running database migrations..."
python manage.py migrate --noinput || exit 1

echo "Starting Gunicorn..."
exec gunicorn config.wsgi --bind 0.0.0.0:8000
