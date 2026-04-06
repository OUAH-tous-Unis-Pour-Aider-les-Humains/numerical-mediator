import uuid

from sqlalchemy import Float, ForeignKey, PrimaryKeyConstraint, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Hypothese(Base):
    __tablename__ = "hypothese"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    formule_latex: Mapped[str] = mapped_column(Text(), nullable=False)
    statut: Mapped[float | None] = mapped_column(Float(), nullable=True)

    variables: Mapped[list["HypotheseVariable"]] = relationship(
        back_populates="hypothese", cascade="all, delete-orphan"
    )
    supports: Mapped[list["HypothesePour"]] = relationship(back_populates="hypothese", cascade="all, delete-orphan")
    objections: Mapped[list["HypotheseContre"]] = relationship(
        back_populates="hypothese", cascade="all, delete-orphan"
    )


class HypotheseVariable(Base):
    __tablename__ = "hypothese_variable"
    __table_args__ = (PrimaryKeyConstraint("hypothese_id", "lettre", name="pk_hypothese_variable"),)

    hypothese_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("hypothese.id", ondelete="CASCADE"), nullable=False
    )
    lettre: Mapped[str] = mapped_column(String(1), nullable=False)
    classification_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("classification_objet.id", ondelete="RESTRICT"), nullable=False
    )

    hypothese: Mapped[Hypothese] = relationship(back_populates="variables")
    classification: Mapped["ClassificationObjet"] = relationship(back_populates="hypothese_variables")


class HypothesePour(Base):
    __tablename__ = "hypothese_pour"
    __table_args__ = (PrimaryKeyConstraint("hypothese_id", "donnee_id", name="pk_hypothese_pour"),)

    hypothese_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("hypothese.id", ondelete="CASCADE"), nullable=False
    )
    donnee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("donnee.id", ondelete="CASCADE"), nullable=False
    )

    hypothese: Mapped[Hypothese] = relationship(back_populates="supports")
    donnee: Mapped["Donnee"] = relationship(back_populates="hypotheses_pour")


class HypotheseContre(Base):
    __tablename__ = "hypothese_contre"
    __table_args__ = (PrimaryKeyConstraint("hypothese_id", "donnee_id", name="pk_hypothese_contre"),)

    hypothese_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("hypothese.id", ondelete="CASCADE"), nullable=False
    )
    donnee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("donnee.id", ondelete="CASCADE"), nullable=False
    )

    hypothese: Mapped[Hypothese] = relationship(back_populates="objections")
    donnee: Mapped["Donnee"] = relationship(back_populates="hypotheses_contre")


from app.models.classification import ClassificationObjet  # noqa: E402
from app.models.experimentation import Donnee  # noqa: E402
