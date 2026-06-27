"""Celery application configuration."""

from celery import Celery

from backend.config.settings import get_settings

settings = get_settings()

celery_app = Celery(
    "pyrocast",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["backend.workers.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
    task_soft_time_limit=3300,
    worker_prefetch_multiplier=1,
    task_always_eager=settings.celery_task_always_eager,
    task_routes={
        "backend.workers.tasks.*": {"queue": "pyrocast"},
    },
)
