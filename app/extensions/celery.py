"""Celery factory bound to the Flask application context."""
from __future__ import annotations

from celery import Celery
from kombu import Queue

celery = Celery(__name__)


def make_celery(app) -> Celery:
    """Configure Celery with Flask settings and context."""

    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        task_default_queue=app.config.get("CELERY_TASK_DEFAULT_QUEUE", "pokemon_sync"),
        task_acks_late=app.config.get("CELERY_TASK_ACKS_LATE", True),
        task_time_limit=app.config.get("CELERY_TASK_TIME_LIMIT", 30),
        task_soft_time_limit=app.config.get("CELERY_TASK_SOFT_TIME_LIMIT", 25),
        task_default_retry_delay=app.config.get("CELERY_TASK_RETRY_DELAY", 5),
        task_annotations={"*": {"max_retries": app.config.get("CELERY_TASK_MAX_RETRIES", 3)}},
        task_serializer="json",
        accept_content=["json"],
        result_expires=app.config.get("CELERY_RESULT_EXPIRES", 3600),
        task_always_eager=app.config.get("CELERY_TASK_ALWAYS_EAGER", False),
        task_store_eager_result=app.config.get("CELERY_TASK_STORE_EAGER_RESULT", False),
        task_ignore_result=app.config.get("CELERY_TASK_IGNORE_RESULT", False),
        include=["app.tasks.pokemon"],
    )

    celery.conf.task_queues = (
        Queue(celery.conf.task_default_queue, routing_key="pokemon.sync"),
    )

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    app.extensions["celery"] = celery
    return celery


def init_app(app):
    return make_celery(app)
