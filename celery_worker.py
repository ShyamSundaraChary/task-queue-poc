from celery import Celery

# Celery configuration
# In a production environment, you would typically use environment variables for these settings.
# For this example, we're using Redis running locally on the default port.
# The broker is responsible for receiving and sending messages between the main application and the worker.
# The backend is where Celery stores the results of tasks. In this case, we're using Redis for both.
# Make sure to have Redis installed and running on your machine for this to work.

celery = Celery( 
    'report_tasks', # Name of the Celery app
    broker='redis://localhost:6379/0', # Redis broker URL
    backend='redis://localhost:6379/0' # Redis backend URL
)

# Optional Celery configuration settings
celery.conf.update(
    task_track_started=True,# Track when a task starts
    result_expires=3600, # Results expire after 1 hour
    worker_prefetch_multiplier=1, # Prevents one worker from grabbing too many tasks.
    worker_concurrency = 10 # Number of worker processes to run (adjust based on your machine's capabilities),

)

# Import tasks to ensure they are registered with Celery
# This import is necessary to ensure that the tasks defined in tasks.py are registered with the Celery app.
# without this import, Celery would not be aware of the tasks and would not be able to execute them when they are called from the Flask app.
import tasks
