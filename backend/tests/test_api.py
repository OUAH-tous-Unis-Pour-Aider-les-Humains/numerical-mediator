from __future__ import annotations

from types import SimpleNamespace
from uuid import UUID, uuid4

from app.api import classification as classification_api
from app.api import experimentation as experimentation_api
from app.api import maths as maths_api
from app.api import science as science_api
from app.api import system as system_api


class FakeClassificationService:
    def __init__(self, db=None) -> None:
        self.db = db

    def list(self, *, limit: int = 50, offset: int = 0):
        return [
            SimpleNamespace(
                id=uuid4(),
                wikidata_ref="Q1",
                nom_fr="Nombre",
                formule_latex="1",
                nature="nombre",
            )
        ]

    def create(self, payload):
        return SimpleNamespace(id=uuid4(), **payload.model_dump())

    def get_or_404(self, object_id: UUID):
        return SimpleNamespace(
            id=object_id,
            wikidata_ref="Q1",
            nom_fr="Nombre",
            formule_latex="1",
            nature="nombre",
        )

    def update(self, object_id: UUID, payload):
        data = {
            "id": object_id,
            "wikidata_ref": "Q1",
            "nom_fr": "Nombre",
            "formule_latex": "1",
            "nature": "nombre",
        }
        data.update(payload.model_dump(exclude_unset=True))
        return SimpleNamespace(**data)

    def delete(self, object_id: UUID):
        return None


class FakeDonneeService:
    def __init__(self, db=None) -> None:
        self.db = db

    def list(self, *, limit: int = 50, offset: int = 0):
        return [SimpleNamespace(id=uuid4(), contenu={"phrase": "bonjour"})]

    def create(self, payload):
        return SimpleNamespace(id=uuid4(), **payload.model_dump())

    def get_or_404(self, donnee_id: UUID):
        return SimpleNamespace(id=donnee_id, contenu={"phrase": "bonjour"})

    def update(self, donnee_id: UUID, payload):
        data = {"id": donnee_id, "contenu": {"phrase": "bonjour"}}
        data.update(payload.model_dump(exclude_unset=True))
        return SimpleNamespace(**data)

    def delete(self, donnee_id: UUID):
        return None


class FakeFormuleMathsService:
    def __init__(self, db=None) -> None:
        self.db = db

    def list(self, *, limit: int = 50, offset: int = 0):
        return [SimpleNamespace(id=uuid4(), cle="axiome_1", formule_latex="a=a", est_axiome=True)]

    def create(self, payload):
        return SimpleNamespace(id=uuid4(), **payload.model_dump())

    def get_or_404(self, formule_id: UUID):
        return SimpleNamespace(id=formule_id, cle="axiome_1", formule_latex="a=a", est_axiome=True)

    def update(self, formule_id: UUID, payload):
        data = {"id": formule_id, "cle": "axiome_1", "formule_latex": "a=a", "est_axiome": True}
        data.update(payload.model_dump(exclude_unset=True))
        return SimpleNamespace(**data)

    def delete(self, formule_id: UUID):
        return None


class FakeHypotheseService:
    def __init__(self, db=None) -> None:
        self.db = db

    def list(self, *, limit: int = 50, offset: int = 0):
        return [SimpleNamespace(id=uuid4(), formule_latex="E=mc^2", statut=0.9)]

    def create(self, payload):
        return SimpleNamespace(id=uuid4(), **payload.model_dump())

    def get_or_404(self, hypothese_id: UUID):
        return SimpleNamespace(id=hypothese_id, formule_latex="E=mc^2", statut=0.9)

    def update(self, hypothese_id: UUID, payload):
        data = {"id": hypothese_id, "formule_latex": "E=mc^2", "statut": 0.9}
        data.update(payload.model_dump(exclude_unset=True))
        return SimpleNamespace(**data)

    def delete(self, hypothese_id: UUID):
        return None


class FakeTaskResult:
    def __init__(self, task_id: str, state: str = "SUCCESS") -> None:
        self.id = task_id
        self.state = state


class FakeTask:
    def delay(self):
        return SimpleNamespace(id="task-123")


class FakeCeleryApp:
    def AsyncResult(self, task_id: str):
        return FakeTaskResult(task_id)


def test_healthcheck(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_classification_crud(client, monkeypatch):
    monkeypatch.setattr(classification_api, "ClassificationService", FakeClassificationService)

    created = client.post(
        "/classification-objets",
        json={"wikidata_ref": "Q1", "nom_fr": "Nombre", "formule_latex": "1", "nature": "nombre"},
    )
    assert created.status_code == 201
    assert created.json()["wikidata_ref"] == "Q1"

    listed = client.get("/classification-objets")
    assert listed.status_code == 200
    assert listed.json()[0]["nom_fr"] == "Nombre"

    object_id = created.json()["id"]
    fetched = client.get(f"/classification-objets/{object_id}")
    assert fetched.status_code == 200

    updated = client.patch(
        f"/classification-objets/{object_id}",
        json={"nom_fr": "Grandeur"},
    )
    assert updated.status_code == 200
    assert updated.json()["nom_fr"] == "Grandeur"

    deleted = client.delete(f"/classification-objets/{object_id}")
    assert deleted.status_code == 204


def test_donnee_crud(client, monkeypatch):
    monkeypatch.setattr(experimentation_api, "DonneeService", FakeDonneeService)

    created = client.post("/donnees", json={"contenu": {"phrase": "bonjour"}})
    assert created.status_code == 201
    assert created.json()["contenu"] == {"phrase": "bonjour"}

    listed = client.get("/donnees")
    assert listed.status_code == 200
    assert listed.json()[0]["contenu"] == {"phrase": "bonjour"}

    donnee_id = created.json()["id"]
    fetched = client.get(f"/donnees/{donnee_id}")
    assert fetched.status_code == 200

    updated = client.patch(f"/donnees/{donnee_id}", json={"contenu": {"phrase": "salut"}})
    assert updated.status_code == 200
    assert updated.json()["contenu"] == {"phrase": "salut"}

    deleted = client.delete(f"/donnees/{donnee_id}")
    assert deleted.status_code == 204


def test_formule_maths_crud(client, monkeypatch):
    monkeypatch.setattr(maths_api, "FormuleMathsService", FakeFormuleMathsService)

    created = client.post(
        "/formules-maths",
        json={"cle": "axiome_1", "formule_latex": "a=a", "est_axiome": True},
    )
    assert created.status_code == 201
    assert created.json()["cle"] == "axiome_1"

    listed = client.get("/formules-maths")
    assert listed.status_code == 200
    assert listed.json()[0]["est_axiome"] is True

    formule_id = created.json()["id"]
    fetched = client.get(f"/formules-maths/{formule_id}")
    assert fetched.status_code == 200

    updated = client.patch(f"/formules-maths/{formule_id}", json={"cle": "axiome_2"})
    assert updated.status_code == 200
    assert updated.json()["cle"] == "axiome_2"

    deleted = client.delete(f"/formules-maths/{formule_id}")
    assert deleted.status_code == 204


def test_hypothese_crud(client, monkeypatch):
    monkeypatch.setattr(science_api, "HypotheseService", FakeHypotheseService)

    created = client.post("/hypotheses", json={"formule_latex": "E=mc^2", "statut": 0.9})
    assert created.status_code == 201
    assert created.json()["formule_latex"] == "E=mc^2"

    listed = client.get("/hypotheses")
    assert listed.status_code == 200
    assert listed.json()[0]["statut"] == 0.9

    hypothese_id = created.json()["id"]
    fetched = client.get(f"/hypotheses/{hypothese_id}")
    assert fetched.status_code == 200

    updated = client.patch(f"/hypotheses/{hypothese_id}", json={"statut": 0.8})
    assert updated.status_code == 200
    assert updated.json()["statut"] == 0.8

    deleted = client.delete(f"/hypotheses/{hypothese_id}")
    assert deleted.status_code == 204


def test_celery_ping_and_status(client, monkeypatch):
    monkeypatch.setattr(system_api, "ping", FakeTask())
    monkeypatch.setattr(system_api, "celery_app", FakeCeleryApp())

    queued = client.post("/system/celery/ping")
    assert queued.status_code == 200
    task_id = queued.json()["task_id"]
    assert task_id == "task-123"

    state = client.get(f"/system/celery/tasks/{task_id}")
    assert state.status_code == 200
    assert state.json() == {"task_id": "task-123", "state": "SUCCESS"}
