#!/bin/bash

echo "Starting Flask API with Gunicorn..."

source venv/bin/activate

exec gunicorn app:app \
    --workers 2 \
    --bind 0.0.0.0:8000 \
    --timeout 120
