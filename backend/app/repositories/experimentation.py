from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.experimentation import Donnee


class DonneeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, *, limit: int = 50, offset: int = 0) -> list[Donnee]:
        stmt = select(Donnee).order_by(Donnee.id).offset(offset).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get(self, donnee_id: UUID) -> Donnee | None:
        return self.db.get(Donnee, donnee_id)

    def create(self, donnee: Donnee) -> Donnee:
        self.db.add(donnee)
        self.db.flush()
        self.db.refresh(donnee)
        return donnee

    def delete(self, donnee: Donnee) -> None:
        self.db.delete(donnee)
