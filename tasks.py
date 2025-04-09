import time
from celery_worker import celery_app


@celery_app.task(name="process_data_task")
def process_data_task(text):
    """
    Process data in the background
    This is a simple example that just takes some time and returns a processed result
    """
    # Simulate processing time
    time.sleep(5)

    # Process the data (in this example, just reverse and uppercase)
    result = text[::-1].upper()

    return {"processed_data": result, "original_data": text, "processing_time": 5}
