from celery import Celery

BROKER_URL = 'redis://localhost:6379/0'
BACKEND_URL = 'redis://localhost:6379/1'

celery_app = Celery( 
    'celery_worker', # Name of the Celery app
    broker=BROKER_URL, # Redis broker URL, this is where Celery will look for tasks to execute
    backend=BACKEND_URL # Redis backend URL, this is where Celery will store the results of tasks
)

# Optional Celery configuration settings
celery_app.conf.update( 
    task_serializer="json", # Use JSON to serialize task arguments, which is a common and human-readable format for data exchange.
    result_serializer="json", # Use JSON to serialize task results, ensuring that the results are stored in a format that is easy to read and work with.
    accept_content=["json"], # Only accept tasks that are serialized in JSON format, which can help improve security by preventing the execution of tasks with unexpected or malicious payloads.
    task_track_started=True,# Track when a task starts
    result_expires=3600, # Results expire after 1 hour in the backend, so store results in database for 1 hour before they are deleted.
    worker_prefetch_multiplier=1, # Prevents one worker from grabbing too many tasks.
    # It ensures that each worker only fetches one task at a time, which can help improve performance and reduce latency when processing tasks.
    task_time_limit=600,        # Hard kill after 10 min (600 seconds)
    task_soft_time_limit=540,   # Graceful stop before hard kill
    task_acks_late=True, # Acknowledge tasks after they have been executed, which helps to ensure that tasks are not lost if a worker crashes while processing a task.
    task_reject_on_worker_lost=True, # If a worker is lost while processing a task, the task will be re-queued and sent to another worker for processing, which helps to ensure that tasks are not lost in case of worker failures.
    broker_connection_retry_on_startup=True # Retry connecting to the broker when the worker starts up, which can help to ensure that the worker is able to connect to the broker even if it is temporarily unavailable when the worker is starting.
)


# task_time_limit and task_soft_time_limit are important to prevent memory leaks, stuck LLM/API calls, and protect workers from infinite loops.



# This import is necessary to ensure that the tasks defined in tasks.py are registered with the Celery app.
# without this import, Celery would not be aware of the tasks and would not be able to execute them when they are called from the Flask app.
# import tasks

# ✅ Automatically discover tasks 
celery_app.autodiscover_tasks(['queuing'])


