from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class HypotheseCreate(BaseModel):
    formule_latex: str = Field(min_length=1)
    statut: float | None = None


class HypotheseUpdate(BaseModel):
    formule_latex: str | None = Field(default=None, min_length=1)
    statut: float | None = None


class HypotheseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    formule_latex: str
    statut: float | None
