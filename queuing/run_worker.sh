#!/bin/bash

echo "Starting Celery Worker..."

# Activate virtualenv
source venv/bin/activate


celery -A queuing.celery_worker.celery_app worker --loglevel=info --concurrency=10 -E

# For auto-scaling workers, you can use the following command instead:
# celery -A queuing.celery_worker.celery_app worker --autoscale=10,2 --loglevel=info
# here maximum number of workers is 10 and minimum is 2. 


# -A flag tells Celery where to find the application instance. In this case, it's looking for a module named queuing.celery_worker and an application object named celery_app within that module.

# -E flag is used to enable events, which allows you to monitor task execution in real-time using tools like Flower.

# concurrency flag is used to specify the number of worker processes to run. Adjust this based on your system's capabilities and workload requirements.

# loglevel flag is used to set the logging level. 'info' will provide detailed logs about task execution, which can be helpful for debugging and monitoring.