from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.science import HypotheseCreate, HypotheseRead, HypotheseUpdate
from app.services.science import HypotheseService

router = APIRouter(prefix="/hypotheses", tags=["science"])


@router.get("", response_model=list[HypotheseRead])
def list_hypotheses(
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    service = HypotheseService(db)
    return service.list(limit=limit, offset=offset)


@router.post("", response_model=HypotheseRead, status_code=status.HTTP_201_CREATED)
def create_hypothese(payload: HypotheseCreate, db: Session = Depends(get_db)):
    service = HypotheseService(db)
    return service.create(payload)


@router.get("/{hypothese_id}", response_model=HypotheseRead)
def get_hypothese(hypothese_id: UUID, db: Session = Depends(get_db)):
    service = HypotheseService(db)
    return service.get_or_404(hypothese_id)


@router.patch("/{hypothese_id}", response_model=HypotheseRead)
def update_hypothese(
    hypothese_id: UUID,
    payload: HypotheseUpdate,
    db: Session = Depends(get_db),
):
    service = HypotheseService(db)
    return service.update(hypothese_id, payload)


@router.delete("/{hypothese_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hypothese(hypothese_id: UUID, db: Session = Depends(get_db)) -> Response:
    service = HypotheseService(db)
    service.delete(hypothese_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
