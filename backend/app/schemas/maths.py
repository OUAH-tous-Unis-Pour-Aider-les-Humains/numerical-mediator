from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class FormuleMathsCreate(BaseModel):
    intitule: str = Field(min_length=1, max_length=100)
    symbole: str | None = Field(default=None, max_length=32)
    formule_latex: str = Field(min_length=1)
    demonstration_latex: str | None = None
    est_axiome: bool = False


class FormuleMathsUpdate(BaseModel):
    intitule: str | None = Field(default=None, min_length=1, max_length=100)
    symbole: str | None = Field(default=None, max_length=32)
    formule_latex: str | None = Field(default=None, min_length=1)
    demonstration_latex: str | None = None
    est_axiome: bool | None = None


class FormuleMathsRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    intitule: str
    symbole: str | None
    formule_latex: str
    demonstration_latex: str | None
    est_axiome: bool
