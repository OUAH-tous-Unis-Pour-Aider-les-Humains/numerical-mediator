from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DonneeCreate(BaseModel):
    contenu: dict[str, Any]


class DonneeUpdate(BaseModel):
    contenu: dict[str, Any] | None = None


class DonneeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    contenu: dict[str, Any]
