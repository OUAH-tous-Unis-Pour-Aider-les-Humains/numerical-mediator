from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.science import Hypothese


class HypotheseRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, *, limit: int = 50, offset: int = 0) -> list[Hypothese]:
        stmt = select(Hypothese).order_by(Hypothese.id).offset(offset).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get(self, hypothese_id: UUID) -> Hypothese | None:
        return self.db.get(Hypothese, hypothese_id)

    def create(self, hypothese: Hypothese) -> Hypothese:
        self.db.add(hypothese)
        self.db.flush()
        self.db.refresh(hypothese)
        return hypothese

    def delete(self, hypothese: Hypothese) -> None:
        self.db.delete(hypothese)
