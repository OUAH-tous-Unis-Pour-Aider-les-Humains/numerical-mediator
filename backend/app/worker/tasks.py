from app.worker.celery_app import celery_app


@celery_app.task(name="system.ping")
def ping() -> dict[str, str]:
    return {"status": "pong"}
