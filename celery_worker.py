from celery import Celery


celery = Celery( 
    'report_tasks', # Name of the Celery app
    broker='redis://localhost:6379/0', # Redis broker URL, this is where Celery will look for tasks to execute
    backend='redis://localhost:6379/0' # Redis backend URL, this is where Celery will store the results of tasks
)

# Optional Celery configuration settings
celery.conf.update(
    task_track_started=True,# Track when a task starts
    result_expires=3600, # Results expire after 1 hour in the backend, so store results in database for 1 hour before they are deleted.
    worker_prefetch_multiplier=1 # Prevents one worker from grabbing too many tasks.
    # It ensures that each worker only fetches one task at a time, which can help improve performance and reduce latency when processing tasks.
)

# This import is necessary to ensure that the tasks defined in tasks.py are registered with the Celery app.
# without this import, Celery would not be aware of the tasks and would not be able to execute them when they are called from the Flask app.
import tasks
