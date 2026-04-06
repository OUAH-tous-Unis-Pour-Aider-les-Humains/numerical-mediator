from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.experimentation import DonneeCreate, DonneeRead, DonneeUpdate
from app.services.experimentation import DonneeService

router = APIRouter(prefix="/donnees", tags=["experimentation"])


@router.get("", response_model=list[DonneeRead])
def list_donnees(
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    service = DonneeService(db)
    return service.list(limit=limit, offset=offset)


@router.post("", response_model=DonneeRead, status_code=status.HTTP_201_CREATED)
def create_donnee(payload: DonneeCreate, db: Session = Depends(get_db)):
    service = DonneeService(db)
    return service.create(payload)


@router.get("/{donnee_id}", response_model=DonneeRead)
def get_donnee(donnee_id: UUID, db: Session = Depends(get_db)):
    service = DonneeService(db)
    return service.get_or_404(donnee_id)


@router.patch("/{donnee_id}", response_model=DonneeRead)
def update_donnee(
    donnee_id: UUID,
    payload: DonneeUpdate,
    db: Session = Depends(get_db),
):
    service = DonneeService(db)
    return service.update(donnee_id, payload)


@router.delete("/{donnee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_donnee(donnee_id: UUID, db: Session = Depends(get_db)) -> Response:
    service = DonneeService(db)
    service.delete(donnee_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
