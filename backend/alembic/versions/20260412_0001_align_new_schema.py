"""Align database schema with classification, source, and maths structure

Revision ID: 20260412_0001
Revises: 20260406_0001
Create Date: 2026-04-12
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "20260412_0001"
down_revision: Union[str, None] = "20260406_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("source", "date_source", new_column_name="date")
    op.drop_column("source", "date_depot")

    op.alter_column("formule_maths", "cle", new_column_name="intitule")
    op.drop_index("ix_formule_maths_cle", table_name="formule_maths")
    op.create_index("ix_formule_maths_intitule", "formule_maths", ["intitule"], unique=True)
    op.add_column("formule_maths", sa.Column("symbole", sa.String(length=32), nullable=True))
    op.add_column("formule_maths", sa.Column("demonstration_latex", sa.Text(), nullable=True))
    op.create_index("ix_formule_maths_symbole", "formule_maths", ["symbole"], unique=False)

    op.create_table(
        "formule_maths_utilisation",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("formule_maths_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("reference_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("nom_reference_dans_demonstration", sa.String(length=100), nullable=False),
        sa.ForeignKeyConstraint(["formule_maths_id"], ["formule_maths.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["reference_id"], ["formule_maths.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("formule_maths_id", "reference_id", name="uq_formule_maths_utilisation"),
    )
    op.create_index(
        "ix_formule_maths_utilisation_formule_maths_id",
        "formule_maths_utilisation",
        ["formule_maths_id"],
        unique=False,
    )
    op.create_index(
        "ix_formule_maths_utilisation_reference_id",
        "formule_maths_utilisation",
        ["reference_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_formule_maths_utilisation_reference_id", table_name="formule_maths_utilisation")
    op.drop_index("ix_formule_maths_utilisation_formule_maths_id", table_name="formule_maths_utilisation")
    op.drop_table("formule_maths_utilisation")

    op.drop_index("ix_formule_maths_symbole", table_name="formule_maths")
    op.drop_column("formule_maths", "demonstration_latex")
    op.drop_column("formule_maths", "symbole")
    op.drop_index("ix_formule_maths_intitule", table_name="formule_maths")
    op.alter_column("formule_maths", "intitule", new_column_name="cle")
    op.create_index("ix_formule_maths_cle", "formule_maths", ["cle"], unique=True)

    op.add_column("source", sa.Column("date_depot", sa.Date(), nullable=True))
    op.alter_column("source", "date", new_column_name="date_source")
