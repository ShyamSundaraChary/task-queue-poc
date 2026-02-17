#!/bin/bash

source venv/bin/activate
celery -A celery_worker.celery flower --port=5555