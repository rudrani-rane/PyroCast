"""Celery task definitions for async data ingestion and inference."""

from celery import Task

from backend.workers.celery_app import celery_app


@celery_app.task(name="backend.workers.tasks.ping", bind=True)  # type: ignore[untyped-decorator]
def ping(self: Task) -> dict[str, str]:
    """Verify Celery worker connectivity."""
    return {"status": "pong", "task_id": self.request.id}
