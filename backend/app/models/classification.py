import enum
import uuid

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ClassificationNature(str, enum.Enum):
    NOMBRE = "nombre"
    ENSEMBLE = "ensemble"
    UNITE = "unite"
    CONSTANTE = "constante"
    AUTRE = "autre"


class ClassificationObjet(Base):
    __tablename__ = "classification_objet"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wikidata_ref: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    nom_fr: Mapped[str] = mapped_column(String(255), index=True)
    formule_latex: Mapped[str | None] = mapped_column(Text(), nullable=True)
    nature: Mapped[ClassificationNature] = mapped_column(
        Enum(ClassificationNature, name="classification_nature_enum"), nullable=False
    )

    variables: Mapped[list["ClassificationVariable"]] = relationship(
        back_populates="objet", cascade="all, delete-orphan"
    )
    hypothese_variables: Mapped[list["HypotheseVariable"]] = relationship(back_populates="classification")


class ClassificationVariable(Base):
    __tablename__ = "classification_variable"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    objet_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("classification_objet.id", ondelete="CASCADE"), nullable=False, index=True
    )
    lettre: Mapped[str] = mapped_column(String(1), nullable=False)
    wikidata_ref: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    objet: Mapped[ClassificationObjet] = relationship(back_populates="variables")


from app.models.science import HypotheseVariable  # noqa: E402
