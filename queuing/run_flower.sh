#!/bin/bash

echo "Starting Celery Flower..."

celery  -A queuing.celery_worker.celery_app flower --port=5555

# chmod +x run_flower.sh
# Make the script executable without typing "bash" before it.
