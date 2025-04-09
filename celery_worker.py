import os
from celery import Celery

# Create Celery instance
celery_redis_port = os.environ.get("CELERY_REDIS_PORT", "6389")
celery_app = Celery(
    "tasks",
    broker=f"redis://localhost:{celery_redis_port}/0",
    backend=f"redis://localhost:{celery_redis_port}/0",
    include=["tasks"],
)

# Optional Celery configuration
celery_app.conf.update(
    result_expires=3600,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    worker_prefetch_multiplier=1,
)

if __name__ == "__main__":
    celery_app.start()
