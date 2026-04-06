from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.experimentation import Donnee
from app.repositories.experimentation import DonneeRepository
from app.schemas.experimentation import DonneeCreate, DonneeUpdate


class DonneeService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = DonneeRepository(db)

    def list(self, *, limit: int = 50, offset: int = 0) -> list[Donnee]:
        return self.repo.list(limit=limit, offset=offset)

    def get_or_404(self, donnee_id: UUID) -> Donnee:
        donnee = self.repo.get(donnee_id)
        if donnee is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donnée introuvable")
        return donnee

    def create(self, payload: DonneeCreate) -> Donnee:
        donnee = Donnee(**payload.model_dump())
        created = self.repo.create(donnee)
        self.db.commit()
        return created

    def update(self, donnee_id: UUID, payload: DonneeUpdate) -> Donnee:
        donnee = self.get_or_404(donnee_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(donnee, field, value)
        self.db.flush()
        self.db.commit()
        self.db.refresh(donnee)
        return donnee

    def delete(self, donnee_id: UUID) -> None:
        donnee = self.get_or_404(donnee_id)
        self.repo.delete(donnee)
        self.db.commit()
