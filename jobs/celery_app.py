import os

from celery import Celery

from app.core.config import get_settings


settings = get_settings()

celery_app = Celery(
    "py.api.joinroster.co",
    broker=os.getenv("QUEUE_CONNECTION_URL", os.getenv("REDIS_URL", "redis://localhost:6379/0")),
)

celery_app.conf.update(
    task_default_queue="default",
)


@celery_app.task(name="jobs.dummy")
def dummy_task() -> None:
    """
    Placeholder Celery task; real jobs will be mapped from Laravel's jobs
    defined in the migration spec (ProcessUserCreatorRefresh, etc.).
    """

