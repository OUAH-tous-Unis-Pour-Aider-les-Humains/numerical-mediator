from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.maths import FormuleMaths


class FormuleMathsRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, *, limit: int = 50, offset: int = 0) -> list[FormuleMaths]:
        stmt = select(FormuleMaths).order_by(FormuleMaths.intitule).offset(offset).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get(self, formule_id: UUID) -> FormuleMaths | None:
        return self.db.get(FormuleMaths, formule_id)

    def create(self, formule: FormuleMaths) -> FormuleMaths:
        self.db.add(formule)
        self.db.flush()
        self.db.refresh(formule)
        return formule

    def delete(self, formule: FormuleMaths) -> None:
        self.db.delete(formule)
