from fastapi import APIRouter

from app.worker.celery_app import celery_app
from app.worker.tasks import ping

router = APIRouter(prefix="/system", tags=["system"])


@router.post("/celery/ping")
def trigger_celery_ping() -> dict[str, str]:
    task = ping.delay()
    return {"task_id": task.id, "state": "queued"}


@router.get("/celery/tasks/{task_id}")
def get_celery_task_state(task_id: str) -> dict[str, str]:
    result = celery_app.AsyncResult(task_id)
    return {"task_id": task_id, "state": result.state}
