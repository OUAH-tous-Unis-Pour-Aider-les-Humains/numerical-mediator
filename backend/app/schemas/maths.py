from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class FormuleMathsCreate(BaseModel):
    cle: str = Field(min_length=1, max_length=100)
    formule_latex: str = Field(min_length=1)
    est_axiome: bool = False


class FormuleMathsUpdate(BaseModel):
    cle: str | None = Field(default=None, min_length=1, max_length=100)
    formule_latex: str | None = Field(default=None, min_length=1)
    est_axiome: bool | None = None


class FormuleMathsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    cle: str
    formule_latex: str
    est_axiome: bool
