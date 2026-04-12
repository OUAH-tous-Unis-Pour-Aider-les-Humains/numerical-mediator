import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class FormuleMaths(Base):
    __tablename__ = "formule_maths"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    intitule: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    symbole: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    formule_latex: Mapped[str] = mapped_column(Text(), nullable=False)
    demonstration_latex: Mapped[str | None] = mapped_column(Text(), nullable=True)
    est_axiome: Mapped[bool] = mapped_column(Boolean(), default=False, nullable=False)

    references_dans_demonstration: Mapped[list["FormuleMathsDemonstrationReference"]] = relationship(
        back_populates="formule", cascade="all, delete-orphan"
    )


class FormuleMathsDemonstrationReference(Base):
    __tablename__ = "formule_maths_utilisation"
    __table_args__ = (UniqueConstraint("formule_maths_id", "reference_id", name="uq_formule_maths_utilisation"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    formule_maths_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("formule_maths.id", ondelete="CASCADE"), nullable=False, index=True
    )
    reference_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("formule_maths.id", ondelete="CASCADE"), nullable=False, index=True
    )
    nom_reference_dans_demonstration: Mapped[str] = mapped_column(String(100), nullable=False)

    formule: Mapped[FormuleMaths] = relationship(
        back_populates="references_dans_demonstration", foreign_keys=[formule_maths_id]
    )
    reference: Mapped[FormuleMaths] = relationship(foreign_keys=[reference_id])
