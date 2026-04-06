from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.classification import ClassificationObjet


class ClassificationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, *, limit: int = 50, offset: int = 0) -> list[ClassificationObjet]:
        stmt = select(ClassificationObjet).order_by(ClassificationObjet.nom_fr).offset(offset).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get(self, object_id: UUID) -> ClassificationObjet | None:
        return self.db.get(ClassificationObjet, object_id)

    def create(self, obj: ClassificationObjet) -> ClassificationObjet:
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ClassificationObjet) -> None:
        self.db.delete(obj)
