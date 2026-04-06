from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.science import Hypothese
from app.repositories.science import HypotheseRepository
from app.schemas.science import HypotheseCreate, HypotheseUpdate


class HypotheseService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = HypotheseRepository(db)

    def list(self, *, limit: int = 50, offset: int = 0) -> list[Hypothese]:
        return self.repo.list(limit=limit, offset=offset)

    def get_or_404(self, hypothese_id: UUID) -> Hypothese:
        hypothese = self.repo.get(hypothese_id)
        if hypothese is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hypothèse introuvable")
        return hypothese

    def create(self, payload: HypotheseCreate) -> Hypothese:
        hypothese = Hypothese(**payload.model_dump())
        created = self.repo.create(hypothese)
        self.db.commit()
        return created

    def update(self, hypothese_id: UUID, payload: HypotheseUpdate) -> Hypothese:
        hypothese = self.get_or_404(hypothese_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(hypothese, field, value)
        self.db.flush()
        self.db.commit()
        self.db.refresh(hypothese)
        return hypothese

    def delete(self, hypothese_id: UUID) -> None:
        hypothese = self.get_or_404(hypothese_id)
        self.repo.delete(hypothese)
        self.db.commit()
