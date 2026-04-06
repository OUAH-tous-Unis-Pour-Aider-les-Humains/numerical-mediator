from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.classification import (
    ClassificationObjetCreate,
    ClassificationObjetRead,
    ClassificationObjetUpdate,
)
from app.services.classification import ClassificationService

router = APIRouter(prefix="/classification-objets", tags=["classification"])


@router.get("", response_model=list[ClassificationObjetRead])
def list_classification_objets(
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    service = ClassificationService(db)
    return service.list(limit=limit, offset=offset)


@router.post("", response_model=ClassificationObjetRead, status_code=status.HTTP_201_CREATED)
def create_classification_objet(
    payload: ClassificationObjetCreate,
    db: Session = Depends(get_db),
):
    service = ClassificationService(db)
    return service.create(payload)


@router.get("/{object_id}", response_model=ClassificationObjetRead)
def get_classification_objet(object_id: UUID, db: Session = Depends(get_db)):
    service = ClassificationService(db)
    return service.get_or_404(object_id)


@router.patch("/{object_id}", response_model=ClassificationObjetRead)
def update_classification_objet(
    object_id: UUID,
    payload: ClassificationObjetUpdate,
    db: Session = Depends(get_db),
):
    service = ClassificationService(db)
    return service.update(object_id, payload)


@router.delete("/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_classification_objet(object_id: UUID, db: Session = Depends(get_db)) -> Response:
    service = ClassificationService(db)
    service.delete(object_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
