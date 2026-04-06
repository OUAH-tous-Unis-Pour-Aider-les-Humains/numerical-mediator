from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.maths import FormuleMathsCreate, FormuleMathsRead, FormuleMathsUpdate
from app.services.maths import FormuleMathsService

router = APIRouter(prefix="/formules-maths", tags=["maths"])


@router.get("", response_model=list[FormuleMathsRead])
def list_formules_maths(
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    service = FormuleMathsService(db)
    return service.list(limit=limit, offset=offset)


@router.post("", response_model=FormuleMathsRead, status_code=status.HTTP_201_CREATED)
def create_formule_maths(payload: FormuleMathsCreate, db: Session = Depends(get_db)):
    service = FormuleMathsService(db)
    return service.create(payload)


@router.get("/{formule_id}", response_model=FormuleMathsRead)
def get_formule_maths(formule_id: UUID, db: Session = Depends(get_db)):
    service = FormuleMathsService(db)
    return service.get_or_404(formule_id)


@router.patch("/{formule_id}", response_model=FormuleMathsRead)
def update_formule_maths(
    formule_id: UUID,
    payload: FormuleMathsUpdate,
    db: Session = Depends(get_db),
):
    service = FormuleMathsService(db)
    return service.update(formule_id, payload)


@router.delete("/{formule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_formule_maths(formule_id: UUID, db: Session = Depends(get_db)) -> Response:
    service = FormuleMathsService(db)
    service.delete(formule_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
