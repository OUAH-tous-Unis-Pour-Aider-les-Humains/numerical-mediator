import uuid
from datetime import date
from typing import Any

from sqlalchemy import Date, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Source(Base):
    __tablename__ = "source"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date: Mapped[date | None] = mapped_column(Date(), nullable=True)
    lieu: Mapped[str | None] = mapped_column(String(255), nullable=True)
    auteur: Mapped[str | None] = mapped_column(String(255), nullable=True)
    environnement: Mapped[str | None] = mapped_column(String(255), nullable=True)

    donnees_associees: Mapped[list["SourceDonnee"]] = relationship(
        back_populates="source", cascade="all, delete-orphan"
    )


class Donnee(Base):
    __tablename__ = "donnee"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contenu: Mapped[Any] = mapped_column(JSONB, nullable=False)

    sources_associees: Mapped[list["SourceDonnee"]] = relationship(
        back_populates="donnee", cascade="all, delete-orphan"
    )
    relations_sortantes: Mapped[list["DonneeRelation"]] = relationship(
        foreign_keys="DonneeRelation.donnee_a_id",
        back_populates="donnee_a",
        cascade="all, delete-orphan",
    )
    relations_entrantes: Mapped[list["DonneeRelation"]] = relationship(
        foreign_keys="DonneeRelation.donnee_b_id",
        back_populates="donnee_b",
        cascade="all, delete-orphan",
    )
    hypotheses_pour: Mapped[list["HypothesePour"]] = relationship(back_populates="donnee")
    hypotheses_contre: Mapped[list["HypotheseContre"]] = relationship(back_populates="donnee")


class SourceDonnee(Base):
    __tablename__ = "source_donnee"
    __table_args__ = (PrimaryKeyConstraint("source_id", "donnee_id", name="pk_source_donnee"),)

    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("source.id", ondelete="CASCADE"), nullable=False
    )
    donnee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("donnee.id", ondelete="CASCADE"), nullable=False
    )

    source: Mapped[Source] = relationship(back_populates="donnees_associees")
    donnee: Mapped[Donnee] = relationship(back_populates="sources_associees")


class DonneeRelation(Base):
    __tablename__ = "donnee_relation"
    __table_args__ = (PrimaryKeyConstraint("donnee_a_id", "donnee_b_id", name="pk_donnee_relation"),)

    donnee_a_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("donnee.id", ondelete="CASCADE"), nullable=False
    )
    donnee_b_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("donnee.id", ondelete="CASCADE"), nullable=False
    )

    donnee_a: Mapped[Donnee] = relationship(foreign_keys=[donnee_a_id], back_populates="relations_sortantes")
    donnee_b: Mapped[Donnee] = relationship(foreign_keys=[donnee_b_id], back_populates="relations_entrantes")


from app.models.science import HypotheseContre, HypothesePour  # noqa: E402
