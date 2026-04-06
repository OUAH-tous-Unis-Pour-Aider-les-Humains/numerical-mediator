import uuid

from sqlalchemy import Boolean, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class FormuleMaths(Base):
    __tablename__ = "formule_maths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cle: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    formule_latex: Mapped[str] = mapped_column(Text(), nullable=False)
    est_axiome: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)
