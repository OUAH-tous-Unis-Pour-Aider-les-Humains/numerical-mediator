from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.classification import ClassificationObjet
from app.repositories.classification import ClassificationRepository
from app.schemas.classification import ClassificationObjetCreate, ClassificationObjetUpdate


class ClassificationService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = ClassificationRepository(db)

    def list(self, *, limit: int = 50, offset: int = 0) -> list[ClassificationObjet]:
        return self.repo.list(limit=limit, offset=offset)

    def get_or_404(self, object_id: UUID) -> ClassificationObjet:
        obj = self.repo.get(object_id)
        if obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Classification introuvable")
        return obj

    def create(self, payload: ClassificationObjetCreate) -> ClassificationObjet:
        obj = ClassificationObjet(**payload.model_dump())
        try:
            created = self.repo.create(obj)
            self.db.commit()
            return created
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Wikidata déjà existant") from exc

    def update(self, object_id: UUID, payload: ClassificationObjetUpdate) -> ClassificationObjet:
        obj = self.get_or_404(object_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)

        try:
            self.db.flush()
            self.db.commit()
            self.db.refresh(obj)
            return obj
        except IntegrityError as exc:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflit de données") from exc

    def delete(self, object_id: UUID) -> None:
        obj = self.get_or_404(object_id)
        self.repo.delete(obj)
        self.db.commit()
