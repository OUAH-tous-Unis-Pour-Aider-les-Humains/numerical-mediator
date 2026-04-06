from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.classification import ClassificationNature


class ClassificationObjetCreate(BaseModel):
    wikidata_ref: str = Field(min_length=1, max_length=255)
    nom_fr: str = Field(min_length=1, max_length=255)
    formule_latex: str | None = None
    nature: ClassificationNature


class ClassificationObjetUpdate(BaseModel):
    wikidata_ref: str | None = Field(default=None, min_length=1, max_length=255)
    nom_fr: str | None = Field(default=None, min_length=1, max_length=255)
    formule_latex: str | None = None
    nature: ClassificationNature | None = None


class ClassificationObjetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    wikidata_ref: str
    nom_fr: str
    formule_latex: str | None
    nature: ClassificationNature
