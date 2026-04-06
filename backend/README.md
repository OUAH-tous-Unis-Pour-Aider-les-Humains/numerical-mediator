# Backend starter (FastAPI + SQLAlchemy + Alembic)

Ce dossier contient une base de travail pour l'API Python du projet.

## Stack

- FastAPI
- SQLAlchemy 2.0
- Alembic
- PostgreSQL (driver psycopg v3)
- Celery + Redis (prepare, non branche sur des workers metier pour l'instant)

## Prerequis

- Python 3.11+
- PostgreSQL 16+
- Redis 7+ (si vous voulez tester Celery)

## Installation

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Lancer l'API

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Ou via Makefile:

```bash
cd backend
make run
```

Le Makefile utilise automatiquement `backend/.venv` si present, sinon `../.venv`.

Endpoints de base:

- GET /health
- GET /docs
- POST /system/celery/ping
- GET /system/celery/tasks/{task_id}

CRUD V1 expose:

- /classification-objets
- /donnees
- /formules-maths
- /hypotheses

## Migrations

```bash
cd backend
source .venv/bin/activate
alembic upgrade head
```

Pour generer une nouvelle migration apres modification des modeles:

```bash
alembic revision --autogenerate -m "describe change"
```

Ou via Makefile:

```bash
cd backend
make migrate
```

## Worker Celery

```bash
cd backend
source .venv/bin/activate
celery -A app.worker.celery_app.celery_app worker --loglevel=info
```

Ou via Makefile:

```bash
cd backend
make worker
```

## Structure

- app/main.py: entree FastAPI
- app/core/config.py: configuration centralisee via variables d'environnement
- app/db/: base declarative SQLAlchemy + session
- app/models/: modeles metier (classification, experimentation, maths, science)
- app/schemas/: schemas d'entree/sortie API (Pydantic v2)
- app/repositories/: acces DB par agregat
- app/services/: logique applicative par agregat
- app/worker/: configuration Celery et tasks
- alembic/: configuration et scripts de migration

## Limites V1

- Authentification/autorisation non implementees.
- Regles metier avancees de fusion pour/contre non implementees.
- Pas encore de suite de tests automatisee dans ce lot.

## Notes schema

Le schema implemente suit le diagramme de reference dans le fichier:

- ../schema_bdd_complet.html
