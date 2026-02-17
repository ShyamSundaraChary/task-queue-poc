import time
import random
from celery_worker import celery

@celery.task(bind=True, max_retries=3)

# Each task run total of 50 seconds (5 steps x 10 seconds each for API call) to simulate a multi-step LLM process. 
# If any step fails, the entire task will be retried from the beginning, up to 3 times, with a 60-second delay between retries.

def generate_report(self, startup_name):
    try:
        print(f"Starting report for {startup_name}")

        # Simulating multi-step LLM process
        for step in range(5):
            print(f"{startup_name}: Step {step+1}")
            time.sleep(10)  # Simulate API call

        result = f"Report generated for {startup_name}"
        return result

    except Exception as e:
        raise self.retry(exc=e, countdown=60)
