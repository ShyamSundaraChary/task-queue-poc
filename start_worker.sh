#!/bin/bash

source venv/bin/activate
celery -A celery_worker.celery worker --loglevel=info --concurrency=10

# For auto-scaling workers, you can use the following command instead:
# celery -A celery_worker.celery worker --autoscale=10,2 --loglevel=info
# here maximum number of workers is 10 and minimum is 2. 