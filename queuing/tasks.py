import time
from queuing.celery_worker import celery_app


@celery_app.task(
    bind=True, # Bind the task to the current instance, allowing access to self for retrying and other task-related information.
    autoretry_for=(Exception,), # Automatically retry the task for any exception that occurs during execution.
    retry_delay=60, # Wait 60 seconds before retrying the task after a failure
    retry_backoff=True, # Enable exponential backoff for retries, which means that the delay between retries will increase exponentially (e.g., 60s, 120s, 240s) to avoid overwhelming the system with rapid retries.
    retry_backoff_max=300, # Maximum delay for exponential backoff is 5 minutes (300 seconds), which prevents the delay from growing indefinitely in case of persistent failures.
    retry_kwargs={"max_retries": 3}, # Maximum number of retries
)
def generate_report(self, startup_name):
    print(f"Starting report for {startup_name}")

    # Simulating multi-step LLM process
    for step in range(5):
        print(f"{startup_name}: Step {step+1}")
        time.sleep(10)  # Simulate API call

    result = f"Report generated for {startup_name}"
    return result

# Each task run total of 50 seconds (5 steps x 10 seconds each for API call) to simulate a multi-step LLM process. 