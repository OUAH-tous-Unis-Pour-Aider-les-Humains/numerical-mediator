from __future__ import annotations

from app.models.classification import ClassificationObjet, ClassificationVariable
from app.models.experimentation import Donnee, DonneeRelation, Source, SourceDonnee
from app.models.maths import FormuleMaths
from app.models.science import Hypothese, HypotheseContre, HypothesePour, HypotheseVariable


def test_classification_schema_contract():
    assert ClassificationObjet.__tablename__ == "classification_objet"
    assert ClassificationVariable.__tablename__ == "classification_variable"
    assert "classification_objet.id" in {str(fk.column) for fk in ClassificationVariable.__table__.foreign_keys}


def test_experimentation_schema_contract():
    assert Source.__tablename__ == "source"
    assert Donnee.__tablename__ == "donnee"
    assert [column.name for column in SourceDonnee.__table__.primary_key.columns] == ["source_id", "donnee_id"]
    assert [column.name for column in DonneeRelation.__table__.primary_key.columns] == ["donnee_a_id", "donnee_b_id"]
    assert "source.id" in {str(fk.column) for fk in SourceDonnee.__table__.foreign_keys}
    assert "donnee.id" in {str(fk.column) for fk in DonneeRelation.__table__.foreign_keys}


def test_science_schema_contract():
    assert FormuleMaths.__tablename__ == "formule_maths"
    assert Hypothese.__tablename__ == "hypothese"
    assert [column.name for column in HypotheseVariable.__table__.primary_key.columns] == ["hypothese_id", "lettre"]
    assert [column.name for column in HypothesePour.__table__.primary_key.columns] == ["hypothese_id", "donnee_id"]
    assert [column.name for column in HypotheseContre.__table__.primary_key.columns] == ["hypothese_id", "donnee_id"]
    assert "classification_objet.id" in {str(fk.column) for fk in HypotheseVariable.__table__.foreign_keys}
    assert "donnee.id" in {str(fk.column) for fk in HypothesePour.__table__.foreign_keys}
