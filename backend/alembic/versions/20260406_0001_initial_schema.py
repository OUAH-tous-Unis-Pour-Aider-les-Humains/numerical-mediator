"""Initial schema from schema_bdd_complet.html

Revision ID: 20260406_0001
Revises:
Create Date: 2026-04-06

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "20260406_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


classification_nature_enum = sa.Enum(
    "nombre",
    "ensemble",
    "unite",
    "constante",
    "autre",
    name="classification_nature_enum",
)


def upgrade() -> None:
    classification_nature_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "classification_objet",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("wikidata_ref", sa.String(length=255), nullable=False),
        sa.Column("nom_fr", sa.String(length=255), nullable=False),
        sa.Column("formule_latex", sa.Text(), nullable=True),
        sa.Column("nature", classification_nature_enum, nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_classification_objet_wikidata_ref", "classification_objet", ["wikidata_ref"], unique=True)
    op.create_index("ix_classification_objet_nom_fr", "classification_objet", ["nom_fr"], unique=False)

    op.create_table(
        "donnee",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("contenu", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "formule_maths",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("cle", sa.String(length=100), nullable=False),
        sa.Column("formule_latex", sa.Text(), nullable=False),
        sa.Column("est_axiome", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_formule_maths_cle", "formule_maths", ["cle"], unique=True)

    op.create_table(
        "hypothese",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("formule_latex", sa.Text(), nullable=False),
        sa.Column("statut", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "source",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("date_source", sa.Date(), nullable=True),
        sa.Column("lieu", sa.String(length=255), nullable=True),
        sa.Column("auteur", sa.String(length=255), nullable=True),
        sa.Column("environnement", sa.String(length=255), nullable=True),
        sa.Column("date_depot", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "classification_variable",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("objet_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("lettre", sa.String(length=1), nullable=False),
        sa.Column("wikidata_ref", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["objet_id"], ["classification_objet.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_classification_variable_objet_id", "classification_variable", ["objet_id"], unique=False)
    op.create_index(
        "ix_classification_variable_wikidata_ref",
        "classification_variable",
        ["wikidata_ref"],
        unique=False,
    )

    op.create_table(
        "donnee_relation",
        sa.Column("donnee_a_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("donnee_b_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["donnee_a_id"], ["donnee.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["donnee_b_id"], ["donnee.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("donnee_a_id", "donnee_b_id", name="pk_donnee_relation"),
    )

    op.create_table(
        "source_donnee",
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("donnee_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["source_id"], ["source.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["donnee_id"], ["donnee.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("source_id", "donnee_id", name="pk_source_donnee"),
    )

    op.create_table(
        "hypothese_contre",
        sa.Column("hypothese_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("donnee_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["hypothese_id"], ["hypothese.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["donnee_id"], ["donnee.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("hypothese_id", "donnee_id", name="pk_hypothese_contre"),
    )

    op.create_table(
        "hypothese_pour",
        sa.Column("hypothese_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("donnee_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["hypothese_id"], ["hypothese.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["donnee_id"], ["donnee.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("hypothese_id", "donnee_id", name="pk_hypothese_pour"),
    )

    op.create_table(
        "hypothese_variable",
        sa.Column("hypothese_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("lettre", sa.String(length=1), nullable=False),
        sa.Column("classification_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["classification_id"], ["classification_objet.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["hypothese_id"], ["hypothese.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("hypothese_id", "lettre", name="pk_hypothese_variable"),
    )


def downgrade() -> None:
    op.drop_table("hypothese_variable")
    op.drop_table("hypothese_pour")
    op.drop_table("hypothese_contre")
    op.drop_table("source_donnee")
    op.drop_table("donnee_relation")
    op.drop_index("ix_classification_variable_wikidata_ref", table_name="classification_variable")
    op.drop_index("ix_classification_variable_objet_id", table_name="classification_variable")
    op.drop_table("classification_variable")
    op.drop_table("source")
    op.drop_table("hypothese")
    op.drop_index("ix_formule_maths_cle", table_name="formule_maths")
    op.drop_table("formule_maths")
    op.drop_table("donnee")
    op.drop_index("ix_classification_objet_nom_fr", table_name="classification_objet")
    op.drop_index("ix_classification_objet_wikidata_ref", table_name="classification_objet")
    op.drop_table("classification_objet")
    classification_nature_enum.drop(op.get_bind(), checkfirst=True)
