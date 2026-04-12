from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.maths import FormuleMaths
from app.repositories.maths import FormuleMathsRepository
from app.schemas.maths import FormuleMathsCreate, FormuleMathsUpdate


class FormuleMathsService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = FormuleMathsRepository(db)

    def list(self, *, limit: int = 50, offset: int = 0) -> list[FormuleMaths]:
        return self.repo.list(limit=limit, offset=offset)

    def get_or_404(self, formule_id: UUID) -> FormuleMaths:
        formule = self.repo.get(formule_id)
        if formule is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Formule introuvable")
        return formule

    def create(self, payload: FormuleMathsCreate) -> FormuleMaths:
        formule = FormuleMaths(**payload.model_dump())
        try:
            created = self.repo.create(formule)
            self.db.commit()
            return created
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Intitulé déjà existant") from exc

    def update(self, formule_id: UUID, payload: FormuleMathsUpdate) -> FormuleMaths:
        formule = self.get_or_404(formule_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(formule, field, value)

        try:
            self.db.flush()
            self.db.commit()
            self.db.refresh(formule)
            return formule
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflit de données") from exc

    def delete(self, formule_id: UUID) -> None:
        formule = self.get_or_404(formule_id)
        self.repo.delete(formule)
        self.db.commit()
